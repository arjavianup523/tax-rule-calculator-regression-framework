from src.tax_framework.services.rule_loader import load_tax_rules


def test_tax_rules_load_successfully():
    rules = load_tax_rules()

    assert rules["country"] == "India"
    assert rules["financial_year"] == "2025-26"
    assert "new_regime" in rules["tax_slabs"]
    assert "old_regime" in rules["tax_slabs"]