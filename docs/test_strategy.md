# Test Strategy
## Tax Rule Calculator & Regression Testing Framework

## 1. Purpose

This document defines the testing approach used to validate tax calculations, identify defects, and ensure that changes to tax rules or application logic do not introduce calculation errors.

## 2. Testing Objectives

- Verify the accuracy of tax calculations.
- Validate tax rules against independently verified reference results.
- Detect errors introduced by software updates.
- Identify calculation discrepancies.
- Validate boundary conditions and exceptional scenarios.
- Maintain reliable historical regression test results.

## 3. Testing Scope

The initial testing scope includes:

- Indian individual income tax.
- FY 2025–26.
- AY 2026–27.
- Old and new tax regimes.
- Salary income.
- Standard deduction.
- Applicable tax slabs.
- Rebate eligibility.
- Marginal relief.
- Health and education cess.

## 4. Testing Types

### 4.1 Unit Testing

Test individual functions independently.

Examples:
- Taxable income calculation.
- Progressive tax calculation.
- Rebate calculation.
- Cess calculation.

### 4.2 Boundary Testing

Test values immediately below, at, and above important thresholds.

Examples:
- Tax slab boundaries.
- Standard deduction boundaries.
- Rebate eligibility thresholds.
- Marginal relief thresholds.

### 4.3 Regression Testing

Re-execute previously approved test cases after changes to tax rules or calculation logic.

Expected behavior:
- Previously valid results remain unchanged unless a documented rule change justifies the difference.
- Unexpected differences are recorded as failures.

### 4.4 Negative Testing

Validate invalid inputs and unsupported scenarios.

Examples:
- Negative salary.
- Invalid tax regime.
- Missing income.
- Non-numeric input.
- Invalid configuration.

### 4.5 Integration Testing

Verify that the tax engine, configuration loader, database, regression engine, and reporting components work together correctly.

### 4.6 Mutation Testing

Deliberately introduce calculation errors to verify that the regression framework detects them.

Examples:
- Incorrect tax slab rate.
- Incorrect deduction.
- Incorrect rebate limit.
- Incorrect cess percentage.

## 5. Test Case Structure

Each test case should contain:

- Test Case ID
- Test Description
- Financial Year
- Tax Regime
- Input Salary
- Expected Taxable Income
- Expected Tax
- Actual Tax
- Difference
- Test Status
- Reference Source

## 6. Test Result Classification

### PASS
Actual result matches the independently validated expected result within the defined tolerance.

### FAIL
Actual result differs from the expected result beyond the permitted tolerance.

### ERROR
The test could not execute because of an unexpected application error.

### BLOCKED
The test cannot execute because a prerequisite or required reference result is unavailable.

## 7. Regression Testing Workflow

1. Load approved regression test cases.
2. Execute calculations using the current tax rules.
3. Compare actual and expected results.
4. Identify discrepancies.
5. Classify failed tests.
6. Record test execution history.
7. Generate a regression report.
8. Investigate failures before approving a software release.

## 8. Test Coverage Requirements

The initial release should include:

- Normal calculation scenarios.
- Tax slab boundary scenarios.
- Rebate eligibility scenarios.
- Marginal relief scenarios.
- Invalid input scenarios.
- Old and new regime comparisons.
- Regression tests for previously validated calculations.

## 9. Quality Acceptance Criteria

The framework will be considered acceptable when:

- All critical tax calculation tests pass.
- Tax calculations are validated against independent references.
- Regression tests identify deliberately introduced calculation defects.
- Invalid inputs are handled correctly.
- Test execution results are reproducible.
- Failed test cases can be investigated.
- Reports accurately summarize testing outcomes.

## 10. Testing Tools

- Pytest
- Python
- SQLite
- Pandas
- OpenPyXL

## 11. Limitations

Testing results depend on the accuracy and completeness of the configured tax rules and independent reference calculations.

The application is an educational portfolio project and is not a substitute for official tax software or professional tax advice.