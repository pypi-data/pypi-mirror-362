#!/usr/bin/env python3
"""
Notification Module for Unified Scraping Framework
Handles email, SMS, and Slack notifications for scraping operations.
"""

import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class NotificationConfig:
    """Configuration for notification services."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize notification configuration."""
        self.config = config
        self.enabled = config.get('enabled', False)

        # Email configuration
        self.email_config = config.get('email', {})
        self.email_enabled = self.email_config.get('enabled', False)

        # SMS configuration
        self.sms_config = config.get('sms', {})
        self.sms_enabled = self.sms_config.get('enabled', False)

        # Slack configuration
        self.slack_config = config.get('slack', {})
        self.slack_enabled = self.slack_config.get('enabled', False)


class NotificationAgent:
    """Unified notification agent for scraping operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize notification agent."""
        self.config = NotificationConfig(config or {})
        self.logger = logging.getLogger(f"{__name__}.NotificationAgent")

    def send_notification(self,
                         message: str,
                         subject: str = "Scraping Notification",
                         notification_type: str = "info",
                         include_stats: bool = False,
                         stats: Optional[Dict[str, Any]] = None) -> bool:
        """Send notification via configured channels."""
        if not self.config.enabled:
            self.logger.debug("Notifications disabled")
            return True

        success = True

        # Prepare message content
        content = self._prepare_message_content(message, subject, notification_type, stats if include_stats else None)

        # Send via email
        if self.config.email_enabled:
            if not self._send_email(content['subject'], content['body']):
                success = False

        # Send via SMS
        if self.config.sms_enabled:
            if not self._send_sms(content['sms']):
                success = False

        # Send via Slack
        if self.config.slack_enabled:
            if not self._send_slack(content['slack']):
                success = False

        return success

    def send_completion_notification(self,
                                   session_name: str,
                                   stats: Dict[str, Any],
                                   success: bool = True) -> bool:
        """Send completion notification with session statistics."""
        status = "completed successfully" if success else "completed with errors"

        message = f"Scraping session '{session_name}' {status}"
        notification_type = "success" if success else "warning"

        return self.send_notification(
            message=message,
            subject=f"Scraping Complete: {session_name}",
            notification_type=notification_type,
            include_stats=True,
            stats=stats
        )

    def send_error_notification(self,
                              session_name: str,
                              error_message: str,
                              error_details: Optional[str] = None) -> bool:
        """Send error notification."""
        message = f"Scraping session '{session_name}' encountered an error: {error_message}"

        if error_details:
            message += f"\n\nDetails:\n{error_details}"

        return self.send_notification(
            message=message,
            subject=f"Scraping Error: {session_name}",
            notification_type="error"
        )

    def send_test_notification(self) -> bool:
        """Send test notification to verify configuration."""
        message = "This is a test notification from the Unified Scraping Framework"

        return self.send_notification(
            message=message,
            subject="Test Notification - Scraping Framework",
            notification_type="test"
        )

    def send_test_email(self) -> bool:
        """Send test email notification only."""
        if not self.config.email_config.get('enabled', False):
            self.logger.warning("Email notifications not enabled")
            return False

        return self._send_email(
            "This is a test email from the Unified Scraping Framework",
            "Test Email - Scraping Framework"
        )

    def send_test_sms(self) -> bool:
        """Send test SMS notification only."""
        if not self.config.sms_config.get('enabled', False):
            self.logger.warning("SMS notifications not enabled")
            return False

        return self._send_sms("Test SMS from Scraping Framework")

    def send_test_slack(self) -> bool:
        """Send test Slack notification only."""
        if not self.config.slack_config.get('enabled', False):
            self.logger.warning("Slack notifications not enabled")
            return False

        return self._send_slack("This is a test Slack message from the Unified Scraping Framework")

    def send_test_notification_by_type(self, notification_type: str) -> bool:
        """Send test notification for specific type."""
        if notification_type == 'email':
            return self.send_test_email()
        elif notification_type == 'sms':
            return self.send_test_sms()
        elif notification_type == 'slack':
            return self.send_test_slack()
        elif notification_type == 'all':
            return self.send_test_notification()
        else:
            self.logger.error(f"Unknown notification type: {notification_type}")
            return False

    def _prepare_message_content(self,
                                message: str,
                                subject: str,
                                notification_type: str,
                                stats: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Prepare message content for different channels."""

        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare email body
        email_body = f"{message}\n\nTimestamp: {timestamp}"

        if stats:
            email_body += self._format_stats_for_email(stats)

        # Prepare SMS (short version)
        sms_message = f"[{notification_type.upper()}] {message[:100]}..."

        # Prepare Slack message
        slack_message = {
            "text": subject,
            "attachments": [{
                "color": self._get_color_for_type(notification_type),
                "fields": [
                    {"title": "Message", "value": message, "short": False},
                    {"title": "Time", "value": timestamp, "short": True},
                    {"title": "Type", "value": notification_type.title(), "short": True}
                ]
            }]
        }

        if stats:
            stats_fields = self._format_stats_for_slack(stats)
            if isinstance(slack_message["attachments"], list) and len(slack_message["attachments"]) > 0:
                slack_message["attachments"][0]["fields"].extend(stats_fields)

        return {
            "subject": subject,
            "body": email_body,
            "sms": sms_message,
            "slack": json.dumps(slack_message)
        }

    def _send_email(self, subject: str, body: str) -> bool:
        """Send email notification."""
        try:
            smtp_server = self.config.email_config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.config.email_config.get('smtp_port', 587)
            sender_email = self.config.email_config.get('sender_email')
            sender_password = self.config.email_config.get('sender_password')
            recipient_emails = self.config.email_config.get('recipients', [])

            if not all([sender_email, sender_password, recipient_emails]):
                self.logger.error("Email configuration incomplete")
                return False

            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = ", ".join(recipient_emails)
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context)
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_emails, message.as_string())

            self.logger.info(f"Email sent to {len(recipient_emails)} recipients")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False

    def _send_sms(self, message: str) -> bool:
        """Send SMS notification via Twilio."""
        try:
            # Import Twilio only if SMS is enabled
            from twilio.rest import Client

            account_sid = self.config.sms_config.get('twilio_account_sid')
            auth_token = self.config.sms_config.get('twilio_auth_token')
            from_number = self.config.sms_config.get('from_number')
            to_numbers = self.config.sms_config.get('to_numbers', [])

            if not all([account_sid, auth_token, from_number, to_numbers]):
                self.logger.error("SMS configuration incomplete")
                return False

            client = Client(account_sid, auth_token)

            for to_number in to_numbers:
                client.messages.create(
                    body=message,
                    from_=from_number,
                    to=to_number
                )

            self.logger.info(f"SMS sent to {len(to_numbers)} recipients")
            return True

        except ImportError:
            self.logger.error("Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            self.logger.error(f"Failed to send SMS: {e}")
            return False

    def _send_slack(self, message: str) -> bool:
        """Send Slack notification."""
        try:
            import requests

            webhook_url = self.config.slack_config.get('webhook_url')

            if not webhook_url:
                self.logger.error("Slack webhook URL not configured")
                return False

            response = requests.post(webhook_url, data=message, headers={'Content-Type': 'application/json'})
            response.raise_for_status()

            self.logger.info("Slack notification sent")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send Slack notification: {e}")
            return False

    def _format_stats_for_email(self, stats: Dict[str, Any]) -> str:
        """Format statistics for email body."""
        stats_text = "\n\n--- Session Statistics ---\n"

        for key, value in stats.items():
            if key == 'start_time' and hasattr(value, 'strftime'):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            stats_text += f"{key.replace('_', ' ').title()}: {value}\n"

        return stats_text

    def _format_stats_for_slack(self, stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format statistics for Slack attachment fields."""
        fields = []

        for key, value in stats.items():
            if key == 'start_time' and hasattr(value, 'strftime'):
                value = value.strftime("%Y-%m-%d %H:%M:%S")

            fields.append({
                "title": key.replace('_', ' ').title(),
                "value": str(value),
                "short": True
            })

        return fields

    def _get_color_for_type(self, notification_type: str) -> str:
        """Get color for Slack message based on notification type."""
        colors = {
            "success": "good",
            "warning": "warning",
            "error": "danger",
            "info": "#36a64f",
            "test": "#439FE0"
        }
        return colors.get(notification_type, "#36a64f")


def create_sample_notification_config() -> Dict[str, Any]:
    """Create sample notification configuration."""
    return {
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
    }
