#!/usr/bin/env python3
"""
Property Validation Module
Validates property data and contact information with comprehensive checks.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import socket
import dns.resolver

logger = logging.getLogger(__name__)


class PropertyValidation:
    """Validates property data and contact information."""

    def __init__(self, output_dir: str = "outputs/hallandale"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        # Validation patterns
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self.phone_pattern = re.compile(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
        self.folio_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{4}$')

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / "validation.log"),
                logging.StreamHandler()
            ]
        )

    def validate_properties(self, input_file: str) -> Dict[str, Any]:
        """Validate property data and contact information."""
        try:
            input_path = Path(input_file)
            if not input_path.exists():
                logger.error(f"Input file not found: {input_file}")
                return {"status": "error", "message": "Input file not found"}

            # Read the enriched data
            df = pd.read_csv(input_path)
            logger.info(f"Loading {len(df)} properties for validation")

            # Initialize validation stats
            validation_stats = {
                "total_properties": len(df),
                "valid_emails": 0,
                "verified_emails": 0,
                "valid_phones": 0,
                "valid_addresses": 0,
                "priority_properties": 0,
                "complete_records": 0,
                "validation_errors": []
            }

            # Validate each property
            validated_properties = []
            for idx, row in df.iterrows():
                try:
                    validated_prop = self._validate_single_property(row.to_dict())
                    validated_properties.append(validated_prop)

                    # Update stats
                    self._update_validation_stats(validated_prop, validation_stats)

                except Exception as e:
                    logger.error(f"Error validating property {idx}: {e}")
                    validation_stats["validation_errors"].append(
                        f"Row {idx}: {str(e)}"
                    )

            # Create validated DataFrame
            validated_df = pd.DataFrame(validated_properties)

            # Save validated data
            output_file = self.output_dir / "hallandale_properties_validated.csv"
            validated_df.to_csv(output_file, index=False)

            # Create Excel export
            excel_file = self.output_dir / "hallandale_properties_validated.xlsx"
            self._create_excel_export(validated_df, excel_file)

            # Create summary report
            summary_file = self._create_summary_report(validation_stats, output_file)

            logger.info(f"Validated {len(validated_properties)} properties")
            logger.info(f"Results saved to: {output_file}")
            logger.info(f"Summary saved to: {summary_file}")

            return {
                "status": "success",
                "validated_count": len(validated_properties),
                "output_file": str(output_file),
                "excel_file": str(excel_file),
                "summary_file": str(summary_file),
                "stats": validation_stats
            }

        except Exception as e:
            logger.error(f"Error validating properties: {e}")
            return {"status": "error", "message": str(e)}

    def _validate_single_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single property record."""
        validated = property_data.copy()

        # Email validation
        email = property_data.get("owner_email", "")
        email_validation = self._validate_email_comprehensive(email)
        validated.update(email_validation)

        # Phone validation
        phone = property_data.get("owner_phone", "")
        phone_validation = self._validate_phone_comprehensive(phone)
        validated.update(phone_validation)

        # Address validation
        address = property_data.get("property_address", "")
        address_validation = self._validate_address_comprehensive(address)
        validated.update(address_validation)

        # Folio validation
        folio = property_data.get("folio_number", "")
        validated["folio_valid"] = self._validate_folio(folio)

        # Date validation
        inspection_due = property_data.get("inspection_due", "")
        date_validation = self._validate_dates(inspection_due)
        validated.update(date_validation)

        # Priority calculation
        validated["priority_flag"] = self._calculate_priority_comprehensive(validated)

        # Completeness score
        validated["completeness_score"] = self._calculate_completeness(validated)

        # Overall validation score
        validated["validation_score"] = self._calculate_validation_score(validated)

        # Add validation metadata
        validated["validation_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated["validation_version"] = "1.0"

        return validated

    def _validate_email_comprehensive(self, email: str) -> Dict[str, Any]:
        """Comprehensive email validation."""
        result = {
            "email_valid": False,
            "email_format_valid": False,
            "email_domain_valid": False,
            "email_verified": False,
            "email_validation_notes": []
        }

        if not email:
            result["email_validation_notes"].append("Email is empty")
            return result

        # Format validation
        if self.email_pattern.match(email):
            result["email_format_valid"] = True
            result["email_validation_notes"].append("Email format is valid")
        else:
            result["email_validation_notes"].append("Invalid email format")
            return result

        # Domain validation
        try:
            domain = email.split('@')[1]
            result["email_domain_valid"] = self._validate_domain(domain)
            if result["email_domain_valid"]:
                result["email_validation_notes"].append("Domain is valid")
            else:
                result["email_validation_notes"].append("Domain validation failed")
        except Exception as e:
            result["email_validation_notes"].append(f"Domain validation error: {e}")

        # SMTP verification (optional, can be resource intensive)
        try:
            result["email_verified"] = self._verify_email_smtp(email)
            if result["email_verified"]:
                result["email_validation_notes"].append("SMTP verification passed")
            else:
                result["email_validation_notes"].append("SMTP verification failed")
        except Exception as e:
            result["email_validation_notes"].append(f"SMTP verification error: {e}")

        # Overall email validity
        result["email_valid"] = (
            result["email_format_valid"] and
            result["email_domain_valid"]
        )

        return result

    def _validate_phone_comprehensive(self, phone: str) -> Dict[str, Any]:
        """Comprehensive phone validation."""
        result = {
            "phone_valid": False,
            "phone_format_valid": False,
            "phone_area_code_valid": False,
            "phone_type": "",
            "phone_validation_notes": []
        }

        if not phone:
            result["phone_validation_notes"].append("Phone is empty")
            return result

        # Clean phone number
        phone_clean = re.sub(r'[^\d]', '', phone)

        # Format validation
        if len(phone_clean) == 10:
            result["phone_format_valid"] = True
            result["phone_validation_notes"].append("Phone format is valid")
        else:
            result["phone_validation_notes"].append(f"Invalid phone length: {len(phone_clean)}")
            return result

        # Area code validation
        area_code = phone_clean[:3]
        florida_area_codes = [
            '239', '305', '321', '352', '386', '407', '561', '727', '754', '772',
            '786', '813', '850', '863', '904', '941', '954'
        ]

        if area_code in florida_area_codes:
            result["phone_area_code_valid"] = True
            result["phone_validation_notes"].append("Florida area code detected")
        else:
            result["phone_validation_notes"].append(f"Non-Florida area code: {area_code}")

        # Phone type detection
        if area_code in ['954', '754']:  # Broward County
            result["phone_type"] = "local"
        elif area_code in florida_area_codes:
            result["phone_type"] = "florida"
        else:
            result["phone_type"] = "other"

        # Overall phone validity
        result["phone_valid"] = result["phone_format_valid"]

        return result

    def _validate_address_comprehensive(self, address: str) -> Dict[str, Any]:
        """Comprehensive address validation."""
        result = {
            "address_valid": False,
            "address_format_valid": False,
            "address_city_valid": False,
            "address_state_valid": False,
            "address_zip_valid": False,
            "address_validation_notes": []
        }

        if not address:
            result["address_validation_notes"].append("Address is empty")
            return result

        # Format validation
        if len(address.strip()) > 10 and any(char.isdigit() for char in address):
            result["address_format_valid"] = True
            result["address_validation_notes"].append("Address format appears valid")
        else:
            result["address_validation_notes"].append("Invalid address format")

        # City validation
        hallandale_indicators = [
            'hallandale', 'hollywood', 'aventura', 'sunny isles', 'bal harbour'
        ]

        address_lower = address.lower()
        for city in hallandale_indicators:
            if city in address_lower:
                result["address_city_valid"] = True
                result["address_validation_notes"].append(f"City detected: {city}")
                break

        # State validation
        if 'fl' in address_lower or 'florida' in address_lower:
            result["address_state_valid"] = True
            result["address_validation_notes"].append("Florida state detected")

        # ZIP code validation
        zip_match = re.search(r'\b33\d{3}\b', address)
        if zip_match:
            result["address_zip_valid"] = True
            result["address_validation_notes"].append(f"Valid ZIP code: {zip_match.group()}")

        # Overall address validity
        result["address_valid"] = (
            result["address_format_valid"] and
            (result["address_city_valid"] or result["address_state_valid"])
        )

        return result

    def _validate_domain(self, domain: str) -> bool:
        """Validate email domain using DNS lookup."""
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            try:
                dns.resolver.resolve(domain, 'A')
                return True
            except:
                return False

    def _verify_email_smtp(self, email: str) -> bool:
        """Verify email using SMTP (basic check)."""
        try:
            domain = email.split('@')[1]

            # Get MX record
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(mx_records[0]).split(' ')[1]

            # Connect to SMTP server
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_record)
            server.helo()
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            server.quit()

            return code == 250

        except Exception:
            return False

    def _validate_folio(self, folio: str) -> bool:
        """Validate folio number format."""
        if not folio:
            return False

        # Basic folio pattern check
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}-\d{4}$', folio))

    def _validate_dates(self, inspection_due: str) -> Dict[str, Any]:
        """Validate date fields."""
        result = {
            "inspection_due_valid": False,
            "inspection_due_upcoming": False,
            "days_until_inspection": None
        }

        if not inspection_due:
            return result

        try:
            # Parse date
            date_obj = pd.to_datetime(inspection_due)
            result["inspection_due_valid"] = True

            # Check if upcoming
            today = datetime.now()
            days_diff = (date_obj - today).days
            result["days_until_inspection"] = days_diff

            if 0 <= days_diff <= 180:  # Next 6 months
                result["inspection_due_upcoming"] = True

        except Exception:
            pass

        return result

    def _calculate_priority_comprehensive(self, property_data: Dict[str, Any]) -> bool:
        """Calculate comprehensive priority flag."""
        priority_factors = []

        # Inspection deadline priority
        if property_data.get("inspection_due_upcoming"):
            priority_factors.append("inspection_upcoming")

        # Year built priority (1984-1986)
        year_built = property_data.get("year_built", "")
        if year_built:
            try:
                year = int(year_built)
                if 1984 <= year <= 1986:
                    priority_factors.append("year_built_priority")
            except ValueError:
                pass

        # Contact availability priority
        if property_data.get("email_valid") and property_data.get("phone_valid"):
            priority_factors.append("full_contact_available")

        # Completeness priority
        if property_data.get("completeness_score", 0) >= 90:
            priority_factors.append("high_completeness")

        # Notes priority
        notes = property_data.get("notes", "")
        if "priority" in notes.lower():
            priority_factors.append("notes_priority")

        return len(priority_factors) >= 2

    def _calculate_completeness(self, property_data: Dict[str, Any]) -> float:
        """Calculate completeness score."""
        required_fields = [
            "property_address", "owner_name", "mailing_address",
            "year_built", "folio_number", "owner_email", "owner_phone"
        ]

        filled_fields = sum(1 for field in required_fields
                          if property_data.get(field, "").strip())

        return (filled_fields / len(required_fields)) * 100

    def _calculate_validation_score(self, property_data: Dict[str, Any]) -> float:
        """Calculate overall validation score."""
        score_components = [
            ("email_valid", 25),
            ("phone_valid", 25),
            ("address_valid", 25),
            ("folio_valid", 10),
            ("inspection_due_valid", 15)
        ]

        total_score = 0
        for field, weight in score_components:
            if property_data.get(field, False):
                total_score += weight

        return total_score

    def _update_validation_stats(self, validated_prop: Dict[str, Any], stats: Dict[str, Any]) -> None:
        """Update validation statistics."""
        if validated_prop.get("email_valid"):
            stats["valid_emails"] += 1
        if validated_prop.get("email_verified"):
            stats["verified_emails"] += 1
        if validated_prop.get("phone_valid"):
            stats["valid_phones"] += 1
        if validated_prop.get("address_valid"):
            stats["valid_addresses"] += 1
        if validated_prop.get("priority_flag"):
            stats["priority_properties"] += 1
        if validated_prop.get("completeness_score", 0) >= 80:
            stats["complete_records"] += 1

    def _create_excel_export(self, df: pd.DataFrame, excel_file: Path) -> None:
        """Create Excel export with formatting."""
        try:
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='Properties', index=False)

                # Priority properties sheet
                priority_df = df[df['priority_flag'] == True]
                priority_df.to_excel(writer, sheet_name='Priority Properties', index=False)

                # Summary statistics sheet
                summary_data = {
                    'Metric': [
                        'Total Properties',
                        'Valid Emails',
                        'Valid Phones',
                        'Valid Addresses',
                        'Priority Properties',
                        'Complete Records'
                    ],
                    'Count': [
                        len(df),
                        len(df[df['email_valid'] == True]),
                        len(df[df['phone_valid'] == True]),
                        len(df[df['address_valid'] == True]),
                        len(df[df['priority_flag'] == True]),
                        len(df[df['completeness_score'] >= 80])
                    ]
                }

                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)

            logger.info(f"Excel export created: {excel_file}")

        except Exception as e:
            logger.error(f"Error creating Excel export: {e}")

    def _create_summary_report(self, stats: Dict[str, Any], output_file: Path) -> Path:
        """Create detailed summary report."""
        summary_file = self.output_dir / "hallandale_processing_summary.txt"

        try:
            with open(summary_file, 'w') as f:
                f.write("HALLANDALE PROPERTY VALIDATION SUMMARY\n")
                f.write("=" * 50 + "\n\n")

                f.write(f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Output File: {output_file}\n\n")

                f.write("VALIDATION STATISTICS:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total Properties Processed: {stats['total_properties']}\n")
                f.write(f"Properties with Valid Emails: {stats['valid_emails']} ({stats['valid_emails']/stats['total_properties']*100:.1f}%)\n")
                f.write(f"Properties with Verified Emails: {stats['verified_emails']} ({stats['verified_emails']/stats['total_properties']*100:.1f}%)\n")
                f.write(f"Properties with Valid Phones: {stats['valid_phones']} ({stats['valid_phones']/stats['total_properties']*100:.1f}%)\n")
                f.write(f"Properties with Valid Addresses: {stats['valid_addresses']} ({stats['valid_addresses']/stats['total_properties']*100:.1f}%)\n")
                f.write(f"Priority Properties: {stats['priority_properties']} ({stats['priority_properties']/stats['total_properties']*100:.1f}%)\n")
                f.write(f"Complete Records: {stats['complete_records']} ({stats['complete_records']/stats['total_properties']*100:.1f}%)\n\n")

                if stats['validation_errors']:
                    f.write("VALIDATION ERRORS:\n")
                    f.write("-" * 30 + "\n")
                    for error in stats['validation_errors']:
                        f.write(f"- {error}\n")
                    f.write("\n")

                f.write("NEXT STEPS:\n")
                f.write("-" * 30 + "\n")
                f.write("1. Review priority properties for immediate outreach\n")
                f.write("2. Validate missing contact information manually\n")
                f.write("3. Export to Google Sheets for team collaboration\n")
                f.write("4. Set up automated monitoring for inspection deadlines\n")

            return summary_file

        except Exception as e:
            logger.error(f"Error creating summary report: {e}")
            return summary_file


if __name__ == "__main__":
    validator = PropertyValidation()
    result = validator.validate_properties("outputs/hallandale/hallandale_properties_enriched.csv")
    print(f"Validation result: {result}")
