"""
Configuration and schema loader for the unified scraping framework.
Handles loading and validation of scraping configurations from JSON/YAML files.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Union
from dataclasses import dataclass


@dataclass
class ScrapingConfig:
    """Configuration for scraping operations."""
    name: str
    description: str
    base_url: str
    listing_phase: Dict[str, Any]
    detail_phase: Dict[str, Any]
    pagination: Dict[str, Any]
    data_extraction: Dict[str, Any]
    output: Dict[str, Any]
    options: Dict[str, Any]


class ConfigLoader:
    """Loads and validates scraping configurations."""

    def __init__(self, config_dir: str = "config"):
        """Initialize with configuration directory."""
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

    def load_config(self, config_path: Union[str, Path]) -> ScrapingConfig:
        """Load configuration from file."""
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Load based on file extension
        if config_path.suffix.lower() == '.yaml' or config_path.suffix.lower() == '.yml':
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")

        # Validate and create config object
        return self._validate_config(config_data)

    def save_config(self, config: ScrapingConfig, config_path: Union[str, Path]) -> None:
        """Save configuration to file."""
        config_path = Path(config_path)

        # Convert to dict
        config_dict = self._config_to_dict(config)

        # Save based on file extension
        if config_path.suffix.lower() == '.yaml' or config_path.suffix.lower() == '.yml':
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")

    def list_configs(self) -> List[str]:
        """List available configuration files."""
        configs = []
        for ext in ['*.json', '*.yaml', '*.yml']:
            configs.extend([f.stem for f in self.config_dir.glob(ext)])
        return sorted(set(configs))

    def generate_sample_config(self, name: str, base_url: str) -> ScrapingConfig:
        """Generate a sample configuration for a directory."""
        return ScrapingConfig(
            name=name,
            description=f"Scraping configuration for {name}",
            base_url=base_url,
            listing_phase={
                "enabled": True,
                "start_url": base_url,
                "list_selector": ".directory-item, .listing-item, .member-item",
                "link_selector": "a[href]",
                "link_attribute": "href",
                "max_pages": 10,
                "delay": 2.0
            },
            detail_phase={
                "enabled": True,
                "delay": 1.0,
                "timeout": 30,
                "retry_count": 3
            },
            pagination={
                "enabled": True,
                "type": "auto",  # auto-detect pagination type
                "next_button": ".next, .pagination-next, [aria-label*='next']",
                "page_numbers": ".pagination a, .page-numbers a",
                "load_more": ".load-more, .show-more, .view-more",
                "infinite_scroll": False,
                "max_pages": 50,
                "delay": 2.0
            },
            data_extraction={
                "selectors": {
                    "name": {
                        "css": ["h1", "h2", ".name", ".title", ".attorney-name"],
                        "required": True
                    },
                    "email": {
                        "css": ["a[href^='mailto:']"],
                        "attribute": "href",
                        "pattern": r"mailto:(.+)",
                        "required": False
                    },
                    "phone": {
                        "css": [".phone", ".tel", "a[href^='tel:']"],
                        "patterns": [
                            r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
                            r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}"
                        ],
                        "required": False
                    },
                    "address": {
                        "css": [".address", ".location", ".office-address"],
                        "required": False
                    },
                    "website": {
                        "css": ["a[href^='http']"],
                        "attribute": "href",
                        "required": False
                    },
                    "practice_areas": {
                        "css": [".practice-areas", ".specialties", ".areas-of-practice"],
                        "multiple": True,
                        "required": False
                    }
                },
                "structured_data": {
                    "json_ld": True,
                    "microdata": True,
                    "rdfa": False
                },
                "contact_extraction": {
                    "enabled": True,
                    "email_domains": [],
                    "phone_formats": ["US"]
                },
                "required_fields": ["name"]
            },
            output={
                "format": "csv",
                "filename": f"{name.lower().replace(' ', '_')}_directory.csv",
                "google_sheets": {
                    "enabled": False,
                    "spreadsheet_id": "",
                    "worksheet_name": "Directory Data"
                },
                "include_metadata": True,
                "include_screenshots": False
            },
            options={
                "headless": True,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "viewport": {"width": 1920, "height": 1080},
                "wait_strategy": "smart",
                "screenshot_on_error": True,
                "respect_robots_txt": True,
                "rate_limit": 1.0,
                "concurrent_requests": 1,
                "timeout": 30
            }
        )

    def _validate_config(self, config_data: Dict[str, Any]) -> ScrapingConfig:
        """Validate configuration data and create ScrapingConfig object."""
        required_fields = [
            'name', 'description', 'base_url', 'listing_phase',
            'detail_phase', 'pagination', 'data_extraction', 'output', 'options'
        ]

        for field in required_fields:
            if field not in config_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate listing phase
        if not isinstance(config_data['listing_phase'], dict):
            raise ValueError("listing_phase must be a dictionary")

        # Validate pagination
        if not isinstance(config_data['pagination'], dict):
            raise ValueError("pagination must be a dictionary")

        # Validate data extraction
        if not isinstance(config_data['data_extraction'], dict):
            raise ValueError("data_extraction must be a dictionary")

        if 'selectors' not in config_data['data_extraction']:
            raise ValueError("data_extraction must contain 'selectors'")

        return ScrapingConfig(**config_data)

    def _config_to_dict(self, config: ScrapingConfig) -> Dict[str, Any]:
        """Convert ScrapingConfig to dictionary."""
        return {
            'name': config.name,
            'description': config.description,
            'base_url': config.base_url,
            'listing_phase': config.listing_phase,
            'detail_phase': config.detail_phase,
            'pagination': config.pagination,
            'data_extraction': config.data_extraction,
            'output': config.output,
            'options': config.options
        }

    def validate_config(self, config: ScrapingConfig) -> Dict[str, Any]:
        """Validate a configuration and return validation results."""
        errors = []
        warnings = []

        # Validate basic fields
        if not config.name:
            errors.append("Configuration name is required")
        if not config.base_url:
            errors.append("Base URL is required")

        # Validate URL format
        if config.base_url and not config.base_url.startswith(('http://', 'https://')):
            errors.append("Base URL must start with http:// or https://")

        # Validate listing phase
        if config.listing_phase.get('enabled', True):
            if not config.listing_phase.get('list_selector'):
                errors.append("List selector is required when listing phase is enabled")
            if not config.listing_phase.get('link_selector'):
                errors.append("Link selector is required when listing phase is enabled")

        # Validate detail phase
        if config.detail_phase.get('enabled', True):
            data_fields = config.data_extraction.get('fields', {})
            if not data_fields:
                warnings.append("No data fields configured for extraction")

        # Validate pagination
        pagination_type = config.pagination.get('type', 'none')
        if pagination_type != 'none':
            if pagination_type == 'next_button' and not config.pagination.get('next_selector'):
                errors.append("Next button selector is required for next_button pagination")
            elif pagination_type == 'load_more' and not config.pagination.get('load_more_selector'):
                errors.append("Load more selector is required for load_more pagination")

        # Validate output configuration
        if not config.output.get('file_path'):
            warnings.append("No output file path specified")

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def validate_selectors(self, selectors: Dict[str, Any]) -> List[str]:
        """Validate CSS selectors and return any issues."""
        issues = []

        for field_name, selector_config in selectors.items():
            if not isinstance(selector_config, dict):
                issues.append(f"Selector for '{field_name}' must be a dictionary")
                continue

            if 'css' not in selector_config and 'xpath' not in selector_config:
                issues.append(f"Selector for '{field_name}' must have 'css' or 'xpath'")

            if 'css' in selector_config:
                css_selectors = selector_config['css']
                if not isinstance(css_selectors, list):
                    issues.append(f"CSS selectors for '{field_name}' must be a list")

        return issues

    def get_selector_priority(self, selector_config: Dict[str, Any]) -> List[str]:
        """Get CSS selectors in priority order."""
        css_selectors = selector_config.get('css', [])
        if isinstance(css_selectors, str):
            return [css_selectors]
        return list(css_selectors) if css_selectors else []

    def is_required_field(self, field_name: str, config: ScrapingConfig) -> bool:
        """Check if a field is required."""
        selector_config = config.data_extraction.get('selectors', {}).get(field_name, {})
        required = selector_config.get('required', False)
        return bool(required)

    def get_extraction_patterns(self, field_name: str, config: ScrapingConfig) -> List[str]:
        """Get regex patterns for field extraction."""
        selector_config = config.data_extraction.get('selectors', {}).get(field_name, {})
        patterns = selector_config.get('patterns', [])
        if isinstance(patterns, str):
            return [patterns]
        return list(patterns) if patterns else []
