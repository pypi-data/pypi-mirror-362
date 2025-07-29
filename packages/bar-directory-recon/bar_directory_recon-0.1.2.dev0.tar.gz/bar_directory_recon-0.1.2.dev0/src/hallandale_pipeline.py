#!/usr/bin/env python3
"""
Hallandale Property Processing Pipeline
Complete pipeline for processing Hallandale property list PDF and enriching data.
"""

import sys
import os
import logging
import argparse
from pathlib import Path
from typing import Dict, Any

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import pipeline modules
from pdf_processor import HallandalePropertyProcessor
from property_enrichment import PropertyEnrichment
from property_validation import PropertyValidation

# Set flag for Google Sheets integration (currently disabled)
GOOGLE_SHEETS_AVAILABLE = False


class HallandalePipeline:
    """Complete Hallandale property processing pipeline."""

    def __init__(self, output_dir: str = "outputs/hallandale"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create logs directory
        (self.output_dir / "logs").mkdir(exist_ok=True)

        # Setup logging
        self._setup_logging()

        # Initialize processors
        self.pdf_processor = HallandalePropertyProcessor(output_dir)
        self.enricher = PropertyEnrichment(output_dir)
        self.validator = PropertyValidation(output_dir)

        self.logger.info("Hallandale Pipeline initialized")
    def _setup_logging(self) -> None:
        """Setup comprehensive logging."""
        log_file = self.output_dir / "logs" / "pipeline.log"

        logging.basicConfig(
            level=logging.INFO,
    def _setup_logging(self) -> None:
        """Setup comprehensive logging."""
        log_file = self.output_dir / "logs" / "pipeline.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("STARTING HALLANDALE PROPERTY PROCESSING PIPELINE")
        self.logger.info("=" * 60)

            results: Dict[str, Any] = {}
            results["pipeline_status"] = "running"
            results["steps_completed"] = []
            results["errors"] = []
                error_msg = f"PDF processing failed: {pdf_result.get('message', 'Unknown error')}"
                logger.error(error_msg)
            # Step 1: Process PDF
            self.logger.info("Step 1: Processing PDF file")
            pdf_result = self.pdf_processor.process_pdf(pdf_path)
            results["errors"] = []
            error_msg = f"PDF processing failed: {pdf_result.get('message', 'Unknown error')}"
            self.logger.error(error_msg)
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["pipeline_status"] = "failed"
                return results

            results["steps_completed"].append("pdf_processing")
            results["pdf_result"] = pdf_result
            self.logger.info(f"PDF processed successfully: {pdf_result['properties_count']} properties extracted")
                logger.error(error_msg)
            # Step 2: Enrich properties
            self.logger.info("Step 2: Enriching property data")
            enrichment_result = self.enricher.enrich_properties(pdf_result["output_file"])

            self.logger.info(f"PDF processed successfully: {pdf_result['properties_count']} properties extracted")
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                results["pipeline_status"] = "failed"
                return results

            results["steps_completed"].append("property_enrichment")
            results["enrichment_result"] = enrichment_result
            self.logger.info(f"Properties enriched successfully: {enrichment_result['enriched_count']} records")
            logger.info("Step 4: Validating property data")
            # Step 3: Generate enrichment summary
            self.logger.info("Step 3: Generating enrichment summary")
            summary = self.enricher.generate_summary_report(enrichment_result["output_file"])
            results["enrichment_summary"] = summary

            # Step 4: Validate properties
            self.logger.info("Step 4: Validating property data")
            validation_result = self.validator.validate_properties(enrichment_result["output_file"])

            if validation_result["status"] != "success":
                error_msg = f"Validation failed: {validation_result.get('message', 'Unknown error')}"
                self.logger.error(error_msg)
                results["errors"].append(error_msg)
                # Continue pipeline even if validation fails
            else:
                results["steps_completed"].append("property_validation")
                results["validation_result"] = validation_result
                self.logger.info("Property validation completed successfully")
                results["excel_result"] = excel_result
            # Step 5: Create Excel export
            self.logger.info("Step 5: Creating Excel export")
            excel_result = self._create_excel_export(enrichment_result["output_file"])

            if excel_result["status"] == "success":
                results["steps_completed"].append("excel_export")
                results["excel_result"] = excel_result
                self.logger.info(f"Excel export created: {excel_result['output_file']}")
            else:
                results["errors"].append(f"Excel export failed: {excel_result.get('message', 'Unknown error')}")
                    results["steps_completed"].append("google_sheets_upload")
            # Step 6: Google Sheets upload (optional)
            if export_to_sheets and GOOGLE_SHEETS_AVAILABLE:
                self.logger.info("Step 6: Uploading to Google Sheets")
                sheets_result = self._upload_to_google_sheets(enrichment_result["output_file"])

                if sheets_result["status"] == "success":
                    results["steps_completed"].append("google_sheets_upload")
                    results["sheets_result"] = sheets_result
                    self.logger.info(f"Data uploaded to Google Sheets: {sheets_result.get('sheet_url', 'N/A')}")
                else:
                    results["errors"].append(
                        f"Google Sheets upload failed: {sheets_result.get('message', 'Unknown error')}"
                    )
            logger.info("=" * 60)

            return results
            self._generate_final_report(results)

            self.logger.info("=" * 60)
            self.logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 60)

            return results

        except Exception as e:
            error_msg = f"Pipeline failed with exception: {e}"
            self.logger.error(error_msg)
            results["pipeline_status"] = "failed"
            results["errors"].append(error_msg)
            return results
            df = pd.read_csv(csv_file)

            # Create Excel file with multiple sheets
            excel_file = self.output_dir / "hallandale_properties_complete.xlsx"

            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # Main data sheet
                df.to_excel(writer, sheet_name='All Properties', index=False)

                # Priority properties sheet
                priority_df = df[df['priority_flag'] == True]
                priority_df.to_excel(writer, sheet_name='Priority Properties', index=False)

                # Corporate entities sheet
                corporate_df = df[df['is_corporate'] == True]
                corporate_df.to_excel(writer, sheet_name='Corporate Entities', index=False)

                # Missing contact info sheet
                missing_contact_df = df[(df['owner_email'].isna() | (df['owner_email'] == '')) &
                                      (df['owner_phone'].isna() | (df['owner_phone'] == ''))]
                missing_contact_df.to_excel(writer, sheet_name='Missing Contact Info', index=False)

                # Summary statistics sheet
                summary_data = {
                    'Metric': [
                        'Total Properties',
                        'Properties with Email',
                        'Properties with Phone',
                        'Priority Properties',
                        'Corporate Entities',
                        'Individual Owners',
                        'Average Quality Score',
                        'High Quality Records (80+)',
                        'Needs Manual Review (<50)'
                    ],
                    'Count': [
                        len(df),
                        len(df[df['owner_email'].notna() & (df['owner_email'] != '')]),
                        len(df[df['owner_phone'].notna() & (df['owner_phone'] != '')]),
                        len(df[df['priority_flag'] == True]),
                        len(df[df['is_corporate'] == True]),
                        len(df[df['is_corporate'] == False]),
                        round(df['data_quality_score'].mean(), 1),
                        len(df[df['data_quality_score'] >= 80]),
                        len(df[df['data_quality_score'] < 50])
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary Statistics', index=False)

            logger.info(f"Excel export created with {len(df)} records")

            return {
                "status": "success",
                "output_file": str(excel_file),
                "sheets_created": [
                    "All Properties", "Priority Properties", "Corporate Entities",
                    "Missing Contact Info", "Summary Statistics"
                ]
            }

        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            return {"status": "error", "message": str(e)}

    def _upload_to_google_sheets(self, csv_file: str) -> Dict[str, Any]:
        """Upload data to Google Sheets (requires credentials setup)."""
        try:
            if not GOOGLE_SHEETS_AVAILABLE:
                return {"status": "error", "message": "Google Sheets libraries not available"}

            # Note: This requires Google Sheets API credentials
            # For now, return a simulated success
            logger.info("Google Sheets upload simulated (requires API credentials setup)")

            return {
                "status": "success",
                "message": "Upload simulated - configure Google Sheets API credentials",
                "sheet_url": "https://docs.google.com/spreadsheets/d/simulated_upload"
            }

        except Exception as e:
            logger.error(f"Google Sheets upload failed: {e}")
            return {"status": "error", "message": str(e)}

    def _generate_final_report(self, results: Dict[str, Any]) -> None:
        """Generate a comprehensive final report."""
        try:
            report_file = self.output_dir / "hallandale_pipeline_report.txt"

            with open(report_file, 'w') as f:
                f.write("HALLANDALE PROPERTY PROCESSING PIPELINE REPORT\n")
                f.write("=" * 60 + "\n\n")

                f.write(f"Pipeline Status: {results['pipeline_status'].upper()}\n")
                f.write(f"Steps Completed: {', '.join(results['steps_completed'])}\n\n")

                if results.get("pdf_result"):
                    f.write("PDF PROCESSING RESULTS:\n")
                    f.write(f"  Properties Extracted: {results['pdf_result']['properties_count']}\n")
                    f.write(f"  Extraction Method: {results['pdf_result']['extraction_method']}\n\n")

                if results.get("enrichment_summary"):
                    summary = results["enrichment_summary"]
                    f.write("ENRICHMENT SUMMARY:\n")
                    f.write(f"  Total Records: {summary.get('total_records_processed', 0)}\n")
                    f.write(f"  Records with Email: {summary.get('records_with_emails', 0)}\n")
                    f.write(f"  Records with Phone: {summary.get('records_with_phones', 0)}\n")
                    f.write(f"  Priority Records: {summary.get('priority_records', 0)}\n")
                    f.write(f"  Corporate Entities: {summary.get('corporate_entities', 0)}\n")
                    f.write(f"  Individual Owners: {summary.get('individual_owners', 0)}\n")
                    f.write(f"  Average Quality Score: {summary.get('average_data_quality_score', 0)}/100\n")
                    f.write(f"  Needs Manual Review: {summary.get('needs_manual_review', 0)}\n\n")

                if results.get("errors"):
                    f.write("ERRORS/WARNINGS:\n")
                    for error in results["errors"]:
                        f.write(f"  - {error}\n")
                    f.write("\n")

                f.write("OUTPUT FILES CREATED:\n")
                output_files = []
                if results.get("pdf_result", {}).get("output_file"):
                    output_files.append(results["pdf_result"]["output_file"])
                if results.get("enrichment_result", {}).get("output_file"):
                    output_files.append(results["enrichment_result"]["output_file"])
                if results.get("excel_result", {}).get("output_file"):
                    output_files.append(results["excel_result"]["output_file"])

                for file_path in output_files:
                    f.write(f"  - {file_path}\n")

            logger.info(f"Final report saved to {report_file}")

        except Exception as e:
            logger.error(f"Error generating final report: {e}")


def main():
    """Main entry point for the pipeline."""
    parser = argparse.ArgumentParser(description="Hallandale Property Processing Pipeline")
    parser.add_argument("pdf_path", help="Path to the Hallandale property list PDF file")
    parser.add_argument("--output-dir", default="outputs/hallandale",
                       help="Output directory for processed files")
    parser.add_argument("--export", action="store_true",
def main() -> None:
    """Main entry point for the pipeline."""
    parser = argparse.ArgumentParser(description="Hallandale Property Processing Pipeline")
    parser.add_argument("pdf_path", help="Path to the Hallandale property list PDF file")
    parser.add_argument("--output-dir", default="outputs/hallandale",
                       help="Output directory for processed files")
    parser.add_argument("--export", action="store_true",
                       help="Export to Google Sheets (requires API credentials)")

    args = parser.parse_args()

    # Initialize and run pipeline
    pipeline = HallandalePipeline(args.output_dir)
    results = pipeline.run_full_pipeline(args.pdf_path, args.export)

    # Print summary
    print("\n" + "=" * 60)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Status: {results['pipeline_status'].upper()}")
    print(f"Steps completed: {len(results['steps_completed'])}")

    if results.get("enrichment_summary"):
        summary = results["enrichment_summary"]
        print("\nRECORD SUMMARY:")
        print(f"  Total records processed: {summary.get('total_records_processed', 0)}")
        print(f"  Records with emails found: {summary.get('records_with_emails', 0)}")
        print(f"  Records with phones found: {summary.get('records_with_phones', 0)}")
        print(f"  Records marked as priority: {summary.get('priority_records', 0)}")
        print(f"  Records needing manual review: {summary.get('needs_manual_review', 0)}")

    if results.get("errors"):
        print(f"\nERRORS/WARNINGS ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  - {error}")

    print("\nProcessing complete. Check the output directory for all generated files.")
