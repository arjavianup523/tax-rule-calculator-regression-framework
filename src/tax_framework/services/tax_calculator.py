from src.tax_framework.services.rule_loader import load_tax_rules


def calculate_slab_tax(taxable_income, regime):
    """
    Calculate income tax using progressive tax slabs.

    taxable_income: Income after applicable deductions.
    regime: 'old_regime' or 'new_regime'.
    """

    if taxable_income < 0:
        raise ValueError("Taxable income cannot be negative.")

    rules = load_tax_rules()

    if regime not in rules["tax_slabs"]:
        raise ValueError(f"Unsupported tax regime: {regime}")

    slabs = rules["tax_slabs"][regime]

    total_tax = 0
    previous_limit = 0

    for slab in slabs:
        upper_limit = slab["up_to"]
        rate = slab["rate"]

        if upper_limit is None:
            taxable_amount = taxable_income - previous_limit
        else:
            taxable_amount = min(
                max(taxable_income - previous_limit, 0),
                upper_limit - previous_limit
            )

        total_tax += taxable_amount * rate

        if upper_limit is None or taxable_income <= upper_limit:
            break

        previous_limit = upper_limit

    return round(total_tax, 2)