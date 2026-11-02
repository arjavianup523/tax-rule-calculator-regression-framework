
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_PATH = PROJECT_ROOT / "data" / "tax_qa_audit.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS regression_runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp TEXT NOT NULL,
                total_cases INTEGER NOT NULL,
                passed_cases INTEGER NOT NULL,
                failed_cases INTEGER NOT NULL,
                overall_status TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS regression_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                case_id TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL,
                expected_tax REAL,
                actual_tax REAL,
                tax_difference REAL,
                details_json TEXT,
                FOREIGN KEY (run_id)
                    REFERENCES regression_runs(run_id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS defects (
                defect_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                case_id TEXT NOT NULL,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'OPEN',
                expected_tax REAL,
                actual_tax REAL,
                difference REAL,
                error_message TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (run_id)
                    REFERENCES regression_runs(run_id)
            )
        """)


def save_regression_run(results, summary):
    initialize_database()

    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO regression_runs (
                run_timestamp,
                total_cases,
                passed_cases,
                failed_cases,
                overall_status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            timestamp,
            summary["total_cases"],
            summary["passed"],
            summary["failed"] + summary.get("errors", 0),
            summary["overall_status"]
        ))

        run_id = cursor.lastrowid

        for result in results:
            connection.execute("""
                INSERT INTO regression_results (
                    run_id,
                    case_id,
                    description,
                    status,
                    expected_tax,
                    actual_tax,
                    tax_difference,
                    details_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                result["case_id"],
                result["description"],
                result["status"],
                result["expected_tax"],
                result["actual_tax"],
                result["tax_difference"],
                json.dumps(result)
            ))

            if result["status"] in ("FAIL", "ERROR"):
                severity = (
                    "HIGH" if result["status"] == "ERROR"
                    else "MEDIUM"
                )

                connection.execute("""
                    INSERT INTO defects (
                        run_id,
                        case_id,
                        title,
                        severity,
                        expected_tax,
                        actual_tax,
                        difference,
                        error_message,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    run_id,
                    result["case_id"],
                    f"Regression {result['status']}: {result['case_id']}",
                    severity,
                    result["expected_tax"],
                    result["actual_tax"],
                    result["tax_difference"],
                    result.get("error_message"),
                    timestamp
                ))

    return run_id


def get_regression_history():
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM regression_runs
            ORDER BY run_id DESC
        """).fetchall()

    return [dict(row) for row in rows]


def get_run_details(run_id):
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM regression_results
            WHERE run_id = ?
            ORDER BY result_id
        """, (run_id,)).fetchall()

    return [dict(row) for row in rows]


def get_open_defects():
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM defects
            WHERE status = 'OPEN'
            ORDER BY defect_id DESC
        """).fetchall()

    return [dict(row) for row in rows]


def update_defect_status(defect_id, status):
    allowed_statuses = {
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    }

    if status not in allowed_statuses:
        raise ValueError("Invalid defect status.")

    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE defects
            SET status = ?
            WHERE defect_id = ?
        """, (status, defect_id))

    return cursor.rowcount
