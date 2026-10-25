```python
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.set_page_config(
    page_title="Business Statistics Lab - Part 4",
    page_icon="📊",
    layout="wide"
)

if st.button("🏠 Return to Home"):
    st.switch_page("home.py")

st.title("📊 Business Statistics Learning Lab")
st.subheader("Part 4: Hypothesis Testing — Z and t Tests")

st.markdown("""
This application demonstrates hypothesis testing step by step.
Edit the sample data and values to explore different results.
""")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

test_type = st.sidebar.selectbox(
    "Select a statistical test",
    [
        "One-Sample Z-Test",
        "Two-Sample Z-Test",
        "One-Sample t-Test",
        "Independent Two-Sample t-Test",
        "Paired t-Test"
    ]
)

alpha = st.sidebar.number_input(
    "Significance level (alpha)",
    min_value=0.001,
    max_value=0.25,
    value=0.05,
    step=0.01,
    format="%.3f"
)

tail = st.sidebar.selectbox(
    "Alternative hypothesis",
    [
        "Two-tailed",
        "Right-tailed",
        "Left-tailed"
    ]
)

st.info(
    f"Significance level α = {alpha:.3f} "
    f"({alpha * 100:.1f}%)"
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def parse_values(text):
    """Convert comma-separated numbers into a NumPy array."""
    try:
        values = np.array(
            [float(x.strip()) for x in text.split(",") if x.strip()],
            dtype=float
        )

        if len(values) == 0 or not np.all(np.isfinite(values)):
            return None

        return values

    except ValueError:
        return None


def alternative_name():
    if tail == "Right-tailed":
        return "greater"
    elif tail == "Left-tailed":
        return "less"
    return "two-sided"


def decision_from_p(p_value):
    if p_value < alpha:
        return "Reject H₀"
    return "Fail to reject H₀"


def interpretation(p_value):
    if p_value < alpha:
        return (
            f"Since p-value ({p_value:.5f}) is less than "
            f"α ({alpha:.3f}), reject the null hypothesis. "
            "The result is statistically significant."
        )

    return (
        f"Since p-value ({p_value:.5f}) is greater than or equal "
        f"to α ({alpha:.3f}), fail to reject the null hypothesis. "
        "The result is not statistically significant."
    )


def show_hypotheses(parameter, value):
    if tail == "Right-tailed":
        st.latex(r"H_0: " + parameter + r" = " + str(value))
        st.latex(r"H_1: " + parameter + r" > " + str(value))
    elif tail == "Left-tailed":
        st.latex(r"H_0: " + parameter + r" = " + str(value))
        st.latex(r"H_1: " + parameter + r" < " + str(value))
    else:
        st.latex(r"H_0: " + parameter + r" = " + str(value))
        st.latex(r"H_1: " + parameter + r" \ne " + str(value))


def z_critical_values(alpha, tail):
    if tail == "Right-tailed":
        return stats.norm.ppf(1 - alpha), None
    elif tail == "Left-tailed":
        return None, stats.norm.ppf(alpha)
    else:
        c = stats.norm.ppf(1 - alpha / 2)
        return c, -c


def t_critical_values(alpha, df, tail):
    if tail == "Right-tailed":
        return stats.t.ppf(1 - alpha, df), None
    elif tail == "Left-tailed":
        return None, stats.t.ppf(alpha, df)
    else:
        c = stats.t.ppf(1 - alpha / 2, df)
        return c, -c


def show_result(test_stat, p_value, df=None, criticals=None):
    st.markdown("### 4. Test Statistic")

    st.metric("Calculated test statistic", f"{test_stat:.5f}")
    st.metric("p-value", f"{p_value:.6f}")

    if df is not None:
        st.write(f"Degrees of freedom = **{df}**")

    st.markdown("### 5. Critical Value Method")

    if criticals is not None:
        upper, lower = criticals

        if upper is not None:
            st.write(f"Upper critical value = **{upper:.5f}**")

        if lower is not None:
            st.write(f"Lower critical value = **{lower:.5f}**")

        if tail == "Right-tailed":
            st.write(
                "Reject H₀ if the calculated statistic exceeds "
                "the upper critical value."
            )
        elif tail == "Left-tailed":
            st.write(
                "Reject H₀ if the calculated statistic is below "
                "the lower critical value."
            )
        else:
            st.write(
                "Reject H₀ if the statistic is below the lower "
                "critical value or above the upper critical value."
            )

    st.markdown("### 6. Decision")
    st.success(decision_from_p(p_value))
    st.write(interpretation(p_value))


# --------------------------------------------------
# ONE-SAMPLE Z-TEST
# --------------------------------------------------

if test_type == "One-Sample Z-Test":

    st.markdown("## One-Sample Z-Test")

    st.markdown("""
    **Business example:** A company claims that the average weight
    of its product is 500 grams. A sample is collected to test the claim.

    A one-sample Z-test is appropriate when the population standard
    deviation is known and the observations satisfy the relevant
    distributional assumptions.
    """)

    col1, col2 = st.columns(2)

    with col1:
        sample_text = st.text_area(
            "Sample observations",
            "510, 505, 498, 502, 507, 495, 501, 506, 499, 503"
        )

    with col2:
        mu0 = st.number_input(
            "Hypothesized population mean",
            value=500.0
        )

        sigma = st.number_input(
            "Known population standard deviation",
            min_value=0.0001,
            value=5.0
        )

    x = parse_values(sample_text)

    if x is None:
        st.error("Enter valid comma-separated numeric observations.")

    else:
        n = len(x)
        xbar = np.mean(x)
        se = sigma / np.sqrt(n)
        z = (xbar - mu0) / se

        if tail == "Right-tailed":
            p = stats.norm.sf(z)
        elif tail == "Left-tailed":
            p = stats.norm.cdf(z)
        else:
            p = 2 * stats.norm.sf(abs(z))

        st.markdown("### 1. Sample Information")

        df = pd.DataFrame({
            "Measure": [
                "Sample size",
                "Sample mean",
                "Population standard deviation",
                "Standard error"
            ],
            "Value": [
                n,
                round(xbar, 5),
                sigma,
                round(se, 5)
            ]
        })

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("### 2. Hypotheses")
        show_hypotheses("μ", mu0)

        st.markdown("### 3. Formula and Calculation")

        st.latex(
            r"Z=\frac{\bar X-\mu_0}{\sigma/\sqrt n}"
        )

        st.latex(
            rf"Z=\frac{{{xbar:.4f}-{mu0:.4f}}}"
            rf"{{{sigma:.4f}/\sqrt{{{n}}}}}"
            rf"={z:.5f}"
        )

        criticals = z_critical_values(alpha, tail)
        show_result(z, p, criticals=criticals)


# --------------------------------------------------
# TWO-SAMPLE Z-TEST
# --------------------------------------------------

elif test_type == "Two-Sample Z-Test":

    st.markdown("## Two-Sample Z-Test")

    st.markdown("""
    **Business example:** Compare the average sales of two branches.

    This version assumes independent samples and known population
    standard deviations for both populations.
    """)

    col1, col2 = st.columns(2)

    with col1:
        a_text = st.text_area(
            "Branch A observations",
            "100, 105, 98, 110, 102, 107"
        )

        mu_a = st.number_input(
            "Hypothesized mean for Branch A",
            value=100.0
        )

        sigma_a = st.number_input(
            "Known population SD for A",
            min_value=0.0001,
            value=8.0
        )

    with col2:
        b_text = st.text_area(
            "Branch B observations",
            "95, 100, 97, 103, 99, 101"
        )

        mu_b = st.number_input(
            "Hypothesized mean for Branch B",
            value=100.0
        )

        sigma_b = st.number_input(
            "Known population SD for B",
            min_value=0.0001,
            value=7.0
        )

    a = parse_values(a_text)
    b = parse_values(b_text)

    if a is None or b is None:
        st.error("Enter valid numeric observations for both samples.")

    else:
        n1, n2 = len(a), len(b)
        x1, x2 = np.mean(a), np.mean(b)

        difference0 = mu_a - mu_b

        se = np.sqrt(
            sigma_a**2 / n1 + sigma_b**2 / n2
        )

        z = ((x1 - x2) - difference0) / se

        if tail == "Right-tailed":
            p = stats.norm.sf(z)
        elif tail == "Left-tailed":
            p = stats.norm.cdf(z)
        else:
            p = 2 * stats.norm.sf(abs(z))

        st.markdown("### 1. Sample Information")

        st.dataframe(
            pd.DataFrame({
                "Measure": ["Sample size", "Sample mean", "Known population SD"],
                "Sample A": [n1, round(x1, 5), sigma_a],
                "Sample B": [n2, round(x2, 5), sigma_b]
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 2. Hypotheses")

        show_hypotheses(
            r"\mu_1-\mu_2",
            f"{difference0:.4f}"
        )

        st.markdown("### 3. Formula and Calculation")

        st.latex(
            r"Z=\frac{(\bar X_1-\bar X_2)-"
            r"(\mu_1-\mu_2)_0}"
            r"{\sqrt{\sigma_1^2/n_1+\sigma_2^2/n_2}}"
        )

        st.write(f"Observed mean difference = {x1 - x2:.5f}")
        st.write(f"Hypothesized difference = {difference0:.5f}")
        st.write(f"Standard error = {se:.5f}")
        st.write(f"Z = {z:.5f}")

        criticals = z_critical_values(alpha, tail)
        show_result(z, p, criticals=criticals)


# --------------------------------------------------
# ONE-SAMPLE T-TEST
# --------------------------------------------------

elif test_type == "One-Sample t-Test":

    st.markdown("## One-Sample t-Test")

    st.markdown("""
    **Business example:** Test whether the average time taken to
    process an invoice differs from the target of 20 minutes.

    Use a one-sample t-test when the population standard deviation
    is unknown. The usual assumptions include independent observations
    and an approximately normal population, particularly for small samples.
    """)

    sample_text = st.text_area(
        "Sample observations",
        "18, 21, 19, 22, 20, 17, 23, 19, 21, 20"
    )

    mu0 = st.number_input(
        "Hypothesized population mean",
        value=20.0
    )

    x = parse_values(sample_text)

    if x is None:
        st.error("Enter valid numeric observations.")

    elif len(x) < 2:
        st.error("At least two observations are required.")

    else:
        n = len(x)
        xbar = np.mean(x)
        s = np.std(x, ddof=1)
        se = s / np.sqrt(n)
        df = n - 1
        t_stat = (xbar - mu0) / se

        if tail == "Right-tailed":
            p = stats.t.sf(t_stat, df)
        elif tail == "Left-tailed":
            p = stats.t.cdf(t_stat, df)
        else:
            p = 2 * stats.t.sf(abs(t_stat), df)

        st.markdown("### 1. Sample Information")

        st.dataframe(
            pd.DataFrame({
                "Measure": [
                    "Sample size",
                    "Sample mean",
                    "Sample standard deviation",
                    "Standard error",
                    "Degrees of freedom"
                ],
                "Value": [
                    n,
                    round(xbar, 5),
                    round(s, 5),
                    round(se, 5),
                    df
                ]
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 2. Hypotheses")
        show_hypotheses("μ", mu0)

        st.markdown("### 3. Formula and Calculation")

        st.latex(
            r"t=\frac{\bar X-\mu_0}{s/\sqrt n}"
        )

        st.latex(
            rf"t=\frac{{{xbar:.4f}-{mu0:.4f}}}"
            rf"{{{s:.4f}/\sqrt{{{n}}}}}"
            rf"={t_stat:.5f}"
        )

        criticals = t_critical_values(alpha, df, tail)
        show_result(t_stat, p, df=df, criticals=criticals)


# --------------------------------------------------
# INDEPENDENT TWO-SAMPLE T-TEST
# --------------------------------------------------

elif test_type == "Independent Two-Sample t-Test":

    st.markdown("## Independent Two-Sample t-Test")

    st.markdown("""
    **Business example:** Compare average productivity before
    introducing a new training programme in two independent groups.

    This version uses Welch's t-test, which does not assume equal
    population variances.
    """)

    col1, col2 = st.columns(2)

    with col1:
        a_text = st.text_area(
            "Group A observations",
            "72, 75, 78, 70, 74, 77, 73"
        )

    with col2:
        b_text = st.text_area(
            "Group B observations",
            "80, 82, 78, 85, 81, 79, 84"
        )

    a = parse_values(a_text)
    b = parse_values(b_text)

    if a is None or b is None:
        st.error("Enter valid numeric observations for both groups.")

    elif len(a) < 2 or len(b) < 2:
        st.error("Each group must contain at least two observations.")

    else:
        n1, n2 = len(a), len(b)
        x1, x2 = np.mean(a), np.mean(b)
        s1, s2 = np.std(a, ddof=1), np.std(b, ddof=1)

        v1, v2 = s1**2, s2**2

        se = np.sqrt(v1 / n1 + v2 / n2)

        t_stat = (x1 - x2) / se

        # Welch-Satterthwaite degrees of freedom
        numerator = (v1 / n1 + v2 / n2)**2

        denominator = (
            (v1 / n1)**2 / (n1 - 1)
            + (v2 / n2)**2 / (n2 - 1)
        )

        df = numerator / denominator

        if tail == "Right-tailed":
            p = stats.t.sf(t_stat, df)
        elif tail == "Left-tailed":
            p = stats.t.cdf(t_stat, df)
        else:
            p = 2 * stats.t.sf(abs(t_stat), df)

        st.markdown("### 1. Sample Information")

        st.dataframe(
            pd.DataFrame({
                "Measure": ["Sample size", "Mean", "Sample SD", "Sample variance"],
                "Group A": [n1, round(x1, 5), round(s1, 5), round(v1, 5)],
                "Group B": [n2, round(x2, 5), round(s2, 5), round(v2, 5)]
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 2. Hypotheses")
        show_hypotheses(r"\mu_1-\mu_2", 0)

        st.markdown("### 3. Formula and Calculation")

        st.latex(
            r"t=\frac{\bar X_1-\bar X_2}"
            r"{\sqrt{s_1^2/n_1+s_2^2/n_2}}"
        )

        st.write(f"Difference between sample means = {x1 - x2:.5f}")
        st.write(f"Standard error = {se:.5f}")
        st.write(f"Welch's degrees of freedom = {df:.5f}")
        st.write(f"Calculated t = {t_stat:.5f}")

        criticals = t_critical_values(alpha, df, tail)
        show_result(t_stat, p, df=df, criticals=criticals)


# --------------------------------------------------
# PAIRED T-TEST
# --------------------------------------------------

elif test_type == "Paired t-Test":

    st.markdown("## Paired t-Test")

    st.markdown("""
    **Business example:** Compare employee performance scores before
    and after training, measured for the same employees.

    Enter the observations in matching order. Each value in the first
    column must correspond to the same person or unit in the second.
    """)

    col1, col2 = st.columns(2)

    with col1:
        before_text = st.text_area(
            "Before training",
            "60, 65, 62, 58, 70, 67, 64, 61"
        )

    with col2:
        after_text = st.text_area(
            "After training",
            "68, 70, 65, 64, 75, 72, 69, 66"
        )

    before = parse_values(before_text)
    after = parse_values(after_text)

    if before is None or after is None:
        st.error("Enter valid numeric observations for both columns.")

    elif len(before) != len(after):
        st.error("Before and after samples must have equal lengths.")

    elif len(before) < 2:
        st.error("At least two matched pairs are required.")

    else:
        differences = after - before

        n = len(differences)
        mean_d = np.mean(differences)
        sd_d = np.std(differences, ddof=1)
        se = sd_d / np.sqrt(n)
        df = n - 1

        if se == 0:
            st.error(
                "All paired differences are identical. "
                "The t statistic cannot be calculated using the "
                "usual formula because the standard error is zero."
            )
            st.stop()

        t_stat = mean_d / se

        if tail == "Right-tailed":
            p = stats.t.sf(t_stat, df)
        elif tail == "Left-tailed":
            p = stats.t.cdf(t_stat, df)
        else:
            p = 2 * stats.t.sf(abs(t_stat), df)

        st.markdown("### 1. Paired Observations")

        st.dataframe(
            pd.DataFrame({
                "Before": before,
                "After": after,
                "Difference (After − Before)": differences
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 2. Summary of Differences")

        st.dataframe(
            pd.DataFrame({
                "Measure": [
                    "Number of pairs",
                    "Mean difference",
                    "SD of differences",
                    "Standard error",
                    "Degrees of freedom"
                ],
                "Value": [
                    n,
                    round(mean_d, 5),
                    round(sd_d, 5),
                    round(se, 5),
                    df
                ]
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### 3. Hypotheses")

        st.markdown(
            "The hypotheses concern the **population mean paired "
            "difference**, μd."
        )

        show_hypotheses(r"\mu_d", 0)

        st.markdown("### 4. Formula and Calculation")

        st.latex(
            r"t=\frac{\bar d}{s_d/\sqrt n}"
        )

        st.latex(
            rf"t=\frac{{{mean_d:.4f}}}"
            rf"{{{sd_d:.4f}/\sqrt{{{n}}}}}"
            rf"={t_stat:.5f}"
        )

        criticals = t_critical_values(alpha, df, tail)
        show_result(t_stat, p, df=df, criticals=criticals)


# --------------------------------------------------
# LEARNING NOTES
# --------------------------------------------------

st.divider()

st.markdown("## Quick Learning Notes")

with st.expander("1. When should I use a Z-test?"):
    st.write("""
    A one-sample Z-test is commonly used when the population standard
    deviation is known and the sampling assumptions are appropriate.

    A two-sample Z-test can compare independent population means when
    both population standard deviations are known.
    """)

with st.expander("2. When should I use a t-test?"):
    st.write("""
    Use a one-sample t-test to compare a sample mean with a target
    when the population standard deviation is unknown.

    Use an independent two-sample t-test to compare two independent
    group means. This application uses Welch's version, which does
    not require equal population variances.

    Use a paired t-test for matched observations, such as measurements
    taken before and after training on the same employees.
    """)

with st.expander("3. What is a p-value?"):
    st.write("""
    The p-value is the probability, assuming the null hypothesis is true,
    of obtaining a test statistic at least as extreme as the one observed,
    in the direction specified by the alternative hypothesis.

    If p-value < significance level, reject the null hypothesis.
    Otherwise, fail to reject the null hypothesis.
    """)

with st.expander("4. What is the difference between one-tailed and two-tailed tests?"):
    st.write("""
    Right-tailed: tests whether a parameter is greater than the
    hypothesized value.

    Left-tailed: tests whether a parameter is less than the
    hypothesized value.

    Two-tailed: tests whether a parameter differs from the
    hypothesized value in either direction.
    """)

st.caption(
    "Educational tool: verify assumptions and study design before "
    "applying any test to real data."
)
```
