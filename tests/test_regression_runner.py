
from src.tax_framework.testing.regression_runner import (
    run_regression_suite,
    summarize_results
)


def test_regression_suite_returns_results():
    results = run_regression_suite()

    assert len(results) == 4
    assert all(
        result["status"] == "PASS"
        for result in results
    )


def test_regression_summary():
    results = run_regression_suite()

    summary = summarize_results(results)

    assert summary["total_cases"] == 4
    assert summary["passed"] == 4
    assert summary["failed"] == 0
    assert summary["overall_status"] == "PASS"
