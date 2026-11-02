
from pathlib import Path

from src.tax_framework.reporting.excel_report import (
    generate_excel_report,
)


def test_excel_report_generation():
    results = [
        {
            "case_id": "TEST001",
            "description": "Sample tax test",
            "status": "PASS",
            "expected_tax": 1000,
            "actual_tax": 1000,
            "tax_difference": 0,
        }
    ]

    summary = {
        "total": 1,
        "passed": 1,
        "failed": 0,
        "errors": 0,
        "overall_status": "PASS",
    }

    report_path = generate_excel_report(results, summary)

    assert report_path.exists()
    assert report_path.suffix == ".xlsx"
    assert report_path.stat().st_size > 0
