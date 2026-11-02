# System Architecture
## Tax Rule Calculator & Regression Testing Framework

## 1. Architecture Overview

The application follows a modular architecture that separates tax calculation logic, business rules, regression testing, data storage, and reporting.

This separation allows tax rules to be updated without unnecessarily modifying the calculation engine or testing framework.

## 2. High-Level Architecture

### Layer 1: User Interface

Technology: Streamlit

Responsibilities:
- Accept salary and taxpayer information.
- Allow selection of tax regimes.
- Display calculation results.
- Trigger regression test execution.
- Display test failures and exceptions.
- Provide access to reports.

### Layer 2: Application Services

Technology: Python

Components:
- Tax Calculation Service
- Input Validation Service
- Regression Testing Service
- Exception Management Service
- Reporting Service

Responsibilities:
- Coordinate calculation workflows.
- Validate incoming requests.
- Execute tax calculations.
- Compare expected and actual results.
- Record calculation and testing outcomes.

### Layer 3: Business Logic

Technology: Python

Components:

#### Tax Calculation Engine
- Calculate taxable income.
- Apply standard deductions.
- Apply progressive tax slabs.
- Calculate eligible rebates.
- Apply cess.
- Return detailed calculation breakdowns.

#### Tax Rule Configuration Engine
- Load tax rules from configuration files.
- Identify financial year and assessment year.
- Maintain configurable tax parameters.
- Support future tax rule versions.

#### Regression Testing Engine
- Load approved test cases.
- Execute calculations against existing scenarios.
- Compare expected and actual results.
- Identify failed test cases.
- Produce regression summaries.

#### Validation Engine
- Validate salary inputs.
- Reject invalid or unsupported values.
- Check calculation assumptions.
- Validate test case integrity.

### Layer 4: Data Storage

Technology: SQLite

Initial tables:

- tax_rule_versions
- calculation_runs
- regression_test_cases
- regression_test_runs
- regression_test_results
- calculation_exceptions
- audit_events

Responsibilities:
- Store tax rule versions.
- Maintain approved test scenarios.
- Record historical test executions.
- Store calculation discrepancies.
- Maintain audit history.

### Layer 5: Reporting

Technologies:
- Pandas
- OpenPyXL
- Streamlit

Outputs:
- Tax Calculation Report
- Regression Test Summary
- Failed Test Case Report
- Exception Report
- Tax Rule Change Report

## 3. Application Workflow

### Tax Calculation Workflow

1. User enters taxpayer information.
2. Input validation checks the submitted data.
3. Tax rule configuration is loaded.
4. Taxable income is calculated.
5. Applicable tax slabs are applied.
6. Rebate and cess are calculated.
7. The calculation result is returned.
8. Calculation history is recorded.
9. Results are displayed and optionally exported.

### Regression Testing Workflow

1. Analyst selects a tax rule version or software release.
2. The framework loads approved regression test cases.
3. Each test case is executed against the current calculation engine.
4. Actual results are compared against expected results.
5. Passing and failing tests are identified.
6. Failed cases are recorded as exceptions.
7. The testing execution is stored in the database.
8. A regression report is generated.

## 4. Regression Testing Strategy

The framework will support:

### Baseline Testing
Validate calculations against approved reference results.

### Boundary Testing
Test values immediately below, at, and above tax slab thresholds.

### Rule Change Testing
Verify the impact of modified tax rules.

### Negative Testing
Validate invalid or unsupported inputs.

### Historical Regression Testing
Re-run previously approved test cases after software changes.

## 5. Exception Management

Each failed calculation or regression test should contain:

- Exception ID
- Test case ID
- Tax regime
- Financial year
- Expected result
- Actual result
- Difference
- Exception category
- Execution timestamp
- Resolution status

## 6. Design Principles

- Separation of concerns.
- Configurable business rules.
- Reproducible calculations.
- Automated quality assurance.
- Traceability.
- Maintainability.
- Extensibility.

## 7. Future Enhancements

- Additional taxpayer categories.
- Multiple financial years.
- More income sources.
- Advanced tax scenarios.
- Role-based access.
- API integration.
- Automated release validation.
- Enhanced audit and compliance reporting.