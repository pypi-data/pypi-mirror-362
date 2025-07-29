"""
Unified logging and error handling for the scraping framework.
Provides structured logging, error capture, and screenshot management.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import traceback
import json


class ScrapingLogger:
    """Enhanced logger for scraping operations."""

    def __init__(self, name: str, log_dir: str = "logs", log_level: str = "INFO"):
        """Initialize the logger."""
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        # File handler for detailed logs
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)

        # Console handler for user feedback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)

        # Statistics tracking
        self.stats: Dict[str, Any] = {
            'start_time': datetime.now(),
            'pages_processed': 0,
            'records_extracted': 0,
            'errors': 0,
            'warnings': 0,
            'screenshots': 0
        }

        # Error tracking
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

        self.info(f"Logger initialized for {name}")

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)
        warnings_count = self.stats.get('warnings', 0)
        if isinstance(warnings_count, int):
            self.stats['warnings'] = warnings_count + 1
        self.warnings.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'kwargs': kwargs
        })

    def error(self, message: str, exception: Optional[Exception] = None, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)
        errors_count = self.stats.get('errors', 0)
        if isinstance(errors_count, int):
            self.stats['errors'] = errors_count + 1

        error_data = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'kwargs': kwargs
        }

        if exception:
            error_data['exception'] = str(exception)
            error_data['traceback'] = traceback.format_exc()

        self.errors.append(error_data)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)

    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs: Any) -> None:
        """Log critical error."""
        self.logger.critical(message, **kwargs)
        errors_count = self.stats.get('errors', 0)
        if isinstance(errors_count, int):
            self.stats['errors'] = errors_count + 1

        error_data = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'level': 'CRITICAL',
            'kwargs': kwargs
        }

        if exception:
            error_data['exception'] = str(exception)
            error_data['traceback'] = traceback.format_exc()

        self.errors.append(error_data)

    def log_page_processed(self, url: str, success: bool = True, **kwargs: Any) -> None:
        """Log page processing result."""
        pages_count = self.stats.get('pages_processed', 0)
        if isinstance(pages_count, int):
            self.stats['pages_processed'] = pages_count + 1

        if success:
            self.info(f"Page processed: {url}", **kwargs)
        else:
            self.warning(f"Page processing failed: {url}", **kwargs)

    def log_record_extracted(self, record: Dict[str, Any], url: str = "") -> None:
        """Log successful record extraction."""
        records_count = self.stats.get('records_extracted', 0)
        if isinstance(records_count, int):
            self.stats['records_extracted'] = records_count + 1
        self.debug(f"Record extracted from {url}: {record.get('name', 'Unknown')}")

    def log_screenshot(self, screenshot_path: str, context: str = "") -> None:
        """Log screenshot capture."""
        screenshots_count = self.stats.get('screenshots', 0)
        if isinstance(screenshots_count, int):
            self.stats['screenshots'] = screenshots_count + 1
        self.info(f"Screenshot saved: {screenshot_path} ({context})")

    def log_pagination(self, current_page: int, total_pages: Optional[int] = None) -> None:
        """Log pagination progress."""
        if total_pages:
            self.info(f"Processing page {current_page}/{total_pages}")
        else:
            self.info(f"Processing page {current_page}")

    def log_extraction_phase(self, phase: str, url: str, success: bool = True) -> None:
        """Log extraction phase (listing/detail)."""
        status = "completed" if success else "failed"
        self.info(f"{phase.title()} phase {status}: {url}")

    def log_config_loaded(self, config_path: str, config_name: str) -> None:
        """Log configuration loading."""
        self.info(f"Configuration loaded: {config_name} from {config_path}")

    def log_driver_action(self, action: str, details: str = "") -> None:
        """Log WebDriver actions."""
        message = f"WebDriver: {action}"
        if details:
            message += f" - {details}"
        self.debug(message)

    def log_data_validation(self, record: Dict[str, Any], valid: bool, issues: Optional[List[str]] = None) -> None:
        """Log data validation results."""
        if valid:
            self.debug(f"Record validation passed: {record.get('name', 'Unknown')}")
        else:
            issues_str = ", ".join(issues) if issues else "Unknown issues"
            self.warning(f"Record validation failed: {record.get('name', 'Unknown')} - {issues_str}")

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        current_time = datetime.now()
        runtime = current_time - self.stats['start_time']

        return {
            **self.stats,
            'end_time': current_time.isoformat(),
            'runtime_seconds': runtime.total_seconds(),
            'runtime_formatted': str(runtime),
            'pages_per_minute': (self.stats['pages_processed'] / max(runtime.total_seconds() / 60, 1)),
            'records_per_minute': (self.stats['records_extracted'] / max(runtime.total_seconds() / 60, 1))
        }

    def get_summary(self) -> str:
        """Get a formatted summary of the scraping session."""
        stats = self.get_stats()

        summary = f"""
