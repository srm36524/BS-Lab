import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.set_page_config(
    page_title="Business Statistics Lab - Part 6",
    page_icon="📊",
    layout="wide"
)

if st.button("🏠 Return to Home"):
    st.switch_page("home.py")

st.title("📊 Business Statistics Learning Lab")
st.subheader("Part 6: Statistical Distribution Tables")

st.markdown("""
Interactive reference tables for students learning hypothesis testing.

Explore Z, t, chi-square and F distributions, calculate critical values,
and understand how statistical tables support hypothesis testing.
""")

# ==========================================================
# SIDEBAR
# ==========================================================

distribution = st.sidebar.selectbox(
    "Select a distribution table",
    [
        "Standard Normal Z-Table",
        "Student's t-Table",
        "Chi-Square Table",
        "F-Distribution Table",
        "Probability Calculator"
    ]
)

# ==========================================================
# COMMON FUNCTIONS
# ==========================================================

def format_number(value, decimals=4):
    if not np.isfinite(value):
        return "∞" if value > 0 else "-∞"
    return f"{value:.{decimals}f}"


def show_interpretation():
    st.info("""
    **How to use a critical value**

    For a right-tailed test, reject H₀ if the calculated statistic
    is greater than the upper critical value.

    For a left-tailed test, reject H₀ if the calculated statistic
    is less than the lower critical value.

    For a two-tailed test, reject H₀ if the calculated statistic
    lies outside the two critical values.

    These rules apply when the selected test and assumptions are appropriate.
    """)


def make_levels():
    return [0.20, 0.10, 0.05, 0.025, 0.01, 0.005, 0.001]


# ==========================================================
# 1. Z TABLE
# ==========================================================

if distribution == "Standard Normal Z-Table":

    st.header("1. Standard Normal Distribution — Z-Table")

    st.markdown("""
    The standard normal distribution has mean 0 and standard deviation 1.

    This table displays the cumulative probability:

    **P(Z ≤ z)**

    It gives the area under the normal curve to the left of the selected Z-score.
    """)

    table_type = st.radio(
        "Choose table format",
        [
            "Cumulative probability P(Z ≤ z)",
            "Area between 0 and positive Z",
            "Upper-tail probability P(Z > z)"
        ]
    )

    st.markdown("### Select a Z-score")

    col1, col2, col3 = st.columns(3)

    with col1:
        z_start = st.number_input(
            "Starting Z-score",
            min_value=-4.0,
            max_value=3.9,
            value=0.0,
            step=0.1
        )

    with col2:
        z_end = st.number_input(
            "Ending Z-score",
            min_value=-3.9,
            max_value=4.0,
            value=2.0,
            step=0.1
        )

    with col3:
        increment = st.selectbox(
            "Increment",
            [0.01, 0.1, 0.2]
        )

    if z_start > z_end:
        st.error("The starting Z-score must not exceed the ending Z-score.")

    else:
        z_values = np.round(
            np.arange(z_start, z_end + increment / 2, increment),
            4
        )

        if len(z_values) > 1000:
            st.error("Please select a smaller range or larger increment.")

        else:
            if table_type == "Cumulative probability P(Z ≤ z)":
                probabilities = stats.norm.cdf(z_values)
                column_name = "P(Z ≤ z)"

            elif table_type == "Area between 0 and positive Z":
                probabilities = np.where(
                    z_values >= 0,
                    stats.norm.cdf(z_values) - 0.5,
                    np.nan
                )
                column_name = "Area from 0 to Z"

            else:
                probabilities = stats.norm.sf(z_values)
                column_name = "P(Z > z)"

            table = pd.DataFrame({
                "Z-score": z_values,
                column_name: probabilities
            })

            st.dataframe(
                table.round(5),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download Z-table as CSV",
                table.to_csv(index=False),
                file_name="z_table.csv",
                mime="text/csv"
            )

    st.divider()

    st.subheader("Calculate a Z critical value")

    alpha = st.selectbox(
        "Significance level",
        make_levels(),
        index=2,
        format_func=lambda x: f"{x:.3f} ({x*100:g}%)"
    )

    tail = st.radio(
        "Test type",
        ["Right-tailed", "Left-tailed", "Two-tailed"],
        horizontal=True
    )

    if tail == "Right-tailed":
        critical = stats.norm.ppf(1 - alpha)
        st.metric("Upper critical Z", f"{critical:.5f}")
        st.write(f"Upper-tail area = {alpha:.5f}")

    elif tail == "Left-tailed":
        critical = stats.norm.ppf(alpha)
        st.metric("Lower critical Z", f"{critical:.5f}")
        st.write(f"Lower-tail area = {alpha:.5f}")

    else:
        critical = stats.norm.ppf(1 - alpha / 2)

        c1, c2 = st.columns(2)
        c1.metric("Lower critical Z", f"{-critical:.5f}")
        c2.metric("Upper critical Z", f"{critical:.5f}")

        st.write(f"Area in each tail = {alpha/2:.5f}")

    st.markdown("### Example")

    st.write("""
    At a 5% significance level:

    - Right-tailed critical Z ≈ 1.645
    - Left-tailed critical Z ≈ −1.645
    - Two-tailed critical Z ≈ ±1.960

    The correct critical value depends on the alternative hypothesis.
    """)

