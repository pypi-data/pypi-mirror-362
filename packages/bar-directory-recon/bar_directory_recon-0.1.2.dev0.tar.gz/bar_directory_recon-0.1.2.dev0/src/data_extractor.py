#!/usr/bin/env python3
"""
Data Extractor
Unified data extraction from web pages using configurable selectors and patterns.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class DataExtractor:
    """Unified data extraction with configurable selectors and patterns."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize data extractor with configuration."""
        self.config = config
        self.extraction_rules = config.get('extraction_rules', {})
        self.contact_patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
            'website': re.compile(
                r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*|'
                r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*'
            )
        }

    def extract_from_page(self, driver_manager: Any) -> List[Dict[str, Any]]:
        """Extract all data from current page using configured rules."""
        try:
            page_source = driver_manager.get_page_source()
            soup = BeautifulSoup(page_source, 'html.parser')

            # Get listing container selector
            container_selector = self.extraction_rules.get('listing_container', 'body')
            containers = soup.select(container_selector)

            if not containers:
                logger.warning(f"No containers found with selector: {container_selector}")
                return []

            extracted_data = []

            for container in containers:
                data = self.extract_from_element(container)
                if data and self._is_valid_record(data):
                    extracted_data.append(data)

            logger.info(f"Extracted {len(extracted_data)} records from page")
            return extracted_data

        except Exception as e:
            logger.error(f"Error extracting data from page: {e}")
            return []

    def extract_from_element(self, element: Tag) -> Dict[str, Any]:
        """Extract data from a single element using configured rules."""
        data = {}

        try:
            # Extract each field defined in extraction rules
            for field_name, field_config in self.extraction_rules.get('fields', {}).items():
                value = self._extract_field(element, field_config)
                if value:
                    data[field_name] = value

            # Extract contact information from all text
            element_text = element.get_text()
            contact_info = self.extract_contact_info(element_text)
            data.update(contact_info)

            # Add source information
            data['extraction_timestamp'] = self._get_timestamp()
            data['source_url'] = self.config.get('current_url', 'unknown')

            return data

        except Exception as e:
            logger.error(f"Error extracting data from element: {e}")
            return {}

    def _extract_field(self, element: Tag, field_config: Dict[str, Any]) -> Optional[str]:
        """Extract a specific field using its configuration."""
        try:
            extraction_type = field_config.get('type', 'text')
            selectors = field_config.get('selectors', [])

            if not selectors:
                return None

            # Try each selector until one works
            for selector in selectors:
                found_element = element.select_one(selector)
                if found_element:
                    if extraction_type == 'text':
                        value = found_element.get_text(strip=True)
                    elif extraction_type == 'attribute':
                        attr_name = field_config.get('attribute', 'href')
                        attr_value = found_element.get(attr_name, '')
                        value = str(attr_value).strip() if attr_value else ''
                    elif extraction_type == 'pattern':
                        text = found_element.get_text()
                        pattern = field_config.get('pattern', '')
                        match = re.search(pattern, text)
                        value = match.group(1) if match else ''
                    else:
                        value = found_element.get_text(strip=True)

                    if value:
                        # Apply transformations
                        value = self._apply_transformations(value, field_config.get('transformations', []))
                        return value

            return None

        except Exception as e:
            logger.error(f"Error extracting field {field_config}: {e}")
            return None

    def _apply_transformations(self, value: str, transformations: List[str]) -> str:
        """Apply transformations to extracted value."""
        for transform in transformations:
            if transform == 'strip':
                value = value.strip()
            elif transform == 'lower':
                value = value.lower()
            elif transform == 'upper':
                value = value.upper()
            elif transform == 'title':
                value = value.title()
            elif transform == 'clean_whitespace':
                value = ' '.join(value.split())
            elif transform.startswith('replace:'):
                # Format: replace:old_text:new_text
                parts = transform.split(':', 2)
                if len(parts) == 3:
                    value = value.replace(parts[1], parts[2])
            elif transform.startswith('regex:'):
                # Format: regex:pattern:replacement
                parts = transform.split(':', 2)
                if len(parts) == 3:
                    value = re.sub(parts[1], parts[2], value)

        return value

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using regex patterns."""
        contact_info = {}

        # Extract email
        email_match = self.contact_patterns['email'].search(text)
        contact_info['email'] = email_match.group(0) if email_match else ''

        # Extract phone
        phone_match = self.contact_patterns['phone'].search(text)
        if phone_match:
            # Format phone number
            phone = f"({phone_match.group(1)}) {phone_match.group(2)}-{phone_match.group(3)}"
            contact_info['phone'] = phone
        else:
            contact_info['phone'] = ''

        # Extract website
        website_match = self.contact_patterns['website'].search(text)
        if website_match:
            website = website_match.group(0)
            if not website.startswith('http'):
                website = 'https://' + website
            contact_info['website'] = website
        else:
            contact_info['website'] = ''

        return contact_info

    def extract_listing_urls(self, driver_manager: Any) -> List[str]:
        """Extract URLs for detail page scraping (two-phase approach)."""
        try:
            page_source = driver_manager.get_page_source()
            soup = BeautifulSoup(page_source, 'html.parser')

            urls = []
            url_selectors = self.extraction_rules.get('detail_url_selectors', [])

            for selector in url_selectors:
                elements = soup.select(selector)
                for element in elements:
                    href_attr = element.get('href', '')
                    href = str(href_attr).strip() if href_attr else ''
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            base_url = self.config.get('base_url', '')
                            href = base_url.rstrip('/') + href
                        elif not href.startswith('http'):
                            base_url = self.config.get('base_url', '')
                            href = base_url.rstrip('/') + '/' + href

                        urls.append(href)

            # Remove duplicates while preserving order
            unique_urls = list(dict.fromkeys(urls))
            logger.info(f"Extracted {len(unique_urls)} unique detail URLs")
            return unique_urls

        except Exception as e:
            logger.error(f"Error extracting listing URLs: {e}")
            return []

    def extract_with_selenium(self, driver_manager: Any, selectors: List[str]) -> List[Dict[str, Any]]:
        """Extract data using Selenium for dynamic content."""
        try:
            driver = driver_manager.driver
            extracted_data = []

            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    logger.info(f"Found {len(elements)} elements with selector: {selector}")

                    for element in elements:
                        try:
                            # Get element as BeautifulSoup for consistent processing
                            element_html = element.get_attribute('outerHTML')
                            soup_element = BeautifulSoup(element_html, 'html.parser')

                            data = self.extract_from_element(soup_element)
                            if data and self._is_valid_record(data):
                                extracted_data.append(data)

                        except Exception as e:
                            logger.error(f"Error processing element: {e}")
                            continue

                    if extracted_data:
                        break  # Found data with this selector

                except Exception as e:
                    logger.error(f"Error with selector {selector}: {e}")
                    continue

            logger.info(f"Extracted {len(extracted_data)} records with Selenium")
            return extracted_data

        except Exception as e:
            logger.error(f"Error in Selenium extraction: {e}")
            return []

    def extract_structured_data(self, page_source: str) -> List[Dict[str, Any]]:
        """Extract structured data (JSON-LD, microdata) from page."""
        try:
            soup = BeautifulSoup(page_source, 'html.parser')
            structured_data = []

            # Extract JSON-LD
            json_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_scripts:
                try:
                    import json
                    script_content = getattr(script, 'string', None) or script.get_text()
                    if script_content:
                        data = json.loads(script_content)
                    if isinstance(data, dict):
                        structured_data.append(data)
                    elif isinstance(data, list):
                        structured_data.extend(data)
                except json.JSONDecodeError:
                    continue

            # Extract microdata
            microdata_elements = soup.find_all(attrs={'itemtype': True})
            for element in microdata_elements:
                try:
                    if isinstance(element, Tag):
                        data = self._extract_microdata(element)
                        if data:
                            structured_data.append(data)
                except Exception:
                    continue

            logger.info(f"Extracted {len(structured_data)} structured data items")
            return structured_data

        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            return []

    def _extract_microdata(self, element: Tag) -> Dict[str, Any]:
        """Extract microdata from element."""
        data = {}

        # Get item type
        itemtype = element.get('itemtype', '')
        if itemtype:
            data['@type'] = itemtype

        # Extract properties
        prop_elements = element.find_all(attrs={'itemprop': True})
        for prop_element in prop_elements:
            if isinstance(prop_element, Tag):
                prop_name = prop_element.get('itemprop')
                prop_value = prop_element.get('content') or prop_element.get_text(strip=True)
                if prop_name and prop_value:
                    data[str(prop_name)] = prop_value

        return data

    def _is_valid_record(self, data: Dict[str, Any]) -> bool:
        """Check if extracted record meets minimum requirements."""
        required_fields = self.config.get('required_fields', [])

        if not required_fields:
            # Default validation: must have at least one of name, email, or phone
            return bool(data.get('name') or data.get('email') or data.get('phone'))

        # Check if all required fields are present and non-empty
        for field in required_fields:
            if not data.get(field):
                return False

        return True

    def _get_timestamp(self) -> str:
        """Get current timestamp for records."""
        from datetime import datetime
        return datetime.now().isoformat()

    def clean_extracted_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and deduplicate extracted data."""
        try:
            cleaned_data = []
            seen_records = set()

            for data in data_list:
                # Create a signature for duplicate detection
                signature_fields = ['name', 'email', 'phone', 'business_name']
                signature_values = []

                for field in signature_fields:
                    value = data.get(field, '').strip().lower()
                    if value:
                        signature_values.append(value)

                signature = '|'.join(signature_values)

                if signature and signature not in seen_records:
                    seen_records.add(signature)

                    # Clean individual fields
                    cleaned_record = {}
                    for key, value in data.items():
                        if isinstance(value, str):
                            # Clean whitespace and empty values
                            cleaned_value = ' '.join(value.split()).strip()
                            cleaned_record[key] = cleaned_value if cleaned_value else ''
                        else:
                            cleaned_record[key] = value

                    cleaned_data.append(cleaned_record)

            logger.info(f"Cleaned data: {len(data_list)} -> {len(cleaned_data)} records")
            return cleaned_data

        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            return data_list

    def validate_and_enrich_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and enrich extracted data."""
        try:
            enriched_data = []

            for data in data_list:
                # Validate email format
                email = data.get('email', '')
                if email and not self.contact_patterns['email'].match(email):
                    data['email'] = ''  # Invalid email

                # Standardize phone format
                phone = data.get('phone', '')
                if phone:
                    # Remove all non-digits
                    digits = re.sub(r'\D', '', phone)
                    if len(digits) == 10:
                        data['phone'] = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
                    elif len(digits) == 11 and digits[0] == '1':
                        data['phone'] = f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
                    else:
                        data['phone'] = ''  # Invalid phone

                # Ensure website has protocol
                website = data.get('website', '')
                if website and not website.startswith(('http://', 'https://')):
                    data['website'] = 'https://' + website

                # Add industry and source tags
                data['industry'] = self.config.get('industry', 'unknown')
                data['source'] = self.config.get('source_name', 'unknown')

                enriched_data.append(data)

            logger.info(f"Validated and enriched {len(enriched_data)} records")
            return enriched_data

        except Exception as e:
            logger.error(f"Error validating data: {e}")
            return data_list
