
from datetime import datetime, timezone


def evaluate_release(results, summary):
    """Evaluate whether the tax software build can be released."""

    failures = [
        result for result in results
        if result.get("status") == "FAIL"
    ]

    errors = [
        result for result in results
        if result.get("status") == "ERROR"
    ]

    total = summary.get("total", len(results))
    passed = summary.get("passed", 0)

    release_approved = (
        total > 0
        and passed == total
        and not failures
        and not errors
    )

    return {
        "release_status": (
            "APPROVED" if release_approved else "BLOCKED"
        ),
        "release_approved": release_approved,
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": len(failures),
        "error_cases": len(errors),
        "release_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "reason": (
            "All regression tests passed."
            if release_approved
            else "Release blocked: regression failures or errors detected."
        ),
    }
