
from src.tax_framework.testing.regression_runner import (
    run_regression_suite,
    summarize_results
)

from src.tax_framework.database.audit_database import (
    initialize_database,
    save_regression_run,
    get_regression_history,
    get_run_details
)


def test_database_initialization():
    initialize_database()


def test_regression_run_is_saved():
    results = run_regression_suite()
    summary = summarize_results(results)

    run_id = save_regression_run(results, summary)

    assert run_id > 0


def test_saved_regression_history():
    history = get_regression_history()

    assert len(history) >= 1
    assert history[0]["overall_status"] == "PASS"


def test_saved_regression_details():
    history = get_regression_history()
    latest_run_id = history[0]["run_id"]

    details = get_run_details(latest_run_id)

    assert len(details) == 4
    assert all(
        result["status"] == "PASS"
        for result in details
    )
