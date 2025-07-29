#!/usr/bin/env python3
"""
Unified Data Schema for Scraping Framework
Defines the standard data structure and field mappings for all scraped data.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UnifiedDataRecord:
    """Unified data record structure for all scraped entities."""

    # Core identification fields
    name: str = ""
    email: str = ""
    phone: str = ""

    # Business information
    company: str = ""
    title: str = ""
    website: str = ""

    # Address information
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    country: str = "US"

    # Professional details
    practice_areas: List[str] = field(default_factory=list)
    specializations: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)

    # Social media and additional contacts
    linkedin_url: str = ""
    facebook_url: str = ""
    twitter_url: str = ""
    other_urls: List[str] = field(default_factory=list)

    # Metadata
    source: str = ""
    source_url: str = ""
    scraped_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    # Quality and validation
    status: str = "active"  # active, inactive, validated, suspect
    validation_score: float = 0.0
    notes: str = ""

    # Custom fields for extensibility
    custom_fields: Dict[str, Any] = field(default_factory=dict)


class SchemaMapper:
    """Maps different data sources to the unified schema."""

    # Standard field mappings for different sources
    FIELD_MAPPINGS = {
        'lawyers': {
            'name': ['name', 'full_name', 'attorney_name', 'lawyer_name'],
            'email': ['email', 'email_address', 'contact_email'],
            'phone': ['phone', 'phone_number', 'contact_phone', 'office_phone'],
            'company': ['firm', 'law_firm', 'company', 'firm_name'],
            'title': ['title', 'position', 'role'],
            'website': ['website', 'firm_website', 'url'],
            'address': ['address', 'full_address', 'office_address'],
            'city': ['city', 'location_city'],
            'state': ['state', 'location_state'],
            'zip_code': ['zip', 'zip_code', 'postal_code'],
            'practice_areas': ['practice_areas', 'specialties', 'areas_of_practice'],
            'certifications': ['certifications', 'bar_admissions', 'licenses']
        },
        'realtors': {
            'name': ['name', 'full_name', 'agent_name', 'realtor_name'],
            'email': ['email', 'email_address', 'contact_email'],
            'phone': ['phone', 'phone_number', 'contact_phone', 'office_phone'],
            'company': ['brokerage', 'company', 'firm', 'agency'],
            'title': ['title', 'position', 'designation'],
            'website': ['website', 'personal_website', 'url'],
            'address': ['address', 'office_address'],
            'city': ['city', 'office_city'],
            'state': ['state', 'office_state'],
            'zip_code': ['zip', 'zip_code', 'postal_code'],
            'specializations': ['specializations', 'property_types', 'market_areas'],
            'certifications': ['certifications', 'designations', 'licenses']
        },
        'contractors': {
            'name': ['name', 'full_name', 'contractor_name', 'business_owner'],
            'email': ['email', 'email_address', 'contact_email'],
            'phone': ['phone', 'phone_number', 'contact_phone', 'business_phone'],
            'company': ['business_name', 'company', 'contractor_company'],
            'title': ['title', 'position', 'role'],
            'website': ['website', 'business_website', 'url'],
            'address': ['address', 'business_address'],
            'city': ['city', 'service_city'],
            'state': ['state', 'service_state'],
            'zip_code': ['zip', 'zip_code', 'postal_code'],
            'specializations': ['services', 'specializations', 'service_types'],
            'certifications': ['certifications', 'licenses', 'insurance']
        }
    }

    # CSV/Excel export column order and headers
    EXPORT_SCHEMA = {
        'standard': [
            ('name', 'Full Name'),
            ('email', 'Email Address'),
            ('phone', 'Phone Number'),
            ('company', 'Company/Firm'),
            ('title', 'Title/Position'),
            ('website', 'Website'),
            ('address', 'Street Address'),
            ('city', 'City'),
            ('state', 'State'),
            ('zip_code', 'ZIP Code'),
            ('source', 'Data Source'),
            ('scraped_at', 'Date Scraped'),
            ('status', 'Status')
        ],
        'detailed': [
            ('name', 'Full Name'),
            ('email', 'Email Address'),
            ('phone', 'Phone Number'),
            ('company', 'Company/Firm'),
            ('title', 'Title/Position'),
            ('website', 'Website'),
            ('address', 'Street Address'),
            ('city', 'City'),
            ('state', 'State'),
            ('zip_code', 'ZIP Code'),
            ('country', 'Country'),
            ('practice_areas', 'Practice Areas'),
            ('specializations', 'Specializations'),
            ('certifications', 'Certifications'),
            ('linkedin_url', 'LinkedIn'),
            ('source', 'Data Source'),
            ('source_url', 'Source URL'),
            ('scraped_at', 'Date Scraped'),
            ('last_updated', 'Last Updated'),
            ('status', 'Status'),
            ('validation_score', 'Validation Score'),
            ('notes', 'Notes')
        ]
    }

    def __init__(self, source_type: str = 'standard'):
        """Initialize schema mapper for a specific source type."""
        self.source_type = source_type
        self.field_mapping = self.FIELD_MAPPINGS.get(source_type, {})

    def map_to_unified(self, raw_data: Dict[str, Any]) -> UnifiedDataRecord:
        """Map raw scraped data to unified schema."""
        unified_data = {}

        # Map each field using the source-specific mapping
        for unified_field, possible_sources in self.field_mapping.items():
            value = None

            # Try each possible source field
            for source_field in possible_sources:
                if source_field in raw_data and raw_data[source_field]:
                    value = raw_data[source_field]
                    break

            if value is not None:
                unified_data[unified_field] = value

        # Handle special fields
        if 'scraped_at' not in unified_data:
            unified_data['scraped_at'] = datetime.now()

        if 'source' not in unified_data:
            unified_data['source'] = self.source_type

        # Store any unmapped fields in custom_fields
        custom_fields = {}
        mapped_source_fields = set()
        for field_list in self.field_mapping.values():
            mapped_source_fields.update(field_list)

        for key, value in raw_data.items():
            if key not in mapped_source_fields and value:
                custom_fields[key] = value

        if custom_fields:
            unified_data['custom_fields'] = custom_fields

        return UnifiedDataRecord(**unified_data)

    def to_export_dict(self, record: UnifiedDataRecord, schema: str = 'standard') -> Dict[str, str]:
        """Convert unified record to export dictionary with proper column headers."""
        export_schema = self.EXPORT_SCHEMA.get(schema, self.EXPORT_SCHEMA['standard'])
        export_data = {}

        for field_name, column_header in export_schema:
            value = getattr(record, field_name, '')

            # Handle special formatting
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, list):
                value = ', '.join(str(item) for item in value)
            elif value is None:
                value = ''

            export_data[column_header] = str(value)

        return export_data

    def get_export_headers(self, schema: str = 'standard') -> List[str]:
        """Get ordered list of export column headers."""
        export_schema = self.EXPORT_SCHEMA.get(schema, self.EXPORT_SCHEMA['standard'])
        return [header for _, header in export_schema]

    def validate_record(self, record: UnifiedDataRecord) -> Dict[str, Any]:
        """Validate a unified data record and return validation results."""
        issues = []
        score = 100.0

        # Required field validation
        if not record.name:
            issues.append("Missing name")
            score -= 30

        # Contact information validation
        if not record.email and not record.phone:
            issues.append("Missing both email and phone")
            score -= 40

        # Email format validation
        if record.email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, record.email):
                issues.append("Invalid email format")
                score -= 15

        # Phone format validation
        if record.phone:
            # Remove common formatting characters
            clean_phone = re.sub(r'[^\d]', '', record.phone)
            if len(clean_phone) < 10:
                issues.append("Phone number too short")
                score -= 10

        # Address validation
        if record.address and not (record.city and record.state):
            issues.append("Incomplete address information")
            score -= 10

        # Business information validation
        if not record.company:
            issues.append("Missing company/firm information")
            score -= 5

        return {
            'valid': len(issues) == 0,
            'score': max(0, score),
            'issues': issues
        }

    def map_data_to_unified_schema(self, raw_data_list: List[Dict[str, Any]],
                                  source_type: Optional[str] = None,
                                  source_name: Optional[str] = None) -> List[UnifiedDataRecord]:
        """Map a list of raw data dictionaries to unified schema records."""
        if source_type:
            self.source_type = source_type
            self.field_mapping = self.FIELD_MAPPINGS.get(source_type, {})

        unified_records = []
        for raw_data in raw_data_list:
            # Add source information
            if source_name and 'source' not in raw_data:
                raw_data['source'] = source_name

            # Map to unified schema
            unified_record = self.map_to_unified(raw_data)
            unified_records.append(unified_record)

        return unified_records

    def create_export_dataframe(self, unified_records: List[UnifiedDataRecord],
                               export_type: str = 'standard') -> Any:
        """Create a pandas DataFrame from unified records with proper column order."""
        import pandas as pd

        # Convert records to export dictionaries
        export_data = []
        for record in unified_records:
            export_dict = self.to_export_dict(record, export_type)
            export_data.append(export_dict)

        # Create DataFrame with proper column order
        df = pd.DataFrame(export_data)

        # Ensure columns are in the correct order
        headers = self.get_export_headers(export_type)
        missing_cols = [col for col in headers if col not in df.columns]
        for col in missing_cols:
            df[col] = ''

        # Reorder columns
        df = df[headers]

        return df

    def deduplicate_records(self, records: List[UnifiedDataRecord],
                           dedup_fields: Optional[List[str]] = None) -> List[UnifiedDataRecord]:
        """Remove duplicate records based on specified fields."""
        if dedup_fields is None:
            dedup_fields = ['email', 'phone']

        seen = set()
        unique_records = []

        for record in records:
            # Create a tuple of dedup field values
            dedup_values = []
            for field in dedup_fields:
                value = getattr(record, field, '')
                if value:
                    # Normalize for comparison
                    if field == 'email':
                        value = value.lower().strip()
                    elif field == 'phone':
                        import re
                        value = re.sub(r'[^\d]', '', value)
                    dedup_values.append(value)

            # Only deduplicate if we have at least one dedup field value
            if dedup_values:
                dedup_key = tuple(dedup_values)
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    unique_records.append(record)
            else:
                # Keep records without dedup field values
                unique_records.append(record)

        return unique_records

def create_unified_config_template() -> Dict[str, Any]:
    """Create template for unified configuration with all options."""
    return {
        "name": "example_directory",
        "description": "Example directory scraping configuration",
        "base_url": "https://example.com",

        # Data schema and mapping
        "data_schema": {
            "source_type": "standard",  # lawyers, realtors, contractors, standard
            "export_format": "standard",  # standard, detailed
            "validation_enabled": True,
            "deduplication_enabled": True,
            "deduplication_fields": ["email", "phone"]
        },

        # Scraping configuration (existing)
        "scraping": {
            "strategy": "two_phase",
            "max_pages": 10,
            "delay_between_pages": 2,
            "list_page": {
                "url_pattern": "https://example.com/page/{page}",
                "listing_selector": ".directory-item",
                "link_selector": "a.profile-link"
            },
            "detail_page": {
                "data_fields": {
                    "name": ".profile-name",
                    "email": ".contact-email",
                    "phone": ".contact-phone",
                    "company": ".company-name",
                    "address": ".address-full"
                }
            }
        },

        # WebDriver configuration
        "webdriver": {
            "browser": "chrome",
            "headless": True,
            "timeout": 30,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },

        # Pagination configuration
        "pagination": {
            "type": "next_button",
            "next_selector": ".next-page",
            "max_retries": 3
        },

        # Output configuration
        "output": {
            "format": "json",
            "file_path": "output/scraped_data.json",
            "csv_export": {
                "enabled": True,
                "file_path": "output/scraped_data.csv",
                "schema": "standard"
            },
            "google_sheets": {
                "enabled": False,
                "sheet_id": "",
                "worksheet_name": "Scraped Data",
                "credentials_path": "",
                "schema": "standard"
            }
        },

        # Notification configuration
        "notifications": {
            "enabled": False,
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": []
            },
            "sms": {
                "enabled": False,
                "twilio_account_sid": "",
                "twilio_auth_token": "",
                "from_number": "",
                "to_numbers": []
            },
            "slack": {
                "enabled": False,
                "webhook_url": ""
            }
        },

        # Logging configuration
        "logging": {
            "level": "INFO",
            "quiet_mode": False,
            "verbose_logging": False,
            "log_file": "logs/scraping.log",
            "enable_screenshots": True
        },

        # Security configuration
        "security": {
            "use_environment_variables": True,
            "credential_fields": [
                "output.google_sheets.credentials_path",
                "notifications.email.sender_password",
                "notifications.sms.twilio_auth_token",
                "notifications.slack.webhook_url"
            ]
        }
    }
