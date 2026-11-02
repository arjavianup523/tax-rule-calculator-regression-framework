
from pathlib import Path
from datetime import datetime

import pandas as pd

from src.tax_framework.database.audit_database import get_open_defects
from src.tax_framework.services.release_gate import evaluate_release


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def generate_excel_report(results, summary):
    """Export regression results, defects, and release decision."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = OUTPUT_DIR / f"tax_regression_report_{timestamp}.xlsx"

    release_decision = evaluate_release(results, summary)

    summary_df = pd.DataFrame({
        "Metric": [
            "Report Generated",
            "Overall Regression Status",
            "Total Test Cases",
            "Passed",
            "Failed",
            "Errors",
        ],
        "Value": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary.get("overall_status", "UNKNOWN"),
            summary.get("total", 0),
            summary.get("passed", 0),
            summary.get("failed", 0),
            summary.get("errors", 0),
        ],
    })

    release_df = pd.DataFrame([
        {"Metric": key, "Value": value}
        for key, value in release_decision.items()
    ])

    results_df = pd.DataFrame(results)
    defects_df = pd.DataFrame(get_open_defects())

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        summary_df.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False,
        )

        release_df.to_excel(
            writer,
            sheet_name="Release Gate",
            index=False,
        )

        results_df.to_excel(
            writer,
            sheet_name="Regression Results",
            index=False,
        )

        defects_df.to_excel(
            writer,
            sheet_name="Open Defects",
            index=False,
        )

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"

            if worksheet.max_row > 1 and worksheet.max_column > 0:
                worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:
                max_length = max(
                    len(str(cell.value or ""))
                    for cell in column_cells
                )

                column_letter = column_cells[0].column_letter
                worksheet.column_dimensions[column_letter].width = min(
                    max_length + 3,
                    45,
                )

    return report_path