=== SCRAPING SESSION SUMMARY ===
Session: {self.name}
Runtime: {stats['runtime_formatted']}
Pages Processed: {stats['pages_processed']}
Records Extracted: {stats['records_extracted']}
Errors: {stats['errors']}
Warnings: {stats['warnings']}
Screenshots: {stats['screenshots']}

Performance:
- Pages per minute: {stats['pages_per_minute']:.2f}
- Records per minute: {stats['records_per_minute']:.2f}
"""

        if self.errors:
            summary += f"\nRecent Errors ({len(self.errors)}):\n"
            for error in self.errors[-5:]:  # Show last 5 errors
                summary += f"- {error['message']}\n"

        if self.warnings:
            summary += f"\nRecent Warnings ({len(self.warnings)}):\n"
            for warning in self.warnings[-5:]:  # Show last 5 warnings
                summary += f"- {warning['message']}\n"

        return summary

    def save_session_report(self, output_path: Optional[str] = None) -> str:
        """Save detailed session report to file."""
        if not output_path:
            report_path = self.log_dir / f"{self.name}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_path = str(report_path)

        start_time = self.stats.get('start_time', datetime.now())
        if isinstance(start_time, datetime):
            start_time_iso = start_time.isoformat()
        else:
            start_time_iso = str(start_time)

        report = {
            'session_info': {
                'name': self.name,
                'start_time': start_time_iso,
                'end_time': datetime.now().isoformat()
            },
            'statistics': self.get_stats(),
            'errors': self.errors,
            'warnings': self.warnings
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.info(f"Session report saved: {output_path}")
        return str(output_path)

    def close(self) -> None:
        """Close the logger and save final report."""
        self.info("Closing logger session")
        self.info(self.get_summary())

        # Save detailed report
        self.save_session_report()

        # Close handlers
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def configure_logging_level(self, quiet: bool = False, verbose: bool = False) -> None:
        """Configure logging level based on quiet/verbose flags."""
        if quiet:
            # Suppress all but critical messages
            self.logger.setLevel(logging.ERROR)
            # Update console handler to only show errors
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.ERROR)
        elif verbose:
            # Show all debug messages
            self.logger.setLevel(logging.DEBUG)
            # Update console handler to show debug
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.DEBUG)
        else:
            # Default INFO level
            self.logger.setLevel(logging.INFO)
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)

        # Log the configuration change
        if not quiet:
            if verbose:
                self.logger.debug("Verbose logging enabled")
            else:
                self.logger.info("Standard logging level set")


def create_logger(name: str, log_dir: str = "logs", log_level: str = "INFO") -> ScrapingLogger:
    """Create a new scraping logger instance."""
    return ScrapingLogger(name, log_dir, log_level)


def log_function_call(logger: ScrapingLogger, func_name: str, args: tuple = (), kwargs: Optional[dict] = None) -> None:
    """Log function call with parameters."""
    kwargs = kwargs or {}
    args_str = ", ".join(str(arg) for arg in args)
    kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    params = ", ".join(filter(None, [args_str, kwargs_str]))
    logger.debug(f"Calling {func_name}({params})")


def log_exception(logger: ScrapingLogger, exception: Exception, context: str = "") -> None:
    """Log exception with context."""
    context_msg = f" in {context}" if context else ""
    logger.error(f"Exception{context_msg}: {str(exception)}", exception=exception)


def log_performance(logger: ScrapingLogger, operation: str, duration: float, **metrics: Any) -> None:
    """Log performance metrics."""
    metrics_str = ", ".join(f"{k}={v}" for k, v in metrics.items())
    logger.info(f"Performance - {operation}: {duration:.2f}s ({metrics_str})")
