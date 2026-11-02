
from src.tax_framework.services.release_gate import evaluate_release


def test_release_approved_when_all_tests_pass():
    results = [
        {"case_id": "TC001", "status": "PASS"},
        {"case_id": "TC002", "status": "PASS"},
    ]

    summary = {
        "total": 2,
        "passed": 2,
        "failed": 0,
        "errors": 0,
    }

    decision = evaluate_release(results, summary)

    assert decision["release_status"] == "APPROVED"
    assert decision["release_approved"] is True


def test_release_blocked_when_test_fails():
    results = [
        {"case_id": "TC001", "status": "PASS"},
        {"case_id": "TC002", "status": "FAIL"},
    ]

    summary = {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "errors": 0,
    }

    decision = evaluate_release(results, summary)

    assert decision["release_status"] == "BLOCKED"
    assert decision["release_approved"] is False


def test_release_blocked_when_test_errors():
    results = [
        {"case_id": "TC001", "status": "PASS"},
        {"case_id": "TC002", "status": "ERROR"},
    ]

    summary = {
        "total": 2,
        "passed": 1,
        "failed": 0,
        "errors": 1,
    }

    decision = evaluate_release(results, summary)

    assert decision["release_status"] == "BLOCKED"
