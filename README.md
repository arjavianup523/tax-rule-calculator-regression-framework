
# Tax Rule Calculator & Regression Testing Framework

A Python-based tax calculation and quality assurance framework designed to calculate Indian individual salary income tax, validate tax rules, detect calculation regressions, and maintain auditable test results.

## Project Overview

This project demonstrates how financial calculations can be supported by automated testing, rule-driven configuration, regression validation, and audit-oriented reporting.

It combines tax calculation logic with software quality engineering practices to help identify calculation defects before releasing updated tax rules.

## Key Features

- Rule-driven tax calculation using JSON configuration
- Old and new tax regime calculations
- Standard deduction handling
- Section 87A rebate calculations
- New-regime marginal relief
- Health and Education Cess calculation
- Tax payable rounding under Section 288B
- Automated regression testing using pytest
- Approved baseline tax cases
- Defect tracking and audit-oriented validation
- Excel-based reporting
- Release validation workflow
- Streamlit dashboard for interactive review

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Tax calculation and application logic |
| pytest | Automated testing and regression validation |
| JSON | Tax rules and approved test cases |
| SQLite | Audit and validation data storage |
| pandas | Data processing |
| openpyxl | Excel report generation |
| Streamlit | Interactive dashboard |

## Project Architecture

```text
Tax_Rule_Calculator_Regression_Framework/
│
├── config/
│   └── tax_rules_fy2025_26.json
│
├── data/
│   └── approved_tax_cases.json
│
├── src/
│   └── tax_framework/
│       └── services/
│           ├── tax_calculator.py
│           ├── full_tax_service.py
│           ├── rule_loader.py
│           └── test_full_tax_service.py
│
├── app.py
├── README.md
└── requirements.txt
```

Additional modules support regression execution, audit logging, reporting, release validation, and defect tracking.

## Tax Calculation Scope

The current implementation covers:

- Financial Year: 2025–26
- Assessment Year: 2026–27
- Country: India
- Taxpayer: Resident individual below 60 years
- Income source: Salary income
- Tax regimes: Old and new

### Supported Tax Rules

- Standard deduction
- Income tax slab calculation
- Section 87A rebate
- New-regime marginal relief
- 4% Health and Education Cess
- Final tax payable rounding

Tax rules are maintained separately in JSON configuration to support controlled rule updates.

## Installation

Clone the repository:

```bash
git clone https://github.com/arjavianup523/Tax_Rule_Calculator_Regression_Framework.git
```

Navigate to the project directory:

```bash
cd Tax_Rule_Calculator_Regression_Framework
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Automated Tests

Execute the complete test suite:

```bash
python -m pytest -v
```

The latest verified test run completed with:

**61 tests passed**

The test suite covers tax calculations, validation scenarios, rebate handling, marginal relief, and tax rounding.

## Launch the Dashboard

Run the Streamlit application:

```bash
python -m streamlit run app.py
```

The dashboard provides an interactive interface for reviewing tax calculations and project validation results.

## Quality Assurance Approach

The framework follows a structured validation process:

1. Load tax rules from configuration.
2. Calculate tax using the configured rules.
3. Validate outputs against approved test cases.
4. Execute automated regression tests.
5. Record validation and audit information.
6. Generate reports for review.
7. Evaluate release readiness.

## Important Limitations

This is an educational and portfolio-oriented software engineering project.

The current implementation is limited to the configured taxpayer profile and salary income scenarios. It is not a comprehensive tax filing application and does not replace professional tax advice.

Tax rules should be independently verified against applicable official legislation before being used for actual tax decisions.

## Author

**Arjavi Shetye**

GitHub: [arjavianup523](https://github.com/arjavianup523)
