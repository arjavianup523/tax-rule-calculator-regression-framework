
import pytest

from src.tax_framework.services.tax_calculator import (
    calculate_slab_tax,
)
from src.tax_framework.services.full_tax_service import (
    calculate_full_tax,
)


@pytest.mark.parametrize(
    "regime,threshold,expected_tax",
    [
        ("new_regime", 400000, 0),
        ("new_regime", 800000, 20000),
        ("new_regime", 1200000, 60000),
        ("new_regime", 1600000, 120000),
        ("new_regime", 2000000, 200000),
        ("new_regime", 2400000, 300000),
        ("old_regime", 250000, 0),
        ("old_regime", 500000, 12500),
        ("old_regime", 1000000, 112500),
    ],
)
def test_tax_at_slab_thresholds(regime, threshold, expected_tax):
    actual_tax = calculate_slab_tax(threshold, regime)

    assert actual_tax == expected_tax


@pytest.mark.parametrize(
    "regime,threshold,marginal_rate",
    [
        ("new_regime", 400000, 0.05),
        ("new_regime", 800000, 0.10),
        ("new_regime", 1200000, 0.15),
        ("new_regime", 1600000, 0.20),
        ("new_regime", 2000000, 0.25),
        ("new_regime", 2400000, 0.30),
        ("old_regime", 250000, 0.05),
        ("old_regime", 500000, 0.20),
        ("old_regime", 1000000, 0.30),
    ],
)
def test_tax_increases_correctly_above_slab_threshold(
    regime,
    threshold,
    marginal_rate,
):
    tax_at_threshold = calculate_slab_tax(
        threshold,
        regime,
    )

    tax_one_rupee_above = calculate_slab_tax(
        threshold + 1,
        regime,
    )

    expected_increment = marginal_rate

    assert tax_one_rupee_above - tax_at_threshold == pytest.approx(
        expected_increment,
        abs=0.01,
    )


@pytest.mark.parametrize(
    "regime,standard_deduction",
    [
        ("new_regime", 75000),
        ("old_regime", 50000),
    ],
)
def test_standard_deduction_applied_correctly(
    regime,
    standard_deduction,
):
    salary = 1000000

    result = calculate_full_tax(salary, regime)

    assert result["standard_deduction"] == standard_deduction
    assert result["taxable_income"] == salary - standard_deduction


def test_new_regime_rebate_threshold():
    salary = 1200000 + 75000

    result = calculate_full_tax(
        salary,
        "new_regime",
    )

    assert result["taxable_income"] == 1200000
    assert result["total_tax"] == 0


def test_old_regime_rebate_threshold():
    salary = 500000 + 50000

    result = calculate_full_tax(
        salary,
        "old_regime",
    )

    assert result["taxable_income"] == 500000
    assert result["total_tax"] == 0


@pytest.mark.parametrize(
    "regime,standard_deduction",
    [
        ("new_regime", 75000),
        ("old_regime", 50000),
    ],
)
def test_taxable_income_never_negative_for_low_salary(
    regime,
    standard_deduction,
):
    result = calculate_full_tax(
        10000,
        regime,
    )

    assert result["taxable_income"] == 0
    assert result["total_tax"] == 0