# ==========================================================
# 2. STUDENT'S t TABLE
# ==========================================================

elif distribution == "Student's t-Table":

    st.header("2. Student's t-Distribution Table")

    st.markdown("""
    The t-distribution is commonly used when testing a population mean
    with an unknown population standard deviation.

    Critical values depend on both the degrees of freedom and the
    significance level.
    """)

    df = st.number_input(
        "Degrees of freedom",
        min_value=1,
        max_value=10000,
        value=10,
        step=1
    )

    alpha = st.selectbox(
        "Significance level",
        make_levels(),
        index=2,
        format_func=lambda x: f"{x:.3f} ({x*100:g}%)"
    )

    tail = st.radio(
        "Test type",
        ["Right-tailed", "Left-tailed", "Two-tailed"],
        horizontal=True
    )

    if tail == "Right-tailed":
        critical = stats.t.ppf(1 - alpha, df)
        st.metric("Upper critical t", f"{critical:.5f}")
        st.latex(r"t_{\text{critical}}=t_{1-\alpha,\,df}")

    elif tail == "Left-tailed":
        critical = stats.t.ppf(alpha, df)
        st.metric("Lower critical t", f"{critical:.5f}")
        st.latex(r"t_{\text{critical}}=t_{\alpha,\,df}")

    else:
        critical = stats.t.ppf(1 - alpha / 2, df)

        c1, c2 = st.columns(2)
        c1.metric("Lower critical t", f"{-critical:.5f}")
        c2.metric("Upper critical t", f"{critical:.5f}")

        st.latex(r"t_{\text{critical}}=\pm t_{1-\alpha/2,\,df}")

    st.divider()

    st.subheader("Generate a t-distribution table")

    df_values_text = st.text_input(
        "Degrees of freedom to include, separated by commas",
        "1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 60, 120"
    )

    try:
        df_values = sorted(
            set(
                int(item.strip())
                for item in df_values_text.split(",")
                if item.strip()
            )
        )

        if not df_values or any(v < 1 for v in df_values):
            raise ValueError

        if len(df_values) > 100:
            st.error("Enter no more than 100 degrees-of-freedom values.")
            df_values = []

    except ValueError:
        st.error("Enter valid positive integer degrees of freedom.")
        df_values = []

    if df_values:
        levels = st.multiselect(
            "Select upper-tail probabilities",
            make_levels(),
            default=[0.10, 0.05, 0.025, 0.01]
        )

        if levels:
            rows = []

            for d in df_values:
                row = {"Degrees of freedom": d}

                for a in levels:
                    row[f"Upper-tail α={a:g}"] = stats.t.ppf(1 - a, d)
                    row[f"Two-tail α={2*a:g}"] = stats.t.ppf(1 - a, d)

                rows.append(row)

            t_table = pd.DataFrame(rows)

            st.dataframe(
                t_table.round(4),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download t-table as CSV",
                t_table.to_csv(index=False),
                file_name="t_table.csv",
                mime="text/csv"
            )

    show_interpretation()

# ==========================================================
# 3. CHI-SQUARE TABLE
# ==========================================================

