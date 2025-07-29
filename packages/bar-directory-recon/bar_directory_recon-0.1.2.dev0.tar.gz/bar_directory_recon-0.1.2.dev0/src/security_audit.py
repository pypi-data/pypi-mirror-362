#!/usr/bin/env python3
"""
Security and Configuration Audit Module
Scans for hardcoded credentials and manages secure configuration.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class SecurityAuditor:
    """Audits code and configuration for security issues."""

    # Patterns for detecting potential credentials
    CREDENTIAL_PATTERNS = {
        'api_key': [
            r'api[_-]?key\s*[=:]\s*["\']([^"\']+)["\']',
            r'apikey\s*[=:]\s*["\']([^"\']+)["\']',
        ],
        'password': [
            r'password\s*[=:]\s*["\']([^"\']+)["\']',
            r'passwd\s*[=:]\s*["\']([^"\']+)["\']',
            r'pwd\s*[=:]\s*["\']([^"\']+)["\']',
        ],
        'secret': [
            r'secret\s*[=:]\s*["\']([^"\']+)["\']',
            r'secret_key\s*[=:]\s*["\']([^"\']+)["\']',
            r'client_secret\s*[=:]\s*["\']([^"\']+)["\']',
        ],
        'token': [
            r'token\s*[=:]\s*["\']([^"\']+)["\']',
            r'access_token\s*[=:]\s*["\']([^"\']+)["\']',
            r'auth_token\s*[=:]\s*["\']([^"\']+)["\']',
        ],
        'url_with_credentials': [
            r'(https?://[^:]+:[^@]+@[^/]+)',
        ],
        'hardcoded_paths': [
            r'["\']([C-Z]:\\\\[^"\']+)["\']',  # Windows absolute paths
            r'["\'](/[^"\']+/[^"\']+)["\']',   # Unix absolute paths
        ]
    }

    # Files to ignore during security audit
    IGNORE_PATTERNS = [
        r'.*\.git.*',
        r'.*__pycache__.*',
        r'.*\.pyc$',
        r'.*\.log$',
        r'.*\.md$',
        r'.*test.*\.py$',
        r'.*example.*\.py$',
        r'.*demo.*\.py$',
    ]

    def __init__(self, project_root: str = "."):
        """Initialize security auditor."""
        self.project_root = Path(project_root)
        self.findings: List[Dict[str, Any]] = []

    def scan_project(self, exclude_dirs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Scan entire project for security issues."""
        if exclude_dirs is None:
            exclude_dirs = ['archive', '.git', '__pycache__', '.venv', 'venv']

        self.findings = []

        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if self._should_ignore_file(py_file, exclude_dirs):
                continue
            self._scan_file(py_file)

        # Scan configuration files
        for config_file in self.project_root.rglob("*.json"):
            if self._should_ignore_file(config_file, exclude_dirs):
                continue
            self._scan_file(config_file)

        # Scan batch and PowerShell files
        for script_file in self.project_root.rglob("*.bat"):
            if self._should_ignore_file(script_file, exclude_dirs):
                continue
            self._scan_file(script_file)

        for script_file in self.project_root.rglob("*.ps1"):
            if self._should_ignore_file(script_file, exclude_dirs):
                continue
            self._scan_file(script_file)

        return self.findings

    def _should_ignore_file(self, file_path: Path, exclude_dirs: List[str]) -> bool:
        """Check if file should be ignored during scan."""
        file_str = str(file_path)

        # Check exclude directories
        for exclude_dir in exclude_dirs:
            if exclude_dir in file_str:
                return True

        # Check ignore patterns
        for pattern in self.IGNORE_PATTERNS:
            if re.search(pattern, file_str, re.IGNORECASE):
                return True

        return False

    def _scan_file(self, file_path: Path) -> None:
        """Scan individual file for security issues."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            line_number = 0
            for line in content.split('\n'):
                line_number += 1
                self._scan_line(file_path, line, line_number)

        except Exception as e:
            logger.warning(f"Could not scan file {file_path}: {e}")

    def _scan_line(self, file_path: Path, line: str, line_number: int) -> None:
        """Scan individual line for security issues."""
        for category, patterns in self.CREDENTIAL_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Skip obvious false positives
                    if self._is_false_positive(match.group(0), category):
                        continue

                    self.findings.append({
                        'file': str(file_path),
                        'line': line_number,
                        'category': category,
                        'pattern': pattern,
                        'match': match.group(0),
                        'context': line.strip(),
                        'severity': self._get_severity(category)
                    })

    def _is_false_positive(self, match: str, category: str) -> bool:
        """Check if match is likely a false positive."""
        false_positive_indicators = [
            'example', 'placeholder', 'your_', 'insert_', 'replace_',
            'todo', 'fixme', 'xxx', 'test', 'dummy', 'fake',
            '<', '>', '{', '}', '[', ']'
        ]

        match_lower = match.lower()
        return any(indicator in match_lower for indicator in false_positive_indicators)

    def _get_severity(self, category: str) -> str:
        """Get severity level for finding category."""
        severity_map = {
            'password': 'HIGH',
            'api_key': 'HIGH',
            'secret': 'HIGH',
            'token': 'HIGH',
            'url_with_credentials': 'HIGH',
            'hardcoded_paths': 'MEDIUM'
        }
        return severity_map.get(category, 'LOW')

    def generate_report(self) -> Dict[str, Any]:
        """Generate security audit report."""
        if not self.findings:
            return {
                'status': 'PASS',
                'summary': 'No security issues found',
                'findings': [],
                'recommendations': []
            }

        # Group findings by severity
        severity_counts = {}
        for finding in self.findings:
            severity = finding['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Generate recommendations
        recommendations = self._generate_recommendations()

        return {
            'status': 'ISSUES_FOUND',
            'summary': f"Found {len(self.findings)} potential security issues",
            'severity_counts': severity_counts,
            'findings': self.findings,
            'recommendations': recommendations
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on findings."""
        recommendations = []

        categories = set(finding['category'] for finding in self.findings)

        if 'password' in categories or 'api_key' in categories or 'secret' in categories:
            recommendations.append(
                "Move all credentials to environment variables or secure configuration files"
            )
            recommendations.append(
                "Use the unified configuration system with environment variable substitution"
            )

        if 'hardcoded_paths' in categories:
            recommendations.append(
                "Replace hardcoded file paths with configurable options"
            )

        if any(cat in categories for cat in ['api_key', 'secret', 'token']):
            recommendations.append(
                "Consider using a secrets management service for production deployments"
            )

        recommendations.append(
            "Add security audit to CI/CD pipeline to catch future issues"
        )

        return recommendations


