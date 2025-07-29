#!/usr/bin/env python3
"""
Unified Scraper Orchestrator
Main controller that coordinates all scraping operations using the modular framework.
"""

import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import pandas as pd

from .webdriver_manager import WebDriverManager
from .pagination_manager import PaginationManager
from .data_extractor import DataExtractor
from .config_loader import ConfigLoader
from .logger import create_logger
from .unified_schema import UnifiedDataRecord, SchemaMapper

# Google Sheets API scopes
GOOGLE_SHEETS_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.readonly'
]


class ScrapingOrchestrator:
    """Main orchestrator for unified scraping operations."""

    def __init__(self, config_path: Union[str, Path]):
        """Initialize the scraping orchestrator."""
        self.config_loader = ConfigLoader()
        self.config = self.config_loader.load_config(config_path)

        # Initialize logger
        self.logger = create_logger(
            name=f"scraper_{self.config.name}",
            log_level=self.config.options.get('log_level', 'INFO')
        )

        # Initialize managers (will be created when needed)
        self.driver_manager: Optional[WebDriverManager] = None
        self.pagination_manager: Optional[PaginationManager] = None
        self.data_extractor: Optional[DataExtractor] = None

        # Results storage
        self.extracted_data: List[Dict[str, Any]] = []
        self.processed_urls: List[str] = []
        self.failed_urls: List[str] = []

        self.logger.log_config_loaded(str(config_path), self.config.name)

    def initialize_managers(self) -> None:
        """Initialize all manager instances."""
        try:
            # WebDriver configuration
            driver_config = {
                'headless': self.config.options.get('headless', True),
                'timeout': self.config.options.get('timeout', 30),
                'user_agent': self.config.options.get('user_agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
                'disable_js': self.config.options.get('disable_js', False),
                'viewport': self.config.options.get('viewport', {'width': 1920, 'height': 1080})
            }

            self.driver_manager = WebDriverManager(driver_config)

            # Pagination configuration
            pagination_config = {
                'max_pages': self.config.pagination.get('max_pages', 10),
                'page_delay': self.config.pagination.get('delay', 2.0),
                'pagination_selectors': {
                    'next_button': self._ensure_list(self.config.pagination.get('next_button', [])),
                    'load_more': self._ensure_list(self.config.pagination.get('load_more', [])),
                    'page_numbers': self._ensure_list(self.config.pagination.get('page_numbers', []))
                }
            }

            self.pagination_manager = PaginationManager(self.driver_manager, pagination_config)

            # Data extraction configuration
            extraction_config = {
                'extraction_rules': {
                    'listing_container': self.config.listing_phase.get('list_selector', 'body'),
                    'fields': self.config.data_extraction.get('selectors', {}),
                    'detail_url_selectors': self._ensure_list(
                        self.config.listing_phase.get('link_selector', [])
                    )
                },
                'required_fields': self.config.data_extraction.get('required_fields', []),
                'base_url': self.config.base_url,
                'current_url': '',
                'industry': self.config.name,
                'source_name': self.config.name
            }

            self.data_extractor = DataExtractor(extraction_config)

            self.logger.info("All managers initialized successfully")

        except Exception as e:
            self.logger.error("Failed to initialize managers", exception=e)
            raise

    def _ensure_list(self, value: Any) -> List[str]:
        """Ensure value is a list of strings."""
        if isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return [str(item) for item in value]
        else:
            return []

    def run_listing_phase(self) -> List[str]:
        """Execute the listing phase to collect URLs."""
        self.logger.info("Starting listing phase")

        if not self.config.listing_phase.get('enabled', True):
            self.logger.info("Listing phase disabled, using base URL only")
            return [self.config.base_url]

        try:
            start_url = self.config.listing_phase.get('start_url', self.config.base_url)
            self.data_extractor.config['current_url'] = start_url

            # Navigate to start URL
            if not self.driver_manager.navigate_to(start_url):
                self.logger.error(f"Failed to navigate to start URL: {start_url}")
                return []

            all_urls = []

            # Process all pages with pagination
            for page_num in self.pagination_manager.paginate_all_pages():
                self.logger.log_pagination(page_num)

                # Extract URLs from current page
                page_urls = self.data_extractor.extract_listing_urls(self.driver_manager)
                all_urls.extend(page_urls)

                self.logger.info(f"Page {page_num}: Found {len(page_urls)} URLs")

                # Add delay between pages
                delay = self.config.listing_phase.get('delay', 2.0)
                if delay > 0:
                    time.sleep(delay)

            # Remove duplicates while preserving order
            unique_urls = list(dict.fromkeys(all_urls))

            self.logger.log_extraction_phase("listing", start_url, success=True)
            self.logger.info(f"Listing phase completed: {len(unique_urls)} unique URLs found")

            return unique_urls

        except Exception as e:
            self.logger.error("Listing phase failed", exception=e)
            self.logger.log_extraction_phase("listing", start_url, success=False)
            return []

    def run_detail_phase(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Execute the detail phase to extract data from URLs."""
        self.logger.info(f"Starting detail phase with {len(urls)} URLs")

        if not self.config.detail_phase.get('enabled', True):
            self.logger.info("Detail phase disabled, extracting from listing pages")
            return self.extract_from_current_page()

        all_data = []

        for i, url in enumerate(urls, 1):
            try:
                self.logger.info(f"Processing URL {i}/{len(urls)}: {url}")
                self.data_extractor.config['current_url'] = url

                # Navigate to detail page
                if not self.driver_manager.navigate_to(url):
                    self.logger.warning(f"Failed to navigate to: {url}")
                    self.failed_urls.append(url)
                    continue

                # Extract data from current page
                page_data = self.data_extractor.extract_from_page(self.driver_manager)

                if page_data:
                    all_data.extend(page_data)
                    self.logger.log_page_processed(url, success=True, records=len(page_data))

                    for record in page_data:
                        self.logger.log_record_extracted(record, url)
                else:
                    self.logger.log_page_processed(url, success=False)

                self.processed_urls.append(url)

                # Add delay between requests
                delay = self.config.detail_phase.get('delay', 1.0)
                if delay > 0:
                    time.sleep(delay)

            except Exception as e:
                self.logger.error(f"Failed to process URL {url}", exception=e)
                self.failed_urls.append(url)
                continue

        self.logger.log_extraction_phase("detail", f"{len(urls)} URLs", success=True)
        self.logger.info(f"Detail phase completed: {len(all_data)} records extracted")

        return all_data

    def extract_from_current_page(self) -> List[Dict[str, Any]]:
        """Extract data from current page (single-phase scraping)."""
        try:
            return self.data_extractor.extract_from_page(self.driver_manager)
        except Exception as e:
            self.logger.error("Failed to extract from current page", exception=e)
            return []

    def run_scraping(self) -> Dict[str, Any]:
        """Run the complete scraping process."""
        start_time = datetime.now()
        self.logger.info(f"Starting scraping session: {self.config.name}")

        try:
            # Initialize all managers
            self.initialize_managers()

            # Determine scraping strategy
            if self.config.listing_phase.get('enabled', True):
                # Two-phase scraping: listing -> detail
                urls = self.run_listing_phase()

                if not urls:
                    self.logger.warning("No URLs found in listing phase")
                    return self._create_result_summary(start_time, success=False)

                # Extract data from detail pages
                self.extracted_data = self.run_detail_phase(urls)
            else:
                # Single-phase scraping: extract from start page
                start_url = self.config.base_url
                self.data_extractor.config['current_url'] = start_url

                if not self.driver_manager.navigate_to(start_url):
                    self.logger.error(f"Failed to navigate to: {start_url}")
                    return self._create_result_summary(start_time, success=False)

                self.extracted_data = self.extract_from_current_page()

            # Clean and validate data
            if self.extracted_data:
                self.extracted_data = self.data_extractor.clean_extracted_data(self.extracted_data)
                self.extracted_data = self.data_extractor.validate_and_enrich_data(self.extracted_data)

            # Save results
            result_summary = self._save_results(start_time)

            self.logger.info(f"Scraping completed successfully: {len(self.extracted_data)} records")
            return result_summary

        except Exception as e:
            self.logger.error("Scraping session failed", exception=e)
            return self._create_result_summary(start_time, success=False)

        finally:
            # Cleanup
            if self.driver_manager:
                self.driver_manager.quit()

            # Close logger
            self.logger.close()

    def _save_results(self, start_time: datetime) -> Dict[str, Any]:
        """Save results to configured outputs using unified schema."""
        try:
            output_files = []

            if not self.extracted_data:
                self.logger.warning("No data to save")
                return self._create_result_summary(start_time, success=True)

            # Initialize schema mapper
            schema_mapper = SchemaMapper()

            # Determine source type from config
            source_type = self.config.name.lower()
            if 'lawyer' in source_type or 'attorney' in source_type:
                source_type = 'lawyers'
            elif 'realtor' in source_type or 'real' in source_type:
                source_type = 'realtors'
            elif 'contractor' in source_type:
                source_type = 'contractors'
            else:
                source_type = 'standard'

            # Apply unified schema mapping
            mapped_data = schema_mapper.map_data_to_unified_schema(
                self.extracted_data,
                source_type=source_type,
                source_name=self.config.name
            )

            # Create DataFrame with unified schema column order
            df = schema_mapper.create_export_dataframe(mapped_data, export_type='standard')

            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = self.config.output.get('filename', f"{self.config.name}_{timestamp}")

            # Remove extension if present
            if '.' in base_filename:
                base_filename = base_filename.rsplit('.', 1)[0]

            # Create output directory
            output_dir = Path("output") / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save CSV (always) - using unified schema order
            csv_path = output_dir / f"{base_filename}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            output_files.append(str(csv_path))
            self.logger.info(f"Data saved to CSV: {csv_path}")

            # Save JSON with unified schema
            json_path = output_dir / f"{base_filename}.json"
            df.to_json(json_path, orient='records', indent=2)
            output_files.append(str(json_path))
            self.logger.info(f"Data saved to JSON: {json_path}")

            # Save Excel with unified schema
            try:
                excel_path = output_dir / f"{base_filename}.xlsx"
                df.to_excel(excel_path, index=False)
                output_files.append(str(excel_path))
                self.logger.info(f"Data saved to Excel: {excel_path}")
            except Exception as e:
                self.logger.warning(f"Failed to save Excel file: {e}")

            # Google Sheets integration (if configured)
            google_config = self.config.output.get('google_sheets', {})
            if google_config.get('enabled', False):
                try:
                    self._save_to_google_sheets(df, google_config)
                except Exception as e:
                    self.logger.warning(f"Failed to save to Google Sheets: {e}")

            return self._create_result_summary(start_time, success=True, output_files=output_files)

        except Exception as e:
            self.logger.error("Failed to save results", exception=e)
            return self._create_result_summary(start_time, success=False)

    def _save_to_google_sheets(self, df: pd.DataFrame, google_config: Dict[str, Any]) -> None:
        """Save data to Google Sheets using unified schema."""
        try:
            # Check if Google Sheets libraries are available
            try:
                from google.auth.transport.requests import Request
                from google.oauth2.credentials import Credentials
                from google_auth_oauthlib.flow import InstalledAppFlow
                from googleapiclient.discovery import build
            except ImportError:
                self.logger.error("Google Sheets libraries not installed. Install with: "
                                 "pip install google-auth google-auth-oauthlib "
                                 "google-auth-httplib2 google-api-python-client")
                return

            # Get configuration
            credentials_path = google_config.get('credentials_path', 'credentials.json')
            token_path = google_config.get('token_path', 'token.json')
            sheet_id = google_config.get('sheet_id')
            worksheet_name = google_config.get('worksheet_name', 'Scraped Data')

            if not sheet_id:
                self.logger.error("Google Sheets sheet_id not configured")
                return

            # Authentication
            creds = None
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, GOOGLE_SHEETS_SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_path):
                        self.logger.error(f"Google Sheets credentials file not found: {credentials_path}")
                        return

                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, GOOGLE_SHEETS_SCOPES)
                    creds = flow.run_local_server(port=0)

                # Save credentials for next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            # Build service
            service = build('sheets', 'v4', credentials=creds)

            # Prepare data for upload
            values = []

            # Add headers
            values.append(list(df.columns))

            # Add data rows
            for _, row in df.iterrows():
                values.append([str(value) for value in row.values])

            # Upload to Google Sheets
            body = {
                'values': values
            }

            # Clear existing data and upload new data
            service.spreadsheets().values().clear(
                spreadsheetId=sheet_id,
                range=f'{worksheet_name}!A:Z'
            ).execute()

            result = service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=f'{worksheet_name}!A1',
                valueInputOption='RAW',
                body=body
            ).execute()

            self.logger.info(f"Google Sheets updated: {result.get('updatedCells', 0)} cells updated")

        except Exception as e:
            self.logger.error("Google Sheets save failed", exception=e)
            raise

    def _create_result_summary(self, start_time: datetime, success: bool,
                             output_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a summary of the scraping results."""
        end_time = datetime.now()
        runtime = end_time - start_time

        stats = self.logger.get_stats() if hasattr(self.logger, 'get_stats') else {}

        return {
            'success': success,
            'session_name': self.config.name,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'runtime_seconds': runtime.total_seconds(),
            'runtime_formatted': str(runtime),
            'records_extracted': len(self.extracted_data),
            'urls_processed': len(self.processed_urls),
            'urls_failed': len(self.failed_urls),
            'output_files': output_files or [],
            'statistics': stats,
            'config_used': self.config.name
        }

    def create_config_template(self, name: str, base_url: str, output_path: str) -> str:
        """Create a configuration template for a new directory."""
        try:
            config = self.config_loader.generate_sample_config(name, base_url)
            self.config_loader.save_config(config, output_path)

            self.logger.info(f"Configuration template created: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to create config template: {e}")
            raise

    @classmethod
    def quick_scrape(cls, name: str, base_url: str,
                    list_selector: str = ".listing-item",
                    max_pages: int = 5) -> Dict[str, Any]:
        """Quick scraping with minimal configuration."""
        try:
            # Create temporary config
            config_loader = ConfigLoader()
            config = config_loader.generate_sample_config(name, base_url)

            # Update with provided parameters
            config.listing_phase['list_selector'] = list_selector
            config.pagination['max_pages'] = max_pages

            # Save temporary config
            temp_config_path = Path("config") / f"temp_{name}.json"
            config_loader.save_config(config, temp_config_path)

            # Run scraping
            orchestrator = cls(temp_config_path)
            result = orchestrator.run_scraping()

            # Cleanup temp config
            if temp_config_path.exists():
                temp_config_path.unlink()

            return result

        except Exception as e:
            print(f"Quick scrape failed: {e}")
            return {'success': False, 'error': str(e)}


# Convenience functions for direct usage
def scrape_directory(config_path: Union[str, Path]) -> Dict[str, Any]:
    """Scrape a directory using configuration file."""
    orchestrator = ScrapingOrchestrator(config_path)
    return orchestrator.run_scraping()


def quick_scrape(name: str, base_url: str, list_selector: str = ".listing-item",
                max_pages: int = 5) -> Dict[str, Any]:
    """Quick scraping with minimal setup."""
    return ScrapingOrchestrator.quick_scrape(name, base_url, list_selector, max_pages)


def create_config(name: str, base_url: str, output_path: str) -> str:
    """Create a configuration template."""
    loader = ConfigLoader()
    config = loader.generate_sample_config(name, base_url)
    loader.save_config(config, output_path)
    return output_path
