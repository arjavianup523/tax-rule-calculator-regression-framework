from src.tax_framework.services.rule_loader import load_tax_rules
from src.tax_framework.services.tax_calculator import calculate_slab_tax


def _round_tax_payable(amount):
    """
    Round tax payable to the nearest Rs. 10.

    Paise are ignored before rounding, consistent with
    Section 288B of the Income-tax Act, 1961.
    """
    whole_rupees = int(amount)
    remainder = whole_rupees % 10

    if remainder >= 5:
        return whole_rupees + (10 - remainder)

    return whole_rupees - remainder


def calculate_full_tax(gross_salary, regime):
    """
    Calculate simplified annual salary tax for a resident
    individual below age 60 for AY 2026-27.

    Scope:
    - Salary income
    - Standard deduction
    - Section 87A rebate
    - New-regime marginal relief
    - 4% Health and Education Cess
    - Section 288B rounding of final tax payable
    """

    if gross_salary < 0:
        raise ValueError("Gross salary cannot be negative.")

    if regime not in ("old_regime", "new_regime"):
        raise ValueError(f"Unsupported tax regime: {regime}")

    rules = load_tax_rules()

    # 1. Standard deduction
    standard_deduction = min(
        gross_salary,
        rules["standard_deduction"][regime]
    )

    taxable_income = max(
        gross_salary - standard_deduction,
        0
    )

    # 2. Slab tax
    tax_before_rebate = calculate_slab_tax(
        taxable_income,
        regime
    )

    # 3. Section 87A rebate
    rebate_rules = rules["rebate_87a"][regime]

    income_limit = rebate_rules["income_limit"]
    maximum_rebate = rebate_rules["maximum_rebate"]

    rebate = 0

    if taxable_income <= income_limit:
        rebate = min(
            tax_before_rebate,
            maximum_rebate
        )

    # 4. New-regime marginal relief
    marginal_relief = 0

    if regime == "new_regime" and taxable_income > income_limit:
        tax_exceeding_limit = taxable_income - income_limit

        if tax_before_rebate > tax_exceeding_limit:
            marginal_relief = (
                tax_before_rebate - tax_exceeding_limit
            )

            rebate = max(
                rebate,
                marginal_relief
            )

    rebate = min(
        rebate,
        tax_before_rebate
    )

    # 5. Tax after rebate
    tax_after_rebate = max(
        tax_before_rebate - rebate,
        0
    )

    # 6. Health and Education Cess
    cess = tax_after_rebate * rules["cess_rate"]

    # 7. Final tax payable rounded to nearest Rs. 10
    tax_before_rounding = tax_after_rebate + cess

    total_tax = _round_tax_payable(
        tax_before_rounding
    )

    return {
        "gross_salary": gross_salary,
        "regime": regime,
        "standard_deduction": standard_deduction,
        "taxable_income": taxable_income,
        "tax_before_rebate": round(tax_before_rebate, 2),
        "rebate": round(rebate, 2),
        "marginal_relief": round(marginal_relief, 2),
        "tax_after_rebate": round(tax_after_rebate, 2),
        "cess": round(cess, 2),
        "total_tax": total_tax
    }