import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RULES_FILE = (
    PROJECT_ROOT
    / "config"
    / "tax_rules_fy2025_26.json"
)


def load_tax_rules():
    """Load tax rules from the JSON configuration."""

    if not RULES_FILE.exists():
        raise FileNotFoundError(
            f"Tax rules file not found: {RULES_FILE}"
        )

    with RULES_FILE.open("r", encoding="utf-8") as file:
        rules = json.load(file)

    if "tax_slabs" not in rules:
        raise ValueError("Tax slabs are missing.")

    if "standard_deduction" not in rules:
        raise ValueError("Standard deduction is missing.")

    return rules