elif distribution == "Chi-Square Table":

    st.header("3. Chi-Square Distribution Table")

    st.markdown("""
    Chi-square critical values are used in goodness-of-fit tests,
    tests of independence and other procedures involving chi-square statistics.

    This page displays **upper-tail critical values**:

    P(χ² > critical value) = α
    """)

    df = st.number_input(
        "Degrees of freedom",
        min_value=1,
        max_value=10000,
        value=4,
        step=1
    )

    alpha = st.selectbox(
        "Upper-tail significance level",
        make_levels(),
        index=2,
        format_func=lambda x: f"{x:.3f} ({x*100:g}%)"
    )

    critical = stats.chi2.isf(alpha, df)

    st.metric("Upper-tail critical chi-square", f"{critical:.5f}")

    st.latex(
        r"P(\chi^2>\chi^2_{\text{critical}})=\alpha"
    )

    st.write(f"Degrees of freedom = {df}")
    st.write(f"Upper-tail probability = {alpha:.5f}")

    st.divider()

    st.subheader("Generate a chi-square table")

    df_values_text = st.text_input(
        "Degrees of freedom to include",
        "1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 40, 50"
    )

    try:
        df_values = sorted(
            set(
                int(item.strip())
                for item in df_values_text.split(",")
                if item.strip()
            )
        )

        if not df_values or any(v < 1 for v in df_values):
            raise ValueError

        if len(df_values) > 100:
            st.error("Enter no more than 100 degrees-of-freedom values.")
            df_values = []

    except ValueError:
        st.error("Enter valid positive integer degrees of freedom.")
        df_values = []

    if df_values:
        levels = st.multiselect(
            "Select upper-tail significance levels",
            make_levels(),
            default=[0.10, 0.05, 0.025, 0.01]
        )

        if levels:
            rows = []

            for d in df_values:
                row = {"Degrees of freedom": d}

                for a in levels:
                    row[f"α = {a:g}"] = stats.chi2.isf(a, d)

                rows.append(row)

            chi_table = pd.DataFrame(rows)

            st.dataframe(
                chi_table.round(4),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download chi-square table as CSV",
                chi_table.to_csv(index=False),
                file_name="chi_square_table.csv",
                mime="text/csv"
            )

    show_interpretation()

# ==========================================================
# 4. F-DISTRIBUTION TABLE
# ==========================================================

elif distribution == "F-Distribution Table":

    st.header("4. F-Distribution Critical Value Table")

    st.markdown("""
    The F-distribution is used in ANOVA and in certain variance tests.

    The critical value depends on:

    - Numerator degrees of freedom
    - Denominator degrees of freedom
    - Upper-tail significance level
    """)

    col1, col2 = st.columns(2)

    with col1:
        df1 = st.number_input(
            "Numerator degrees of freedom (df₁)",
            min_value=1,
            max_value=10000,
            value=2,
            step=1
        )

    with col2:
        df2 = st.number_input(
            "Denominator degrees of freedom (df₂)",
            min_value=1,
            max_value=10000,
            value=12,
            step=1
        )

    alpha = st.selectbox(
        "Upper-tail significance level",
        make_levels(),
        index=2,
        format_func=lambda x: f"{x:.3f} ({x*100:g}%)"
    )

    critical = stats.f.isf(alpha, df1, df2)

    st.metric("Upper critical F-value", f"{critical:.5f}")

    st.latex(
        r"P(F>F_{\text{critical}})=\alpha"
    )

    st.write(f"Numerator df = {df1}")
    st.write(f"Denominator df = {df2}")
    st.write(f"Upper-tail probability = {alpha:.5f}")

    st.divider()

    st.subheader("Generate an F-table")

    numerator_text = st.text_input(
        "Numerator degrees of freedom",
        "1, 2, 3, 4, 5"
    )

    denominator_text = st.text_input(
        "Denominator degrees of freedom",
        "5, 10, 12, 15, 20, 30, 60"
    )

    try:
        numerator_values = sorted(
            set(
                int(item.strip())
                for item in numerator_text.split(",")
                if item.strip()
            )
        )

        denominator_values = sorted(
            set(
                int(item.strip())
                for item in denominator_text.split(",")
                if item.strip()
            )
        )

        if (
            not numerator_values
            or not denominator_values
            or any(v < 1 for v in numerator_values + denominator_values)
        ):
            raise ValueError

        if len(numerator_values) > 50 or len(denominator_values) > 50:
            st.error("Enter no more than 50 values in either list.")
            numerator_values = []
            denominator_values = []

    except ValueError:
        st.error("Enter valid positive integer degrees of freedom.")
        numerator_values = []
        denominator_values = []

    if numerator_values and denominator_values:
        levels = st.multiselect(
            "Select upper-tail significance levels",
            make_levels(),
            default=[0.10, 0.05, 0.01]
        )

        if levels:
            for a in levels:
                st.markdown(f"#### Upper-tail α = {a:g}")

                rows = []

                for d1 in numerator_values:
                    row = {"Numerator df": d1}

                    for d2 in denominator_values:
                        row[f"Denominator df = {d2}"] = stats.f.isf(
                            a, d1, d2
                        )

                    rows.append(row)

                f_table = pd.DataFrame(rows)

                st.dataframe(
                    f_table.round(4),
                    use_container_width=True,
                    hide_index=True
                )

            # Export one selected significance level
            export_alpha = st.selectbox(
                "Significance level for CSV export",
                levels,
                key="f_export_alpha"
            )

            export_rows = []

            for d1 in numerator_values:
                row = {"Numerator df": d1}

                for d2 in denominator_values:
                    row[f"Denominator df = {d2}"] = stats.f.isf(
                        export_alpha, d1, d2
                    )

                export_rows.append(row)

            export_table = pd.DataFrame(export_rows)

            st.download_button(
                "Download selected F-table as CSV",
                export_table.to_csv(index=False),
                file_name="f_table.csv",
                mime="text/csv"
            )

    show_interpretation()

