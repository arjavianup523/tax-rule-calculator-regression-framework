import pytest

from src.tax_framework.services.tax_calculator import (
    calculate_slab_tax
)


def test_new_regime_tax_on_10_lakh():
    assert calculate_slab_tax(
        1000000, "new_regime"
    ) == 40000


def test_new_regime_tax_on_25_lakh():
    assert calculate_slab_tax(
        2500000, "new_regime"
    ) == 330000


def test_old_regime_tax_on_10_lakh():
    assert calculate_slab_tax(
        1000000, "old_regime"
    ) == 112500


def test_zero_income():
    assert calculate_slab_tax(
        0, "new_regime"
    ) == 0


def test_negative_income_rejected():
    with pytest.raises(ValueError):
        calculate_slab_tax(-1000, "new_regime")


def test_invalid_regime_rejected():
    with pytest.raises(ValueError):
        calculate_slab_tax(1000000, "invalid_regime")