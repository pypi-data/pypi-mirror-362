#!/usr/bin/env python3
"""
Data Hunter - Automated Property List Discovery Module
Automatically discovers and downloads property inspection lists from municipal websites
"""

import os
import re
import time
import logging
import requests
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Tuple
import json
import hashlib

# Core dependencies
from bs4 import BeautifulSoup
import schedule
from dotenv import load_dotenv

# Optional dependencies for notifications
try:
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SMTP_AVAILABLE = True
except ImportError:
    SMTP_AVAILABLE = False

try:
    import requests as slack_requests
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

# Load environment variables
load_dotenv()

class DataHunter:
    """Automated property list discovery and download system."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize DataHunter with configuration."""
        self.config_path = config_path or "config/data_hunter_config.json"
        self.input_dir = Path("input")
        self.logs_dir = Path("logs")
        self.config = self._load_config()
        self.logger = self._setup_logging()

        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Downloaded files tracking
        self.downloaded_files = self._load_downloaded_files()

    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        default_config = {
            "sources": [
                {
                    "name": "Miami-Dade",
                    "url": "https://www.miamidade.gov/pa/property_search.asp",
                    "patterns": [
                        r".*inspection.*\.pdf",
                        r".*property.*list.*\.pdf",
                        r".*recertification.*\.pdf",
                        r".*building.*safety.*\.pdf"
                    ],
                    "enabled": True,
                    "check_frequency_hours": 24
                },
                {
                    "name": "Broward",
                    "url": "https://www.broward.org/Building/Pages/BuildingSafetyInspectionProgram.aspx",
                    "patterns": [
                        r".*inspection.*\.pdf",
                        r".*building.*safety.*\.pdf",
                        r".*property.*list.*\.pdf",
                        r".*inspection.*\.xlsx?"
                    ],
                    "enabled": True,
                    "check_frequency_hours": 24
                },
                {
                    "name": "Palm-Beach",
                    "url": "https://discover.pbcgov.org/pzb/building/Pages/Recertification.aspx",
                    "patterns": [
                        r".*recertification.*\.pdf",
                        r".*building.*list.*\.pdf",
                        r".*inspection.*\.pdf",
                        r".*property.*\.xlsx?"
                    ],
                    "enabled": True,
                    "check_frequency_hours": 24
                }
            ],
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "to_emails": []
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": ""
                },
                "console": {
                    "enabled": True
                }
            },
            "download_settings": {
                "max_file_size_mb": 50,
                "timeout_seconds": 30,
                "retry_attempts": 3,
                "retry_delay_seconds": 5
            },
            "schedule": {
                "enabled": True,
                "time": "09:00",
                "timezone": "US/Eastern"
            }
        }

        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")

        # Save default config
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger('DataHunter')
        logger.setLevel(logging.INFO)

        # File handler
        log_file = self.logs_dir / "auto_discovery.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _load_downloaded_files(self) -> Dict:
        """Load record of previously downloaded files."""
        tracking_file = self.logs_dir / "downloaded_files.json"
        if tracking_file.exists():
            try:
                with open(tracking_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_downloaded_files(self):
        """Save record of downloaded files."""
        tracking_file = self.logs_dir / "downloaded_files.json"
        with open(tracking_file, 'w') as f:
            json.dump(self.downloaded_files, f, indent=2)

    def _get_file_hash(self, url: str) -> str:
        """Generate hash for file URL to track downloads."""
        return hashlib.md5(url.encode()).hexdigest()

    def discover_files(self, source: Dict) -> List[Tuple[str, str]]:
        """Discover files from a source website."""
        found_files = []

        try:
            self.logger.info(f"Scanning {source['name']}: {source['url']}")

            response = self.session.get(
                source['url'],
                timeout=self.config['download_settings']['timeout_seconds']
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']

                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin(source['url'], href)
                elif not href.startswith('http'):
                    href = urljoin(source['url'], href)

                # Check if link matches any patterns
                for pattern in source['patterns']:
                    if re.search(pattern, href, re.IGNORECASE):
                        # Extract filename from URL or link text
                        filename = self._extract_filename(href, link.get_text(strip=True))
                        found_files.append((href, filename))
                        self.logger.info(f"Found matching file: {filename} -> {href}")
                        break

        except Exception as e:
            self.logger.error(f"Error scanning {source['name']}: {str(e)}")

        return found_files

    def _extract_filename(self, url: str, link_text: str) -> str:
        """Extract appropriate filename from URL and link text."""
        # Try to get filename from URL
        parsed_url = urlparse(url)
        url_filename = Path(parsed_url.path).name

        if url_filename and '.' in url_filename:
            return url_filename

        # Use link text as filename
        if link_text:
            # Clean up link text for filename
            filename = re.sub(r'[^\w\s-]', '', link_text).strip()
            filename = re.sub(r'[-\s]+', '_', filename)

            # Add extension if missing
            if not filename.lower().endswith(('.pdf', '.xlsx', '.xls')):
                filename += '.pdf'

            return filename

        # Fallback to generic name
        return f"document_{int(time.time())}.pdf"

    def download_file(self, url: str, filename: str, source_name: str) -> bool:
        """Download a file with retry logic."""
        file_hash = self._get_file_hash(url)

        # Check if already downloaded
        if file_hash in self.downloaded_files:
            self.logger.debug(f"File already downloaded: {filename}")
            return False

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_parts = Path(filename).stem, timestamp, source_name.lower().replace('-', '_')
        extension = Path(filename).suffix
        new_filename = f"{'_'.join(name_parts)}{extension}"

        file_path = self.input_dir / new_filename

        # Download with retry logic
        for attempt in range(self.config['download_settings']['retry_attempts']):
            try:
                self.logger.info(f"Downloading {filename} (attempt {attempt + 1})...")

                response = self.session.get(
                    url,
                    timeout=self.config['download_settings']['timeout_seconds'],
                    stream=True
                )
                response.raise_for_status()

                # Check file size
                content_length = response.headers.get('content-length')
                if content_length:
                    size_mb = int(content_length) / (1024 * 1024)
                    if size_mb > self.config['download_settings']['max_file_size_mb']:
                        self.logger.warning(f"File too large: {size_mb:.1f}MB > {self.config['download_settings']['max_file_size_mb']}MB")
                        return False

                # Download file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Record successful download
                self.downloaded_files[file_hash] = {
                    'url': url,
                    'filename': new_filename,
                    'source': source_name,
                    'download_date': datetime.now().isoformat(),
                    'original_filename': filename
                }

                self.logger.info(f"Successfully downloaded: {new_filename}")
                return True

            except Exception as e:
                self.logger.warning(f"Download attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.config['download_settings']['retry_attempts'] - 1:
                    time.sleep(self.config['download_settings']['retry_delay_seconds'])

        self.logger.error(f"Failed to download after {self.config['download_settings']['retry_attempts']} attempts: {filename}")
        return False

    def send_notification(self, message: str, new_files: List[str]):
        """Send notifications about new files."""
        notifications = self.config['notifications']

        # Console notification
        if notifications['console']['enabled']:
            print(f"\n🔔 {message}")
            for file in new_files:
                print(f"   📄 {file}")

        # Email notification
        if notifications['email']['enabled'] and SMTP_AVAILABLE:
            self._send_email_notification(message, new_files)

        # Slack notification
        if notifications['slack']['enabled'] and SLACK_AVAILABLE:
            self._send_slack_notification(message, new_files)

    def _send_email_notification(self, message: str, new_files: List[str]):
        """Send email notification."""
        try:
            email_config = self.config['notifications']['email']

            msg = MIMEMultipart()
            msg['From'] = email_config['username']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = f"Data Hunter: New Property Lists Discovered"

            body = f"{message}\n\nNew files:\n"
            for file in new_files:
                body += f"• {file}\n"

            body += f"\nDiscovered at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            text = msg.as_string()
            server.sendmail(email_config['username'], email_config['to_emails'], text)
            server.quit()

            self.logger.info("Email notification sent successfully")

        except Exception as e:
            self.logger.error(f"Failed to send email notification: {str(e)}")

    def _send_slack_notification(self, message: str, new_files: List[str]):
        """Send Slack notification."""
        try:
            webhook_url = self.config['notifications']['slack']['webhook_url']

            slack_message = {
                "text": f"🔔 Data Hunter Alert: {message}",
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "title": "New Files",
                                "value": "\n".join(f"• {file}" for file in new_files),
                                "short": False
                            }
                        ]
                    }
                ]
            }

            response = requests.post(webhook_url, json=slack_message)
            response.raise_for_status()

            self.logger.info("Slack notification sent successfully")

        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {str(e)}")

    def suggest_pipeline_processing(self, new_files: List[str]):
        """Suggest pipeline processing for new files."""
        if not new_files:
            return

        suggestion_log = []
        suggestion_log.append("🚀 PIPELINE PROCESSING SUGGESTIONS")
        suggestion_log.append("=" * 50)

        for file in new_files:
            file_path = self.input_dir / file
            if file_path.exists():
                # Determine processing script based on file source
                if 'miami_dade' in file.lower():
                    script = 'miami_dade_pipeline.py'
                elif 'broward' in file.lower():
                    script = 'broward_pipeline.py'
                elif 'palm_beach' in file.lower():
                    script = 'palm_beach_pipeline.py'
                else:
                    script = 'universal_pipeline.py'

                suggestion_log.append(f"File: {file}")
                suggestion_log.append(f"  Suggested command: python {script} --input {file_path}")
                suggestion_log.append(f"  Alternative: python unified_scraper.py --pdf {file_path}")
                suggestion_log.append("")

        # Log suggestions
        suggestion_text = "\n".join(suggestion_log)
        self.logger.info(f"Pipeline processing suggestions:\n{suggestion_text}")

        # Save suggestions to file
        suggestions_file = self.logs_dir / f"processing_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(suggestions_file, 'w') as f:
            f.write(suggestion_text)

    def run_discovery(self) -> List[str]:
        """Run discovery process for all enabled sources."""
        self.logger.info("Starting automated discovery run...")
        new_files = []

        for source in self.config['sources']:
            if not source['enabled']:
                continue

            try:
                # Discover files
                found_files = self.discover_files(source)

                # Download new files
                for url, filename in found_files:
                    if self.download_file(url, filename, source['name']):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        name_parts = Path(filename).stem, timestamp, source['name'].lower().replace('-', '_')
                        extension = Path(filename).suffix
                        new_filename = f"{'_'.join(name_parts)}{extension}"
                        new_files.append(new_filename)

            except Exception as e:
                self.logger.error(f"Error processing source {source['name']}: {str(e)}")

        # Save download records
        self._save_downloaded_files()

        # Send notifications if new files found
        if new_files:
            message = f"Discovered {len(new_files)} new property list(s)"
            self.send_notification(message, new_files)
            self.suggest_pipeline_processing(new_files)
        else:
            self.logger.info("No new files discovered")

        self.logger.info(f"Discovery run completed. New files: {len(new_files)}")
        return new_files

    def setup_scheduler(self):
        """Set up automated scheduling."""
        if not self.config['schedule']['enabled']:
            self.logger.info("Scheduling disabled in config")
            return

        schedule_time = self.config['schedule']['time']
        schedule.every().day.at(schedule_time).do(self.run_discovery)

        self.logger.info(f"Scheduled daily discovery at {schedule_time}")

        # Keep scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Data Hunter - Automated Property List Discovery')
    parser.add_argument('--run-once', action='store_true', help='Run discovery once and exit')
    parser.add_argument('--schedule', action='store_true', help='Run with scheduler')
    parser.add_argument('--config', help='Path to config file')

    args = parser.parse_args()

    hunter = DataHunter(config_path=args.config)

    if args.run_once:
        hunter.run_discovery()
    elif args.schedule:
        hunter.setup_scheduler()
    else:
        print("Data Hunter - Automated Property List Discovery")
        print("Usage:")
        print("  --run-once    Run discovery once and exit")
        print("  --schedule    Run with scheduler")
        print("  --config      Specify config file path")

if __name__ == "__main__":
    main()
