
import streamlit as st
import pandas as pd

from src.tax_framework.testing.regression_runner import (
    run_regression_suite,
)
from src.tax_framework.reporting.excel_report import (
    generate_excel_report,
)
from src.tax_framework.database.audit_database import (
    get_regression_history,
    get_open_defects,
)
from src.tax_framework.services.release_gate import (
    evaluate_release,
)


st.set_page_config(
    page_title="Tax QA & Regression Framework",
    page_icon="🧾",
    layout="wide",
)

st.title("Tax Rule Calculator & Regression Testing Framework")

st.caption(
    "Automated tax calculation validation, regression testing, "
    "and financial software quality assurance."
)

st.info("Tax configuration: FY 2025–26 | AY 2026–27")


# Session state
if "results" not in st.session_state:
    st.session_state.results = []

if "summary" not in st.session_state:
    st.session_state.summary = None

if "release_decision" not in st.session_state:
    st.session_state.release_decision = None


# Regression execution
st.subheader("Regression Test Execution")

if st.button("Run Regression Suite", type="primary"):

    with st.spinner("Executing regression tests..."):

        try:
            runner_output = run_regression_suite()

            if not isinstance(runner_output, (tuple, list)):
                raise TypeError(
                    "Regression runner must return a tuple or list."
                )

            if len(runner_output) < 2:
                raise ValueError(
                    "Regression runner must return results and summary."
                )

            results = runner_output[0]
            summary = runner_output[1]

            decision = evaluate_release(results, summary)

            st.session_state.results = results
            st.session_state.summary = summary
            st.session_state.release_decision = decision

            st.success("Regression suite execution completed.")

        except Exception as error:
            st.error(f"Regression execution failed: {error}")


# Execution summary
results = st.session_state.results
summary = st.session_state.summary
decision = st.session_state.release_decision


if summary:

    st.subheader("Latest Execution Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Cases", summary.get("total", 0))
    col2.metric("Passed", summary.get("passed", 0))
    col3.metric("Failed", summary.get("failed", 0))
    col4.metric("Errors", summary.get("errors", 0))

    if summary.get("overall_status") == "PASS":
        st.success("Regression Status: PASS")
    else:
        st.error(
            f"Regression Status: "
            f"{summary.get('overall_status', 'UNKNOWN')}"
        )


# Release gate
if decision:

    st.subheader("Automated Release Gate")

    if decision["release_approved"]:
        st.success("RELEASE APPROVED")
    else:
        st.error("RELEASE BLOCKED")

    st.write(decision["reason"])

    gate_col1, gate_col2, gate_col3 = st.columns(3)

    gate_col1.metric(
        "Release Decision",
        decision["release_status"],
    )

    gate_col2.metric(
        "Failed Tests",
        decision["failed_cases"],
    )

    gate_col3.metric(
        "Test Errors",
        decision["error_cases"],
    )


# Detailed results
if results:

    st.subheader("Detailed Regression Results")

    results_df = pd.DataFrame(results)

    st.dataframe(
        results_df,
        width="stretch",
        hide_index=True,
    )

    if summary:

        if st.button("Generate Excel Report"):

            try:
                report_path = generate_excel_report(
                    results,
                    summary,
                )

                with open(report_path, "rb") as report_file:

                    st.download_button(
                        label="Download Excel Report",
                        data=report_file,
                        file_name=report_path.name,
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                    )

            except Exception as error:
                st.error(
                    f"Excel report generation failed: {error}"
                )


# Defect tracking
st.divider()
st.subheader("Open Defects")

try:

    defects = get_open_defects()

    if defects:

        defects_df = pd.DataFrame(defects)

        st.dataframe(
            defects_df,
            width="stretch",
            hide_index=True,
        )

    else:
        st.success("No open defects currently recorded.")

except Exception as error:

    st.error(
        f"Unable to retrieve defects: {error}"
    )


# Regression history
st.divider()
st.subheader("Regression Execution History")

try:

    history = get_regression_history()

    if history:

        history_df = pd.DataFrame(history)

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True,
        )

    else:
        st.info("No regression history available yet.")

except Exception as error:

    st.error(
        f"Unable to retrieve regression history: {error}"
    )


# Footer
st.divider()

st.caption(
    "Internal financial software QA prototype. "
    "Tax calculations require independent verification "
    "against applicable official tax rules."
)
