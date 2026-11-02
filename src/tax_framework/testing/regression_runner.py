
import json
from pathlib import Path
from datetime import datetime, timezone

from src.tax_framework.services.full_tax_service import (
    calculate_full_tax
)
from src.tax_framework.database.audit_database import (
    save_regression_run
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

BASELINE_FILE = PROJECT_ROOT / "data" / "approved_tax_cases.json"


def load_baseline_cases():
    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)["cases"]


def run_regression_suite(save_to_database=True):
    cases = load_baseline_cases()
    results = []

    for case in cases:
        try:
            actual = calculate_full_tax(
                case["gross_salary"],
                case["regime"]
            )

            expected_tax = case["expected_total_tax"]
            actual_tax = actual["total_tax"]

            expected_income = case["expected_taxable_income"]
            actual_income = actual["taxable_income"]

            passed = (
                expected_tax == actual_tax
                and expected_income == actual_income
            )

            results.append({
                "case_id": case["case_id"],
                "description": case["description"],
                "status": "PASS" if passed else "FAIL",
                "expected_tax": expected_tax,
                "actual_tax": actual_tax,
                "tax_difference": round(
                    actual_tax - expected_tax, 2
                ),
                "expected_taxable_income": expected_income,
                "actual_taxable_income": actual_income,
                "error_message": None
            })

        except Exception as error:
            results.append({
                "case_id": case["case_id"],
                "description": case["description"],
                "status": "ERROR",
                "expected_tax": case["expected_total_tax"],
                "actual_tax": None,
                "tax_difference": None,
                "expected_taxable_income": case[
                    "expected_taxable_income"
                ],
                "actual_taxable_income": None,
                "error_message": str(error)
            })

    summary = summarize_results(results)

    if save_to_database:
        run_id = save_regression_run(results, summary)
        summary["run_id"] = run_id

    return results


def summarize_results(results):
    total = len(results)
    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    errors = sum(r["status"] == "ERROR" for r in results)

    return {
        "total_cases": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "overall_status": (
            "PASS" if failed == 0 and errors == 0 else "FAIL"
        )
    }
