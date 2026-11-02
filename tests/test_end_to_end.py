
from tax_framework.testing.regression_runner import run_regression_suite
from tax_framework.services.release_gate import evaluate_release


def test_complete_qa_workflow():
    # 1. Execute regression suite.
    results = run_regression_suite()

    assert isinstance(results, list)
    assert results
    assert all(isinstance(result, dict) for result in results)

    # 2. Generate regression summary.
    statuses = [
        str(result.get("status", "")).upper()
        for result in results
    ]

    summary = {
        "total": len(results),
        "passed": statuses.count("PASS"),
        "failed": statuses.count("FAIL"),
        "errors": statuses.count("ERROR"),
    }

    assert summary["total"] == (
        summary["passed"]
        + summary["failed"]
        + summary["errors"]
    )

    # 3. Evaluate release gate.
    release = evaluate_release(results, summary)

    assert isinstance(release, dict)
    assert "release_approved" in release
    assert "release_status" in release

    # 4. Validate release decision.
    assert release["release_status"] in {"APPROVED", "BLOCKED"}

    if summary["failed"] > 0 or summary["errors"] > 0:
        assert release["release_approved"] is False
    else:
        assert release["release_approved"] is True
