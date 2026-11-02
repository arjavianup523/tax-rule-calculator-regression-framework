
import json
from pathlib import Path

from src.tax_framework.services.full_tax_service import (
    calculate_full_tax
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASELINE_FILE = (
    PROJECT_ROOT
    / "data"
    / "approved_tax_cases.json"
)


def load_baseline_cases():
    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    return baseline["cases"]


def test_approved_tax_cases_match_baseline():
    cases = load_baseline_cases()

    for case in cases:
        result = calculate_full_tax(
            case["gross_salary"],
            case["regime"]
        )

        assert result["taxable_income"] == (
            case["expected_taxable_income"]
        ), f"Taxable income mismatch: {case['case_id']}"

        assert result["total_tax"] == (
            case["expected_total_tax"]
        ), f"Tax mismatch: {case['case_id']}"
