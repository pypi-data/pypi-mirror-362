# Universal Recon - Bar Directory Reconnaissance Tool

[![PyPI version](https://img.shields.io/pypi/v/bar-directory-recon.svg)](https://pypi.org/project/bar-directory-recon/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-33%20passed-green.svg)](https://github.com/samiat-quadir/bar-directory-recon/actions)

## Overview

Universal Recon is a comprehensive bar directory reconnaissance and automation tool designed for legal professional data extraction. It provides a modular plugin system for extracting, validating, and analyzing data from legal bar directories and professional websites.

---

## Key Features

- **Plugin-Based Architecture**: Modular system with specialized extractors for different data types
- **Social Media Detection**: Automated discovery of LinkedIn, Twitter, Facebook, and Instagram profiles
- **Firm Data Extraction**: Intelligent parsing of law firm information and contact details
- **ML-Powered Classification**: Machine learning-based content labeling and categorization
- **Validation Framework**: Comprehensive data validation and quality assessment tools
- **Analytics Suite**: Risk assessment, trend analysis, and reporting capabilities
- **Cross-Platform Support**: Works on Windows and Linux with automated environment detection

---

## Getting Started

### Requirements

- Windows 10/11, PowerShell 5.1+
- OneDrive installed and configured
- Python 3.11+
- Admin rights for scheduled tasks

### Virtual Environment Setup

- Use `activate_venv.bat` (CMD) or `ActivateVenv.ps1` (PowerShell) to activate the Python environment.
- For full dev setup: `RunDevelopment.bat` or `StartDevPowerShell.bat`.
- To fix or recreate the venv: `fix_venv_activation.bat` and `InstallDependencies.bat`.

### Environment Variables

- `.env.work` and `.env.asus` are used for device-specific configs.
- `env_loader.py` auto-detects and loads the correct file.
- Only one `.env` is loaded per execution.

### First-Time Setup

1. Activate the venv and install dependencies.
2. Run `RunOneDriveAutomation.bat` and follow the menu.
3. For preview, use option 7; for full automation, use option 1.

---

## Automation Scripts

- **OneDriveAutomation.ps1**: Main entry for all tasks.
- **auto_git_commit.py**: Auto-commits and pushes to GitHub.
- **git_commit_and_notify.py**: Commits, pushes, and sends notifications.
- **notifier.py**: Handles all email notifications (HTML supported).
- **motion_task_creator.py**: Local integration with Motion App via Flask API.
- **health_check.py**: Verifies environment and variables.
- **log_rotator.py**: Archives old logs.

---

## Best Practices

- Always use `env_loader.py` for environment detection.
- Maintain only one version of each core script.
- Keep `.env` files in the project root.
- Log all actions for traceability.
- Deprecated: `.env` (generic), `token.pickle`, device-specific notifier scripts.

---

## Project Roadmap (Excerpt)

- [x] Unified .env management and loader
- [x] Centralized logging
- [x] AI-powered task automation (Motion App integration)
- [x] Git automation and notification
- [ ] Optional: Further AI enhancements and advanced analytics

---

## Contributors & Contact

- For setup help, see the archived Setup Instructions and Roadmap in `docs/archive/`.
- For issues, open a ticket or contact the maintainer.

---

## Data Hunter - Automated Discovery Module

The Data Hunter module provides automated discovery and download of property lists and inspection documents from municipal websites.

### Key Features

- **Automated Web Scanning**: Periodically crawls configured municipal websites
- **Smart File Detection**: Uses regex patterns to identify relevant documents
- **Intelligent Download Management**: Prevents duplicate downloads and manages file sizes
- **Multi-Source Support**: Configurable sources for easy expansion
- **Notification System**: Email, Slack, and console notifications for new discoveries
- **Pipeline Integration**: Suggests processing commands for new files

### Quick Start

```bash
# Test the system
python test_data_hunter.py

# Run discovery once
python src/data_hunter.py --run-once

# Start scheduled discovery (daily)
python src/data_hunter.py --schedule

# Windows users - use the batch script
RunDataHunter.bat
```

### Configuration

Edit `config/data_hunter_config.json` to:

- Add new municipal data sources
- Configure notification preferences
- Adjust download settings and file patterns
- Set scheduling preferences

### Supported Sources

Currently configured for:

- **Miami-Dade County**: Property appraiser and inspection lists
- **Broward County**: Building safety inspection programs
- **Palm Beach County**: Recertification and property lists

### Adding New Sources

To add a new city/county source:

```json
{
  "name": "New-City",
  "url": "https://newcity.gov/inspections",
  "patterns": [
    ".*inspection.*\\.pdf",
    ".*property.*list.*\\.pdf"
  ],
  "enabled": true,
  "check_frequency_hours": 24
}
```

### Notification Setup

**Email Notifications:**

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "username": "your-email@gmail.com",
  "password": "your-app-password",
  "to_emails": ["recipient@example.com"]
}
```

**Slack Notifications:**

```json
"slack": {
  "enabled": true,
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
}
```

### File Processing

Downloaded files are saved to `input/` with timestamped names:

```
inspection_list_20250709_120000_miami_dade.pdf
property_safety_20250709_120000_broward.xlsx
```

Process new files using existing pipeline scripts:

```bash
python unified_scraper.py --pdf input/filename.pdf
python final_hallandale_pipeline.py  # Adapt for other cities
```

---

*This README consolidates all previous documentation, setup guides, and roadmaps. For historical docs, see `docs/archive/`.*
