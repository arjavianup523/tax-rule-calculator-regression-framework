
from src.tax_framework.database.audit_database import (
    initialize_database,
    get_open_defects,
    update_defect_status
)


def test_defect_table_initializes():
    initialize_database()


def test_invalid_defect_status_rejected():
    try:
        update_defect_status(1, "INVALID")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid status should be rejected")


def test_open_defects_returns_list():
    defects = get_open_defects()

    assert isinstance(defects, list)
