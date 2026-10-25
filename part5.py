```python
import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.set_page_config(
    page_title="Business Statistics Lab - Part 5",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Statistics Learning Lab")
st.subheader(
    "Part 5: Chi-Square, F-Test, ANOVA and Probability Distributions"
)

st.markdown("""
Learn statistical tests and probability distributions using
editable sample data, formulas and step-by-step calculations.
""")

# ==========================================================
# SIDEBAR
# ==========================================================

topic = st.sidebar.selectbox(
    "Select a topic",
    [
        "Chi-Square Goodness of Fit",
        "Chi-Square Test of Independence",
        "F-Test: Two Variances",
        "One-Way ANOVA",
        "Binomial Distribution",
        "Poisson Distribution",
        "Normal Distribution"
    ]
)

# ==========================================================
# COMMON FUNCTIONS
# ==========================================================

def parse_values(text):
    try:
        values = np.array(
            [
                float(item.strip())
                for item in text.split(",")
                if item.strip()
            ],
            dtype=float
        )

        if len(values) == 0 or not np.all(np.isfinite(values)):
            return None

        return values

    except ValueError:
        return None


def show_test_decision(statistic, p_value, alpha, df=None):
    st.markdown("### Test Results")

    c1, c2 = st.columns(2)

    c1.metric("Test statistic", f"{statistic:.5f}")
    c2.metric("p-value", f"{p_value:.6f}")

    if df is not None:
        st.write(f"Degrees of freedom: **{df}**")

    if p_value < alpha:
        st.error("Decision: Reject the null hypothesis.")
        st.write(
            f"Since p-value ({p_value:.6f}) is less than "
            f"the significance level ({alpha:.3f}), "
            "the result is statistically significant."
        )
    else:
        st.success("Decision: Fail to reject the null hypothesis.")
        st.write(
            f"Since p-value ({p_value:.6f}) is greater than or equal "
            f"to the significance level ({alpha:.3f}), "
            "the result is not statistically significant."
        )


def parse_matrix(text):
    """
    Enter one row per line and separate values using commas.
    """
    try:
        rows = []

        for line in text.strip().splitlines():
            if line.strip():
                rows.append(
                    [
                        float(item.strip())
                        for item in line.split(",")
                    ]
                )

        if not rows:
            return None

        lengths = [len(row) for row in rows]

        if len(set(lengths)) != 1:
            return None

        matrix = np.array(rows, dtype=float)

        if not np.all(np.isfinite(matrix)):
            return None

        if np.any(matrix < 0):
            return None

        return matrix

    except ValueError:
        return None


# ==========================================================
# 1. CHI-SQUARE GOODNESS OF FIT
# ==========================================================

if topic == "Chi-Square Goodness of Fit":

    st.header("1. Chi-Square Goodness-of-Fit Test")

    st.markdown("""
    **Business example:** A company expects its products to be sold
    equally across four regions. The observed sales are compared with
    the expected sales.
    """)

    observed_text = st.text_input(
        "Observed frequencies, separated by commas",
        "40, 30, 20, 10"
    )

    expected_text = st.text_input(
        "Expected frequencies, separated by commas",
        "25, 25, 25, 25"
    )

    alpha = st.number_input(
        "Significance level",
        min_value=0.001,
        max_value=0.25,
        value=0.05,
        step=0.01
    )

    observed = parse_values(observed_text)
    expected = parse_values(expected_text)

    if observed is None or expected is None:
        st.error("Enter valid numerical frequencies.")

    elif len(observed) != len(expected):
        st.error("Observed and expected frequencies must have equal lengths.")

    elif len(observed) < 2:
        st.error("Enter at least two categories.")

    elif np.any(observed < 0) or np.any(expected <= 0):
        st.error("Observed frequencies must be non-negative and expected frequencies positive.")

    elif not np.allclose(observed, np.round(observed)):
        st.error("Observed frequencies must be whole numbers.")

    elif not np.allclose(expected, np.round(expected)):
        st.error("Expected frequencies must be whole numbers.")

    elif not np.isclose(np.sum(observed), np.sum(expected)):
        st.error(
            "Observed and expected frequencies must have equal totals. "
            "For a goodness-of-fit test, expected counts should reflect "
            "the same total sample size."
        )

    elif np.any(expected < 5):
        st.warning(
            "Some expected frequencies are below 5. "
            "The usual chi-square approximation may be unreliable; "
            "consider combining appropriate categories or using an "
            "alternative method."
        )

    else:
        chi_components = (observed - expected) ** 2 / expected
        chi_square = np.sum(chi_components)

        k = len(observed)
        df = k - 1

        p_value = stats.chi2.sf(chi_square, df)
        critical = stats.chi2.ppf(1 - alpha, df)

        table = pd.DataFrame({
            "Category": [f"Category {i+1}" for i in range(k)],
            "Observed (O)": observed.astype(int),
            "Expected (E)": expected.astype(int),
            "O - E": observed - expected,
            "(O - E)²": (observed - expected) ** 2,
            "(O - E)² / E": chi_components
        })

        st.subheader("Step 1: Calculation Table")
        st.dataframe(table, use_container_width=True, hide_index=True)

        st.write(f"Total observed frequency = {observed.sum():.0f}")
        st.write(f"Total expected frequency = {expected.sum():.0f}")

        st.subheader("Step 2: Formula")
        st.latex(
            r"\chi^2=\sum\frac{(O-E)^2}{E}"
        )

        st.latex(
            rf"\chi^2={chi_square:.5f}"
        )

        st.subheader("Step 3: Hypotheses")
        st.write("H₀: The observed distribution follows the expected distribution.")
        st.write("H₁: The observed distribution differs from the expected distribution.")

        st.write(f"Degrees of freedom = k − 1 = {k} − 1 = {df}")
        st.write(f"Critical chi-square value = {critical:.5f}")

        show_test_decision(chi_square, p_value, alpha, df)

# ==========================================================
# 2. CHI-SQUARE TEST OF INDEPENDENCE
# ==========================================================

elif topic == "Chi-Square Test of Independence":

    st.header("2. Chi-Square Test of Independence")

    st.markdown("""
    **Business example:** Determine whether customer preference
    for a product is associated with customer age group.

    Enter the observed contingency table. Use commas between columns
    and new lines between rows. Do not enter row or column totals.
    """)

    matrix_text = st.text_area(
        "Observed frequency table",
        "30, 20, 10\n20, 25, 35"
    )

    alpha = st.number_input(
        "Significance level",
        min_value=0.001,
        max_value=0.25,
        value=0.05,
        step=0.01
    )

    observed = parse_matrix(matrix_text)

    if observed is None:
        st.error(
            "Enter a rectangular table of non-negative numbers. "
            "Separate columns with commas and rows with new lines."
        )

    elif observed.shape[0] < 2 or observed.shape[1] < 2:
        st.error("The table must have at least two rows and two columns.")

    elif not np.allclose(observed, np.round(observed)):
        st.error("Observed frequencies must be whole numbers.")

    elif np.any(observed.sum(axis=0) == 0) or np.any(observed.sum(axis=1) == 0):
        st.error("Every row and column must have a positive total.")

    else:
        row_totals = observed.sum(axis=1)
        col_totals = observed.sum(axis=0)
        grand_total = observed.sum()

        expected = np.outer(row_totals, col_totals) / grand_total

        components = (observed - expected) ** 2 / expected
        chi_square = components.sum()

        rows, cols = observed.shape
        df = (rows - 1) * (cols - 1)

        p_value = stats.chi2.sf(chi_square, df)
        critical = stats.chi2.ppf(1 - alpha, df)

        st.subheader("Step 1: Observed Frequencies")

        st.dataframe(
            pd.DataFrame(
                observed.astype(int),
                index=[f"Row {i+1}" for i in range(rows)],
                columns=[f"Column {j+1}" for j in range(cols)]
            ),
            use_container_width=True
        )

        st.subheader("Step 2: Expected Frequencies")

        st.dataframe(
            pd.DataFrame(
                expected,
                index=[f"Row {i+1}" for i in range(rows)],
                columns=[f"Column {j+1}" for j in range(cols)]
            ).round(4),
            use_container_width=True
        )

        st.subheader("Step 3: Chi-Square Components")

        st.dataframe(
            pd.DataFrame(
                components,
                index=[f"Row {i+1}" for i in range(rows)],
                columns=[f"Column {j+1}" for j in range(cols)]
            ).round(4),
            use_container_width=True
        )

        st.latex(
            r"E_{ij}=\frac{(\text{Row Total})(\text{Column Total})}"
            r"{\text{Grand Total}}"
        )

        st.latex(
            r"\chi^2=\sum\frac{(O-E)^2}{E}"
        )

        st.write(f"Grand total = {grand_total:.0f}")
        st.write(f"Degrees of freedom = (r − 1)(c − 1) = {df}")
        st.write(f"Critical chi-square value = {critical:.5f}")

        if np.any(expected < 5):
            st.warning(
                "At least one expected cell frequency is below 5. "
                "The chi-square approximation may be unreliable. "
                "Consider combining substantively appropriate categories "
                "or using an exact test when suitable."
            )

        st.write("H₀: The two categorical variables are independent.")
        st.write("H₁: The two categorical variables are associated.")

        show_test_decision(chi_square, p_value, alpha, df)

# ==========================================================
# 3. F-TEST FOR TWO VARIANCES
# ==========================================================

elif topic == "F-Test: Two Variances":

    st.header("3. F-Test for Two Population Variances")

    st.markdown("""
    **Business example:** Compare the variability of output
    from two production machines.

    This classical F-test assumes independent random samples
    from normally distributed populations.
    """)

    col1, col2 = st.columns(2)

    with col1:
        sample_a_text = st.text_area(
            "Machine A observations",
            "48, 50, 52, 49, 51, 50, 47, 53"
        )

    with col2:
        sample_b_text = st.text_area(
            "Machine B observations",
            "45, 52, 48, 55, 50, 47, 54, 49"
        )

    alpha = st.number_input(
        "Significance level",
        min_value=0.001,
        max_value=0.25,
        value=0.05,
        step=0.01
    )

    tail = st.selectbox(
        "Alternative hypothesis",
        ["Two-tailed", "Right-tailed", "Left-tailed"]
    )

    a = parse_values(sample_a_text)
    b = parse_values(sample_b_text)

    if a is None or b is None:
        st.error("Enter valid numerical observations.")

    elif len(a) < 2 or len(b) < 2:
        st.error("Each sample must have at least two observations.")

    else:
        n1, n2 = len(a), len(b)
        var1 = np.var(a, ddof=1)
        var2 = np.var(b, ddof=1)

        if var1 == 0 or var2 == 0:
            st.error(
                "Both sample variances must be positive for this F-test."
            )
            st.stop()

        f_stat = var1 / var2
        df1 = n1 - 1
        df2 = n2 - 1

        if tail == "Right-tailed":
            p_value = stats.f.sf(f_stat, df1, df2)
            critical = stats.f.ppf(1 - alpha, df1, df2)
            st.write("H₀: σ₁² = σ₂²")
            st.write("H₁: σ₁² > σ₂²")

            st.write(f"Upper critical F-value = {critical:.5f}")

        elif tail == "Left-tailed":
            p_value = stats.f.cdf(f_stat, df1, df2)
            critical = stats.f.ppf(alpha, df1, df2)
            st.write("H₀: σ₁² = σ₂²")
            st.write("H₁: σ₁² < σ₂²")

            st.write(f"Lower critical F-value = {critical:.5f}")

        else:
            lower = stats.f.ppf(alpha / 2, df1, df2)
            upper = stats.f.ppf(1 - alpha / 2, df1, df2)

            p_value = min(
                1.0,
                2 * min(
                    stats.f.cdf(f_stat, df1, df2),
                    stats.f.sf(f_stat, df1, df2)
                )
            )

            st.write("H₀: σ₁² = σ₂²")
            st.write("H₁: σ₁² ≠ σ₂²")

            st.write(f"Lower critical F-value = {lower:.5f}")
            st.write(f"Upper critical F-value = {upper:.5f}")

        st.subheader("Step 1: Sample Statistics")

        st.dataframe(
            pd.DataFrame({
                "Measure": ["Sample size", "Sample variance", "Degrees of freedom"],
                "Machine A": [n1, var1, df1],
                "Machine B": [n2, var2, df2]
            }),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Step 2: Formula")

        st.latex(
            r"F=\frac{s_1^2}{s_2^2}"
        )

        st.latex(
            rf"F=\frac{{{var1:.5f}}}{{{var2:.5f}}}"
            rf"={f_stat:.5f}"
        )

        st.write(f"Numerator degrees of freedom = {df1}")
        st.write(f"Denominator degrees of freedom = {df2}")

        show_test_decision(
            f_stat,
            p_value,
            alpha,
            f"({df1}, {df2})"
        )

# ==========================================================
# 4. ONE-WAY ANOVA
# ==========================================================

elif topic == "One-Way ANOVA":

    st.header("4. One-Way Analysis of Variance (ANOVA)")

    st.markdown("""
    **Business example:** Compare the average sales generated by
    three different advertising campaigns.

    Enter one group's observations per line, separated by commas.
    This implementation uses the classical one-way ANOVA, which
    assumes independent observations, approximately normal errors
    within groups and equal population variances.
    """)

    groups_text = st.text_area(
        "Enter each group's observations on a separate line",
        "20, 22, 19, 23, 21\n"
        "25, 27, 24, 26, 28\n"
        "18, 17, 20, 19, 16"
    )

    alpha = st.number_input(
        "Significance level",
        min_value=0.001,
        max_value=0.25,
        value=0.05,
        step=0.01
    )

    try:
        groups = [
            parse_values(line)
            for line in groups_text.strip().splitlines()
            if line.strip()
        ]

        valid = (
            len(groups) >= 2
            and all(g is not None and len(g) >= 2 for g in groups)
        )

    except Exception:
        valid = False
        groups = []

    if not valid:
        st.error(
            "Enter at least two groups with at least two numeric "
            "observations in each group."
        )

    else:
        k = len(groups)
        ns = np.array([len(g) for g in groups])
        means = np.array([np.mean(g) for g in groups])
        variances = np.array([np.var(g, ddof=1) for g in groups])

        all_data = np.concatenate(groups)
        grand_mean = np.mean(all_data)
        N = len(all_data)

        ss_between = np.sum(
            ns * (means - grand_mean) ** 2
        )

        ss_within = sum(
            np.sum((g - np.mean(g)) ** 2)
            for g in groups
        )

        ss_total = np.sum(
            (all_data - grand_mean) ** 2
        )

        df_between = k - 1
        df_within = N - k
        df_total = N - 1

        ms_between = ss_between / df_between
        ms_within = ss_within / df_within

        if ms_within == 0:
            st.error(
                "Within-group variation is zero. "
                "The usual F statistic cannot be calculated."
            )
            st.stop()

        f_stat = ms_between / ms_within
        p_value = stats.f.sf(f_stat, df_between, df_within)
        critical = stats.f.ppf(1 - alpha, df_between, df_within)

        st.subheader("Step 1: Group Summary")

        st.dataframe(
            pd.DataFrame({
                "Group": [f"Group {i+1}" for i in range(k)],
                "Sample size": ns,
                "Mean": means,
                "Sample variance": variances
            }).round(4),
            use_container_width=True,
            hide_index=True
        )

        st.write(f"Grand mean = {grand_mean:.5f}")
        st.write(f"Total number of observations = {N}")

        st.subheader("Step 2: Sum of Squares")

        st.latex(
            r"SS_B=\sum n_i(\bar X_i-\bar X)^2"
        )

        st.latex(
            r"SS_W=\sum\sum(X_{ij}-\bar X_i)^2"
        )

        st.latex(
            r"SS_T=SS_B+SS_W"
        )

        st.dataframe(
            pd.DataFrame({
                "Source": ["Between groups", "Within groups", "Total"],
                "Sum of squares": [ss_between, ss_within, ss_total],
                "Degrees of freedom": [df_between, df_within, df_total],
                "Mean square": [ms_between, ms_within, np.nan]
            }).round(5),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Step 3: ANOVA Table")

        st.latex(
            r"F=\frac{MS_B}{MS_W}"
        )

        st.latex(
            rf"F=\frac{{{ms_between:.5f}}}"
            rf"{{{ms_within:.5f}}}={f_stat:.5f}"
        )

        st.write("H₀: All population means are equal.")
        st.write("H₁: At least one population mean differs.")

        st.write(f"Critical F-value = {critical:.5f}")

        show_test_decision(
            f_stat,
            p_value,
            alpha,
            f"({df_between}, {df_within})"
        )

        st.info(
            "A significant ANOVA result shows that not all means are equal. "
            "It does not identify which particular groups differ. "
            "A suitable post-hoc procedure, such as Tukey's HSD, "
            "is needed for pairwise comparisons."
        )

# ==========================================================
# 5. BINOMIAL DISTRIBUTION
# ==========================================================

elif topic == "Binomial Distribution":

    st.header("5. Binomial Probability Distribution")

    st.markdown("""
    **Business example:** A salesperson has a known probability of
    making a sale on each independent customer contact.

    The binomial model assumes a fixed number of trials, independent
    trials, two possible outcomes per trial and a constant success
    probability.
    """)

    n = st.number_input(
        "Number of trials (n)",
        min_value=1,
        max_value=100000,
        value=10
    )

    p = st.number_input(
        "Probability of success (p)",
        min_value=0.0,
        max_value=1.0,
        value=0.30,
        step=0.05
    )

    x = st.number_input(
        "Number of successes (x)",
        min_value=0,
        max_value=int(n),
        value=min(3, int(n))
    )

    event = st.selectbox(
        "Choose the probability",
        [
            "Exactly x successes",
            "At most x successes",
            "Fewer than x successes",
            "At least x successes",
            "More than x successes"
        ]
    )

    probability = stats.binom.pmf(int(x), int(n), p)

    if event == "Exactly x successes":
        result = probability
        description = f"P(X = {int(x)})"

    elif event == "At most x successes":
        result = stats.binom.cdf(int(x), int(n), p)
        description = f"P(X ≤ {int(x)})"

    elif event == "Fewer than x successes":
        result = stats.binom.cdf(int(x) - 1, int(n), p)
        description = f"P(X < {int(x)})"

    elif event == "At least x successes":
        result = stats.binom.sf(int(x) - 1, int(n), p)
        description = f"P(X ≥ {int(x)})"

    else:
        result = stats.binom.sf(int(x), int(n), p)
        description = f"P(X > {int(x)})"

    mean = n * p
    variance = n * p * (1 - p)
    sd = np.sqrt(variance)

    st.subheader("Formula")

    st.latex(
        r"P(X=x)=\binom{n}{x}p^x(1-p)^{n-x}"
    )

    st.latex(
        rf"\binom{{{int(n)}}}{{{int(x)}}}"
        rf"=\frac{{{int(n)}!}}"
        rf"{{{int(x)}!({int(n)}-{int(x)})!}}"
    )

    st.subheader("Results")

    c1, c2, c3 = st.columns(3)

    c1.metric("Mean", f"{mean:.5f}")
    c2.metric("Variance", f"{variance:.5f}")
    c3.metric("Standard deviation", f"{sd:.5f}")

    st.metric(description, f"{result:.8f}")

    st.write(f"Probability as a percentage = {result * 100:.5f}%")

    chart_data = pd.DataFrame({
        "Number of successes": np.arange(int(n) + 1),
        "Probability": stats.binom.pmf(
            np.arange(int(n) + 1), int(n), p
        )
    })

    st.subheader("Probability Distribution")
    st.bar_chart(
        chart_data.set_index("Number of successes")
    )

# ==========================================================
# 6. POISSON DISTRIBUTION
# ==========================================================

elif topic == "Poisson Distribution":

    st.header("6. Poisson Probability Distribution")

    st.markdown("""
    **Business example:** Estimate the probability of receiving
    a certain number of customer complaints per day.

    The Poisson distribution models counts in a fixed interval
    when events occur independently at a stable average rate.
    """)

    lam = st.number_input(
        "Average number of events (λ)",
        min_value=0.0001,
        max_value=10000.0,
        value=4.0,
        step=0.5
    )

    x = st.number_input(
        "Number of events (x)",
        min_value=0,
        max_value=100000,
        value=2
    )

    event = st.selectbox(
        "Choose the probability",
        [
            "Exactly x events",
            "At most x events",
            "Fewer than x events",
            "At least x events",
            "More than x events"
        ]
    )

    if event == "Exactly x events":
        result = stats.poisson.pmf(int(x), lam)
        description = f"P(X = {int(x)})"

    elif event == "At most x events":
        result = stats.poisson.cdf(int(x), lam)
        description = f"P(X ≤ {int(x)})"

    elif event == "Fewer than x events":
        result = stats.poisson.cdf(int(x) - 1, lam)
        description = f"P(X < {int(x)})"

    elif event == "At least x events":
        result = stats.poisson.sf(int(x) - 1, lam)
        description = f"P(X ≥ {int(x)})"

    else:
        result = stats.poisson.sf(int(x), lam)
        description = f"P(X > {int(x)})"

    st.subheader("Formula")

    st.latex(
        r"P(X=x)=\frac{e^{-\lambda}\lambda^x}{x!}"
    )

    st.latex(
        rf"P(X={int(x)})="
        rf"\frac{{e^{{-{lam}}}{lam}^{{{int(x)}}}}}"
        rf"{{{int(x)}!}}"
        rf"={stats.poisson.pmf(int(x), lam):.8f}"
    )

    st.subheader("Results")

    c1, c2 = st.columns(2)

    c1.metric("Mean", f"{lam:.5f}")
    c2.metric("Variance", f"{lam:.5f}")

    st.metric(description, f"{result:.8f}")

    st.write(f"Probability as a percentage = {result * 100:.5f}%")

    max_k = min(
        100,
        max(15, int(lam + 5 * np.sqrt(lam) + 5))
    )

    chart_data = pd.DataFrame({
        "Number of events": np.arange(max_k + 1),
        "Probability": stats.poisson.pmf(
            np.arange(max_k + 1), lam
        )
    })

    st.subheader("Probability Distribution")
    st.bar_chart(
        chart_data.set_index("Number of events")
    )

# ==========================================================
# 7. NORMAL DISTRIBUTION
# ==========================================================

elif topic == "Normal Distribution":

    st.header("7. Normal Probability Distribution")

    st.markdown("""
    **Business example:** Analyse product weights, examination marks
    or delivery times using a normal distribution when the normal
    model is appropriate.
    """)

    col1, col2 = st.columns(2)

    with col1:
        mu = st.number_input(
            "Population mean (μ)",
            value=100.0
        )

    with col2:
        sigma = st.number_input(
            "Population standard deviation (σ)",
            min_value=0.0001,
            value=15.0
        )

    event = st.selectbox(
        "Select the event",
        [
            "Probability below a value",
            "Probability above a value",
            "Probability between two values"
        ]
    )

    if event in [
        "Probability below a value",
        "Probability above a value"
    ]:
        x = st.number_input(
            "Value (x)",
            value=110.0
        )

        z = (x - mu) / sigma

        if event == "Probability below a value":
            result = stats.norm.cdf(x, loc=mu, scale=sigma)
            expression = f"P(X ≤ {x:.4f})"

        else:
            result = stats.norm.sf(x, loc=mu, scale=sigma)
            expression = f"P(X > {x:.4f})"

        st.subheader("Step 1: Standardise the value")

        st.latex(
            r"Z=\frac{X-\mu}{\sigma}"
        )

        st.latex(
            rf"Z=\frac{{{x:.4f}-{mu:.4f}}}"
            rf"{{{sigma:.4f}}}={z:.5f}"
        )

        st.subheader("Step 2: Probability")

        st.metric(expression, f"{result:.8f}")
        st.write(f"Percentage = {result * 100:.5f}%")

    else:
        col1, col2 = st.columns(2)

        with col1:
            lower = st.number_input(
                "Lower value",
                value=85.0
            )

        with col2:
            upper = st.number_input(
                "Upper value",
                value=115.0
            )

        if lower >= upper:
            st.error("The upper value must exceed the lower value.")

        else:
            z_lower = (lower - mu) / sigma
            z_upper = (upper - mu) / sigma

            result = (
                stats.norm.cdf(upper, loc=mu, scale=sigma)
                - stats.norm.cdf(lower, loc=mu, scale=sigma)
            )

            st.subheader("Step 1: Calculate Z-scores")

            st.latex(
                r"Z_1=\frac{X_1-\mu}{\sigma}"
            )

            st.latex(
                r"Z_2=\frac{X_2-\mu}{\sigma}"
            )

            st.write(f"Lower Z-score = {z_lower:.5f}")
            st.write(f"Upper Z-score = {z_upper:.5f}")

            st.subheader("Step 2: Probability")

            st.latex(
                r"P(a<X<b)=\Phi(Z_b)-\Phi(Z_a)"
            )

            st.metric(
                f"P({lower:.4f} < X < {upper:.4f})",
                f"{result:.8f}"
            )

            st.write(f"Percentage = {result * 100:.5f}%")

    st.subheader("Normal Curve")

    x_values = np.linspace(
        mu - 4 * sigma,
        mu + 4 * sigma,
        300
    )

    density = stats.norm.pdf(
        x_values,
        loc=mu,
        scale=sigma
    )

    st.line_chart(
        pd.DataFrame({
            "X": x_values,
            "Probability density": density
        }).set_index("X")
    )

# ==========================================================
# LEARNING NOTES
# ==========================================================

st.divider()

st.header("Quick Revision")

with st.expander("Chi-square tests"):
    st.write("""
    Goodness of fit checks whether observed frequencies agree with
    an expected distribution.

    Independence tests whether two categorical variables are associated.

    Both use a chi-square statistic based on observed and expected counts.
    """)

with st.expander("F-test"):
    st.write("""
    The classical F-test compares two population variances under
    normality and independence assumptions.

    F = Sample variance 1 / Sample variance 2.

    The order of the variances determines the numerator and denominator
    degrees of freedom.
    """)

with st.expander("ANOVA"):
    st.write("""
    One-way ANOVA compares the means of three or more independent groups.

    F = Between-group mean square / Within-group mean square.

    A significant result means at least one population mean differs;
    it does not establish which means differ.
    """)

with st.expander("Binomial distribution"):
    st.write("""
    Use when there is a fixed number of independent trials and each
    trial has two possible outcomes with a constant success probability.

    Mean = np.

    Variance = np(1 − p).
    """)

with st.expander("Poisson distribution"):
    st.write("""
    Use for event counts in a fixed interval when a stable event rate
    and appropriate independence assumptions are reasonable.

    Mean = λ.

    Variance = λ.
    """)

with st.expander("Normal distribution"):
    st.write("""
    Convert an observation to a Z-score using:

    Z = (X − μ) / σ.

    The Z-score indicates how many population standard deviations
    the observation lies above or below the mean.
    """)

st.caption(
    "Educational use: verify assumptions, sampling design and "
    "expected frequencies before drawing conclusions from real data."
)
```
