# Tax Rule Calculator & Regression Testing Framework

## 1. Project Overview

The Tax Rule Calculator & Regression Testing Framework is a financial software quality assurance system designed to validate Indian individual income tax calculations and detect calculation errors introduced by changes in tax rules or software releases.

The system simulates an internal tax validation platform used by financial institutions, fintech companies, and tax software providers.

## 2. Business Problem

Tax software must be updated whenever tax regulations or calculation logic change.

These updates may unintentionally introduce calculation errors, potentially affecting thousands of customers.

Organizations need a reliable mechanism to:

- Validate tax calculations against approved expected results.
- Detect incorrect calculations before software releases.
- Identify calculation discrepancies.
- Maintain historical test results.
- Track changes in tax rules and calculation logic.

## 3. Business Objective

Develop a configurable tax calculation and regression testing framework that automatically validates tax calculations and identifies discrepancies following software or tax rule changes.

## 4. Project Scope

### Included

- Indian individual income tax.
- Financial Year 2025–26.
- Assessment Year 2026–27.
- Old and new tax regimes.
- Salary income calculations.
- Standard deduction.
- Applicable tax slabs and rebates.
- Automated calculation validation.
- Regression testing.
- Exception tracking.
- Tax rule version management.
- Audit history.
- Excel reporting.
- Interactive dashboard.

### Excluded from Initial Version

- Corporate income tax.
- Capital gains tax.
- Cryptocurrency taxation.
- Complex special-rate income.
- Tax return filing.
- Direct integration with government tax systems.

## 5. Primary Users

- Tax Analysts
- Business Analysts
- Quality Assurance Analysts
- Financial Analysts
- Financial Software Development Teams

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Calculate taxable income from eligible salary inputs. |
| FR-02 | Calculate tax under the old and new regimes. |
| FR-03 | Apply configured tax slabs and deductions. |
| FR-04 | Apply eligible rebates and cess. |
| FR-05 | Validate calculation inputs. |
| FR-06 | Compare actual tax results against approved expected results. |
| FR-07 | Execute automated regression test cases. |
| FR-08 | Identify calculation discrepancies. |
| FR-09 | Record tax rule versions and test execution history. |
| FR-10 | Generate calculation and regression reports. |
| FR-11 | Track failed test cases and exceptions. |
| FR-12 | Display testing metrics through a dashboard. |

## 7. Non-Functional Requirements

- Calculation accuracy.
- Maintainable modular architecture.
- Reproducible test results.
- Configurable tax rules.
- Automated testing.
- Traceable calculation outputs.
- Reliable error handling.
- Clear documentation.

## 8. Success Criteria

The project will be considered successful when:

- Both tax regimes produce validated results.
- Tax rules can be updated without rewriting the calculation engine.
- Regression tests detect deliberately introduced calculation errors.
- Failed calculations are recorded and reported.
- Historical test results remain accessible.
- Reports can be exported to Excel.
- The application can be demonstrated through a working interface.

## 9. Technology Stack

- Python
- Pandas
- SQL / SQLite
- Pytest
- Streamlit
- OpenPyXL
- Git and GitHub

## 10. Project Disclaimer

This project is an educational portfolio demonstration of financial calculation validation and software testing. It is not intended to provide official tax advice, file tax returns, or replace professional tax software.