class ConfigurationSecurityManager:
    """Manages secure configuration with environment variable substitution."""

    def __init__(self):
        """Initialize configuration security manager."""
        self.env_var_pattern = re.compile(r'\$\{([^}]+)\}')

    def secure_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process configuration to substitute environment variables."""
        return self._process_dict(config)

    def _process_dict(self, obj: Any) -> Any:
        """Recursively process dictionary for environment variable substitution."""
        if isinstance(obj, dict):
            return {key: self._process_dict(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._process_dict(item) for item in obj]
        elif isinstance(obj, str):
            return self._substitute_env_vars(obj)
        else:
            return obj

    def _substitute_env_vars(self, value: str) -> str:
        """Substitute environment variables in string value."""
        def replace_env_var(match):
            env_var = match.group(1)
            # Support default values: ${VAR_NAME:default_value}
            if ':' in env_var:
                var_name, default_value = env_var.split(':', 1)
                return os.getenv(var_name, default_value)
            else:
                env_value = os.getenv(env_var)
                if env_value is None:
                    logger.warning(f"Environment variable '{env_var}' not found")
                    return match.group(0)  # Return original if not found
                return env_value

        return self.env_var_pattern.sub(replace_env_var, value)

    def list_required_env_vars(self, config: Dict[str, Any]) -> Set[str]:
        """List all environment variables referenced in configuration."""
        env_vars = set()
        self._collect_env_vars(config, env_vars)
        return env_vars

    def _collect_env_vars(self, obj: Any, env_vars: Set[str]) -> None:
        """Recursively collect environment variable names."""
        if isinstance(obj, dict):
            for value in obj.values():
                self._collect_env_vars(value, env_vars)
        elif isinstance(obj, list):
            for item in obj:
                self._collect_env_vars(item, env_vars)
        elif isinstance(obj, str):
            matches = self.env_var_pattern.findall(obj)
            for match in matches:
                # Handle default values
                var_name = match.split(':', 1)[0] if ':' in match else match
                env_vars.add(var_name)

    def create_env_template(self, config: Dict[str, Any], output_path: str) -> None:
        """Create .env template file with all required environment variables."""
        env_vars = self.list_required_env_vars(config)

        template_content = [
            "# Environment Variables for Unified Scraping Framework",
            "# Copy this file to .env and fill in the values",
            ""
        ]

        # Group variables by category
        categories = {
            'google': [],
            'notification': [],
            'database': [],
            'general': []
        }

        for var in sorted(env_vars):
            var_lower = var.lower()
            if 'google' in var_lower or 'sheets' in var_lower:
                categories['google'].append(var)
            elif any(word in var_lower for word in ['email', 'sms', 'slack', 'twilio']):
                categories['notification'].append(var)
            elif 'db' in var_lower or 'database' in var_lower:
                categories['database'].append(var)
            else:
                categories['general'].append(var)

        for category, vars_in_category in categories.items():
            if vars_in_category:
                template_content.append(f"# {category.title()} Configuration")
                for var in vars_in_category:
                    template_content.append(f"{var}=")
                template_content.append("")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(template_content))

        logger.info(f"Environment template created: {output_path}")


def audit_project_security(project_root: str = ".") -> Dict[str, Any]:
    """Perform complete security audit of the project."""
    auditor = SecurityAuditor(project_root)
    findings = auditor.scan_project()
    return auditor.generate_report()


def secure_configuration(config_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Load and secure a configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    manager = ConfigurationSecurityManager()
    secured_config = manager.secure_config(config)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(secured_config, f, indent=2)

    return secured_config
