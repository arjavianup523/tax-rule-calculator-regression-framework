
import pytest

from src.tax_framework.services.full_tax_service import (
    calculate_full_tax,
    _round_tax_payable,
)


# ============================================================
# NEW REGIME TESTS
# ============================================================

def test_new_regime_salary_12_75_lakh_has_zero_tax():
    result = calculate_full_tax(1275000, "new_regime")

    assert result["taxable_income"] == 1200000
    assert result["total_tax"] == 0


def test_new_regime_marginal_relief():
    result = calculate_full_tax(1285000, "new_regime")

    assert result["taxable_income"] == 1210000
    assert result["marginal_relief"] == 51500
    assert result["tax_after_rebate"] == 10000
    assert result["cess"] == 400
    assert result["total_tax"] == 10400


# ============================================================
# OLD REGIME TESTS
# ============================================================

def test_old_regime_salary_5_5_lakh_rebate():
    result = calculate_full_tax(550000, "old_regime")

    assert result["taxable_income"] == 500000
    assert result["rebate"] == 12500
    assert result["total_tax"] == 0


def test_old_regime_salary_10_lakh():
    result = calculate_full_tax(1000000, "old_regime")

    assert result["taxable_income"] == 950000
    assert result["tax_before_rebate"] == 102500
    assert result["rebate"] == 0
    assert result["tax_after_rebate"] == 102500
    assert result["cess"] == 4100
    assert result["total_tax"] == 106600


# ============================================================
# VALIDATION TESTS
# ============================================================

def test_zero_salary():
    result = calculate_full_tax(0, "new_regime")

    assert result["taxable_income"] == 0
    assert result["total_tax"] == 0


def test_negative_salary_rejected():
    with pytest.raises(ValueError):
        calculate_full_tax(-1000, "new_regime")


def test_invalid_regime_rejected():
    with pytest.raises(ValueError):
        calculate_full_tax(1000000, "invalid_regime")


# ============================================================
# SECTION 288B TAX ROUNDING TESTS
# ============================================================

@pytest.mark.parametrize(
    "amount, expected",
    [
        (1231, 1230),
        (1234, 1230),
        (1235, 1240),
        (1239, 1240),
        (1234.99, 1230),
        (1235.99, 1240),
        (1000, 1000),
        (0, 0),
    ],
)
def test_tax_payable_rounding(amount, expected):
    assert _round_tax_payable(amount) == expected