# ==========================================================
# 5. PROBABILITY CALCULATOR
# ==========================================================

elif distribution == "Probability Calculator":

    st.header("5. Statistical Probability Calculator")

    dist_name = st.selectbox(
        "Choose distribution",
        ["Normal", "t", "Chi-square", "F"]
    )

    event = st.selectbox(
        "Choose probability",
        [
            "Left-tail probability",
            "Right-tail probability",
            "Probability between two values"
        ]
    )

    if dist_name == "Normal":

        mu = st.number_input("Mean", value=0.0)
        sigma = st.number_input(
            "Standard deviation",
            min_value=0.0001,
            value=1.0
        )

        def cdf(x):
            return stats.norm.cdf(x, loc=mu, scale=sigma)

        def sf(x):
            return stats.norm.sf(x, loc=mu, scale=sigma)

    elif dist_name == "t":

        df = st.number_input(
            "Degrees of freedom",
            min_value=1,
            max_value=10000,
            value=10
        )

        def cdf(x):
            return stats.t.cdf(x, df)

        def sf(x):
            return stats.t.sf(x, df)

    elif dist_name == "Chi-square":

        df = st.number_input(
            "Degrees of freedom",
            min_value=1,
            max_value=10000,
            value=5
        )

        def cdf(x):
            return stats.chi2.cdf(x, df)

        def sf(x):
            return stats.chi2.sf(x, df)

    else:

        col1, col2 = st.columns(2)

        with col1:
            df1 = st.number_input(
                "Numerator degrees of freedom",
                min_value=1,
                max_value=10000,
                value=5
            )

        with col2:
            df2 = st.number_input(
                "Denominator degrees of freedom",
                min_value=1,
                max_value=10000,
                value=10
            )

        def cdf(x):
            return stats.f.cdf(x, df1, df2)

        def sf(x):
            return stats.f.sf(x, df1, df2)

    if event in ["Left-tail probability", "Right-tail probability"]:

        x = st.number_input(
            "Enter the test statistic or distribution value",
            value=1.5
        )

        result = cdf(x) if event == "Left-tail probability" else sf(x)

        st.metric("Calculated probability", f"{result:.8f}")
        st.write(f"Percentage = {result * 100:.5f}%")

    else:

        col1, col2 = st.columns(2)

        with col1:
            lower = st.number_input(
                "Lower value",
                value=0.0
            )

        with col2:
            upper = st.number_input(
                "Upper value",
                value=2.0
            )

        if lower >= upper:
            st.error("The upper value must exceed the lower value.")

        else:
            result = cdf(upper) - cdf(lower)

            st.metric("Probability between the values", f"{result:.8f}")
            st.write(f"Percentage = {result * 100:.5f}%")

# ==========================================================
# FINAL REVISION
# ==========================================================

st.divider()

st.header("Quick Revision: Which Table Should I Use?")

st.dataframe(
    pd.DataFrame({
        "Distribution": [
            "Z",
            "t",
            "Chi-square",
            "F"
        ],
        "Typical application": [
            "Tests involving normal Z statistics",
            "Tests involving sample means when population SD is unknown",
            "Categorical frequency tests",
            "ANOVA and selected variance procedures"
        ],
        "Required information": [
            "Tail probability or significance level",
            "Degrees of freedom and significance level",
            "Degrees of freedom and tail probability",
            "Numerator df, denominator df and tail probability"
        ]
    }),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Values are calculated using SciPy distribution functions. "
    "Small differences from printed tables may arise from rounding."
)
```
