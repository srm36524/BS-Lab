import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Business Statistics Lab - Part 2",
    page_icon="📊",
    layout="wide"
)

if st.button("🏠 Return to Home"):
    st.switch_page("home.py")if st.button("🏠 Return to Home"):
    st.switch_page("home.py")

st.title("📊 Business Statistics Learning Lab")
st.header("Part 2: Dispersion, Skewness and Kurtosis")

st.write(
    "Explore Range, Quartile Deviation, Mean Deviation, "
    "Variance, Standard Deviation, Coefficient of Variation, "
    "Skewness and Kurtosis."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

data_type = st.sidebar.selectbox(
    "Type of Data",
    [
        "Individual Series",
        "Discrete Frequency Distribution",
        "Continuous Frequency Distribution"
    ]
)

measure = st.sidebar.selectbox(
    "Select Measure",
    [
        "Range",
        "Quartiles and Quartile Deviation",
        "Mean Deviation about Mean",
        "Mean Deviation about Median",
        "Variance and Standard Deviation",
        "Coefficient of Variation",
        "Karl Pearson Skewness",
        "Bowley Skewness",
        "Moment Coefficient of Skewness",
        "Kurtosis"
    ]
)

variance_type = st.sidebar.radio(
    "Variance / SD convention",
    ["Population", "Sample"]
)

# --------------------------------------------------
# COMMON HELPERS
# --------------------------------------------------

def fmt(x):
    return f"{x:,.4f}"


def show_formula(formula):
    st.markdown("### Formula")
    st.latex(formula)


def get_quartiles_individual(x):
    """
    Use the median-of-halves method:
    odd-sized data excludes the overall median from both halves.
    """
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)

    if n < 2:
        raise ValueError("At least two observations are required.")

    median = float(np.median(x))

    if n % 2 == 0:
        lower_half = x[:n // 2]
        upper_half = x[n // 2:]
    else:
        lower_half = x[:n // 2]
        upper_half = x[n // 2 + 1:]

    q1 = float(np.median(lower_half))
    q3 = float(np.median(upper_half))

    return q1, median, q3


def calc_weighted_stats(x, f):
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)

    n = f.sum()
    if n <= 0:
        raise ValueError("Total frequency must be greater than zero.")

    mean = np.sum(f * x) / n
    median = weighted_quantile(x, f, 0.50)

    return n, mean, median


def weighted_quantile(x, f, p):
    """
    Locate the observation at the first cumulative frequency
    reaching p*N. This is a discrete-frequency quantile convention.
    """
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)

    order = np.argsort(x)
    x = x[order]
    f = f[order]

    cf = np.cumsum(f)
    target = p * f.sum()

    idx = np.searchsorted(cf, target, side="left")
    idx = min(idx, len(x) - 1)

    return float(x[idx])


def grouped_quantile(lower, upper, f, p):
    """
    Grouped-data quantile:
    Qp = L + ((p*N - F)/f_q) * h
    """
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    f = np.asarray(f, dtype=float)

    N = f.sum()
    if N <= 0:
        raise ValueError("Total frequency must be greater than zero.")

    cf = np.cumsum(f)
    target = p * N

    idx = int(np.searchsorted(cf, target, side="left"))
    idx = min(idx, len(f) - 1)

    F = cf[idx - 1] if idx > 0 else 0
    fq = f[idx]
    h = upper[idx] - lower[idx]

    if fq <= 0:
        raise ValueError("Quantile class must have positive frequency.")

    q = lower[idx] + ((target - F) / fq) * h

    return float(q), idx, float(F), float(fq), float(h)


def parse_classes(class_text):
    classes = []

    for item in class_text:
        try:
            lo, hi = map(float, str(item).split("-"))
        except ValueError:
            raise ValueError(
                "Enter intervals such as 0-10, 10-20, 20-30."
            )

        if hi <= lo:
            raise ValueError("Upper limit must exceed lower limit.")

        classes.append((lo, hi))

    lower = np.array([a for a, b in classes], dtype=float)
    upper = np.array([b for a, b in classes], dtype=float)

    if np.any(lower[1:] < lower[:-1]):
        raise ValueError("Class intervals must be ordered.")

    if np.any(lower[1:] < upper[:-1]):
        raise ValueError("Class intervals must not overlap.")

    return lower, upper


# --------------------------------------------------
# INDIVIDUAL SERIES
# --------------------------------------------------

def individual_calculation(values, measure, variance_type):
    x = np.asarray(values, dtype=float)
    n = len(x)

    if n < 2:
        st.error("Enter at least two observations.")
        return

    xs = np.sort(x)
    mean = np.mean(x)
    median = np.median(x)
    deviations_mean = np.abs(x - mean)
    deviations_median = np.abs(x - median)

    if measure == "Range":
        value = np.max(x) - np.min(x)

        show_formula(r"\text{Range}=X_{\max}-X_{\min}")
        st.write(f"Maximum value = {np.max(x):g}")
        st.write(f"Minimum value = {np.min(x):g}")
        st.success(f"Range = {fmt(value)}")

    elif measure == "Quartiles and Quartile Deviation":
        q1, q2, q3 = get_quartiles_individual(x)
        iqr = q3 - q1
        qd = iqr / 2

        show_formula(r"QD=\frac{Q_3-Q_1}{2}")

        st.write("Sorted observations:")
        st.write(xs.tolist())
        st.write(f"First quartile Q1 = {fmt(q1)}")
        st.write(f"Median Q2 = {fmt(q2)}")
        st.write(f"Third quartile Q3 = {fmt(q3)}")
        st.write(f"Interquartile range = Q3 − Q1 = {fmt(iqr)}")
        st.success(f"Quartile Deviation = {fmt(qd)}")

        st.caption(
            "Quartiles can differ slightly across textbooks because "
            "different quartile conventions are used. This app uses "
            "the median-of-halves method for individual data."
        )

    elif measure in [
        "Mean Deviation about Mean",
        "Mean Deviation about Median"
    ]:
        if measure == "Mean Deviation about Mean":
            center = mean
            dev = np.abs(x - mean)
            center_name = "Mean"
        else:
            center = median
            dev = np.abs(x - median)
            center_name = "Median"

        md = np.mean(dev)

        show_formula(r"MD=\frac{\sum |x-A|}{n}")

        table = pd.DataFrame({
            "x": x,
            "x − A": x - center,
            "|x − A|": dev
        })

        st.dataframe(table, use_container_width=True)
        st.write(f"{center_name} (A) = {fmt(center)}")
        st.write(f"Sum of absolute deviations = {fmt(dev.sum())}")
        st.success(f"Mean Deviation = {fmt(md)}")

    elif measure in [
        "Variance and Standard Deviation",
        "Coefficient of Variation"
    ]:
        if variance_type == "Population":
            denominator = n
            label = "Population"
        else:
            denominator = n - 1
            label = "Sample"

        squared_dev = (x - mean) ** 2
        ss = squared_dev.sum()
        variance = ss / denominator
        sd = np.sqrt(variance)
        cv = sd / mean * 100 if mean != 0 else np.nan

        show_formula(
            r"\sigma^2=\frac{\sum(x-\bar{x})^2}{N}"
            r"\quad\text{(population)}"
        )
        st.latex(
            r"s^2=\frac{\sum(x-\bar{x})^2}{n-1}"
            r"\quad\text{(sample)}"
        )

        table = pd.DataFrame({
            "x": x,
            "x − Mean": x - mean,
            "(x − Mean)²": squared_dev
        })

        st.dataframe(table, use_container_width=True)
        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Sum of squared deviations = {fmt(ss)}")
        st.write(f"Denominator = {denominator}")

        st.success(f"{label} Variance = {fmt(variance)}")
        st.success(f"{label} Standard Deviation = {fmt(sd)}")

        if measure == "Coefficient of Variation":
            show_formula(r"CV=\frac{SD}{\bar{x}}\times100")
            if np.isfinite(cv):
                st.success(f"Coefficient of Variation = {fmt(cv)}%")
                st.write(
                    "A lower CV indicates less relative variability "
                    "when comparing datasets measured on a comparable "
                    "basis and with a meaningful positive mean."
                )
            else:
                st.warning(
                    "CV is undefined because the mean is zero."
                )

    elif measure == "Karl Pearson Skewness":
        modes = pd.Series(x).mode().to_numpy()
        mode = modes[0] if len(modes) == 1 else np.nan
        sd_pop = np.sqrt(np.mean((x - mean) ** 2))

        show_formula(r"Sk=\frac{\bar{x}-Mode}{SD}")
        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Mode(s) = {modes.tolist()}")
        st.write(f"Population SD = {fmt(sd_pop)}")

        if np.isfinite(mode) and sd_pop != 0:
            sk = (mean - mode) / sd_pop
            st.success(f"Karl Pearson Skewness = {fmt(sk)}")
        else:
            st.warning(
                "This coefficient is unavailable because there is "
                "no unique mode or the standard deviation is zero."
            )

        show_formula(r"Sk=\frac{3(\bar{x}-Median)}{SD}")
        if sd_pop != 0:
            sk2 = 3 * (mean - median) / sd_pop
            st.success(
                f"Alternative Pearson Skewness = {fmt(sk2)}"
            )

    elif measure == "Bowley Skewness":
        q1, q2, q3 = get_quartiles_individual(x)
        denominator = q3 - q1

        show_formula(
            r"Sk_B=\frac{Q_3+Q_1-2Q_2}{Q_3-Q_1}"
        )

        st.write(f"Q1 = {fmt(q1)}")
        st.write(f"Q2 = {fmt(q2)}")
        st.write(f"Q3 = {fmt(q3)}")

        if denominator != 0:
            bowley = (q3 + q1 - 2 * q2) / denominator
            st.success(f"Bowley Skewness = {fmt(bowley)}")
        else:
            st.warning("Bowley skewness is undefined when Q3 = Q1.")

    elif measure == "Moment Coefficient of Skewness":
        mu2 = np.mean((x - mean) ** 2)
        mu3 = np.mean((x - mean) ** 3)

        show_formula(r"\gamma_1=\frac{\mu_3}{\mu_2^{3/2}}")

        if mu2 > 0:
            skew = mu3 / (mu2 ** 1.5)
            st.write(f"Second central moment μ2 = {fmt(mu2)}")
            st.write(f"Third central moment μ3 = {fmt(mu3)}")
            st.success(f"Moment Skewness γ1 = {fmt(skew)}")
        else:
            st.warning("Skewness is undefined when all values are equal.")

    elif measure == "Kurtosis":
        mu2 = np.mean((x - mean) ** 2)
        mu4 = np.mean((x - mean) ** 4)

        show_formula(r"\beta_2=\frac{\mu_4}{\mu_2^2}")

        if mu2 > 0:
            beta2 = mu4 / (mu2 ** 2)
            excess = beta2 - 3

            st.write(f"Second central moment μ2 = {fmt(mu2)}")
            st.write(f"Fourth central moment μ4 = {fmt(mu4)}")
            st.write(f"Kurtosis β2 = {fmt(beta2)}")
            st.write(f"Excess kurtosis = β2 − 3 = {fmt(excess)}")

            if np.isclose(excess, 0, atol=0.05):
                shape = "Approximately mesokurtic"
            elif excess > 0:
                shape = "Leptokurtic relative to the normal distribution"
            else:
                shape = "Platykurtic relative to the normal distribution"

            st.success(shape)
        else:
            st.warning("Kurtosis is undefined when all values are equal.")


# --------------------------------------------------
# DISCRETE FREQUENCY SERIES
# --------------------------------------------------

def discrete_calculation(values, frequencies, measure, variance_type):
    x = np.asarray(values, dtype=float)
    f = np.asarray(frequencies, dtype=float)

    if len(x) != len(f):
        st.error("Each value needs a frequency.")
        return

    if np.any(f < 0) or np.any(f != np.floor(f)):
        st.error("Frequencies must be non-negative whole numbers.")
        return

    if f.sum() <= 0:
        st.error("Total frequency must be positive.")
        return

    if len(set(x)) != len(x):
        st.error("Enter each distinct value only once.")
        return

    order = np.argsort(x)
    x, f = x[order], f[order]

    N = f.sum()
    mean = np.sum(f * x) / N
    median = weighted_quantile(x, f, 0.5)

    modes = x[f == f.max()]
    mode = modes[0] if len(modes) == 1 else np.nan

    if measure == "Range":
        value = x.max() - x.min()
        show_formula(r"\text{Range}=X_{\max}-X_{\min}")
        st.write(f"Maximum = {x.max():g}")
        st.write(f"Minimum = {x.min():g}")
        st.success(f"Range = {fmt(value)}")

    elif measure == "Quartiles and Quartile Deviation":
        q1 = weighted_quantile(x, f, 0.25)
        q2 = weighted_quantile(x, f, 0.50)
        q3 = weighted_quantile(x, f, 0.75)

        show_formula(r"QD=\frac{Q_3-Q_1}{2}")

        st.write(f"Q1 = {fmt(q1)}")
        st.write(f"Q2 = {fmt(q2)}")
        st.write(f"Q3 = {fmt(q3)}")
        st.success(f"Quartile Deviation = {fmt((q3-q1)/2)}")

        st.caption(
            "For discrete frequency data, quartiles are located "
            "using cumulative frequencies. Other textbook conventions "
            "may yield different quartiles."
        )

    elif measure in [
        "Mean Deviation about Mean",
        "Mean Deviation about Median"
    ]:
        if measure == "Mean Deviation about Mean":
            center = mean
            name = "Mean"
        else:
            center = median
            name = "Median"

        abs_dev = np.abs(x - center)
        f_abs_dev = f * abs_dev
        md = f_abs_dev.sum() / N

        show_formula(r"MD=\frac{\sum f|x-A|}{N}")

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "|x − A|": abs_dev,
            "f|x − A|": f_abs_dev
        })
        st.dataframe(table, use_container_width=True)
        st.write(f"{name} (A) = {fmt(center)}")
        st.write(f"Sum of f|x − A| = {fmt(f_abs_dev.sum())}")
        st.success(f"Mean Deviation = {fmt(md)}")

    elif measure in [
        "Variance and Standard Deviation",
        "Coefficient of Variation"
    ]:
        denominator = N if variance_type == "Population" else N - 1
        if denominator <= 0:
            st.error("Insufficient observations for sample variance.")
            return

        sq_dev = (x - mean) ** 2
        f_sq_dev = f * sq_dev
        variance = f_sq_dev.sum() / denominator
        sd = np.sqrt(variance)
        cv = sd / mean * 100 if mean != 0 else np.nan

        show_formula(
            r"\sigma^2=\frac{\sum f(x-\bar{x})^2}{N}"
            r"\quad\text{(population)}"
        )
        st.latex(
            r"s^2=\frac{\sum f(x-\bar{x})^2}{N-1}"
            r"\quad\text{(frequency data treated as a sample)}"
        )

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "x − Mean": x - mean,
            "(x − Mean)²": sq_dev,
            "f(x − Mean)²": f_sq_dev
        })
        st.dataframe(table, use_container_width=True)

        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Sum of f(x − Mean)² = {fmt(f_sq_dev.sum())}")
        st.success(f"{variance_type} Variance = {fmt(variance)}")
        st.success(f"{variance_type} SD = {fmt(sd)}")

        if measure == "Coefficient of Variation":
            show_formula(r"CV=\frac{SD}{\bar{x}}\times100")
            if np.isfinite(cv):
                st.success(f"CV = {fmt(cv)}%")
            else:
                st.warning("CV is undefined because the mean is zero.")

    elif measure == "Karl Pearson Skewness":
        sd = np.sqrt(np.sum(f * (x - mean) ** 2) / N)

        show_formula(r"Sk=\frac{\bar{x}-Mode}{SD}")
        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Mode(s) = {modes.tolist()}")
        st.write(f"Population SD = {fmt(sd)}")

        if np.isfinite(mode) and sd > 0:
            st.success(
                f"Karl Pearson Skewness = {fmt((mean-mode)/sd)}"
            )
        else:
            st.warning("No unique mode or zero SD.")

        show_formula(r"Sk=\frac{3(\bar{x}-Median)}{SD}")
        if sd > 0:
            st.success(
                "Alternative Pearson Skewness = "
                + fmt(3 * (mean - median) / sd)
            )

    elif measure == "Bowley Skewness":
        q1 = weighted_quantile(x, f, 0.25)
        q2 = weighted_quantile(x, f, 0.50)
        q3 = weighted_quantile(x, f, 0.75)

        show_formula(r"Sk_B=\frac{Q_3+Q_1-2Q_2}{Q_3-Q_1}")

        st.write(f"Q1 = {fmt(q1)}")
        st.write(f"Q2 = {fmt(q2)}")
        st.write(f"Q3 = {fmt(q3)}")

        if q3 != q1:
            st.success(
                "Bowley Skewness = "
                + fmt((q3 + q1 - 2*q2)/(q3-q1))
            )
        else:
            st.warning("Undefined because Q3 equals Q1.")

    elif measure in ["Moment Coefficient of Skewness", "Kurtosis"]:
        mu2 = np.sum(f * (x - mean) ** 2) / N

        if mu2 <= 0:
            st.warning("Shape measure is undefined when all values are equal.")
            return

        if measure == "Moment Coefficient of Skewness":
            mu3 = np.sum(f * (x - mean) ** 3) / N
            skew = mu3 / (mu2 ** 1.5)

            show_formula(r"\gamma_1=\frac{\mu_3}{\mu_2^{3/2}}")
            st.write(f"μ2 = {fmt(mu2)}")
            st.write(f"μ3 = {fmt(mu3)}")
            st.success(f"Moment Skewness = {fmt(skew)}")

        else:
            mu4 = np.sum(f * (x - mean) ** 4) / N
            beta2 = mu4 / (mu2 ** 2)
            excess = beta2 - 3

            show_formula(r"\beta_2=\frac{\mu_4}{\mu_2^2}")
            st.write(f"μ2 = {fmt(mu2)}")
            st.write(f"μ4 = {fmt(mu4)}")
            st.write(f"Kurtosis β2 = {fmt(beta2)}")
            st.success(f"Excess Kurtosis = {fmt(excess)}")


# --------------------------------------------------
# CONTINUOUS FREQUENCY SERIES
# --------------------------------------------------

def continuous_calculation(classes, frequencies, measure, variance_type):
    lower, upper = parse_classes(classes)
    f = np.asarray(frequencies, dtype=float)

    if len(lower) != len(f):
        st.error("Each class interval needs a frequency.")
        return

    if np.any(f < 0) or np.any(f != np.floor(f)):
        st.error("Frequencies must be non-negative whole numbers.")
        return

    N = f.sum()
    if N <= 0:
        st.error("Total frequency must be positive.")
        return

    midpoint = (lower + upper) / 2
    width = upper - lower

    mean = np.sum(f * midpoint) / N
    cf = np.cumsum(f)

    if measure == "Range":
        value = upper.max() - lower.min()
        show_formula(r"\text{Range}=\text{Upper limit of last class}-\text{Lower limit of first class}")
        st.write(f"Lowest boundary = {lower.min():g}")
        st.write(f"Highest boundary = {upper.max():g}")
        st.success(f"Approximate Range = {fmt(value)}")

    elif measure == "Quartiles and Quartile Deviation":
        q1, i1, F1, fq1, h1 = grouped_quantile(lower, upper, f, 0.25)
        q2, i2, F2, fq2, h2 = grouped_quantile(lower, upper, f, 0.50)
        q3, i3, F3, fq3, h3 = grouped_quantile(lower, upper, f, 0.75)

        show_formula(r"Q_k=L+\left(\frac{kN/4-F}{f_q}\right)h")
        st.write(f"Q1 class = {classes[i1]}")
        st.write(f"Q1 = {fmt(q1)}")
        st.write(f"Q2 (Median) = {fmt(q2)}")
        st.write(f"Q3 class = {classes[i3]}")
        st.write(f"Q3 = {fmt(q3)}")
        st.write(f"Interquartile Range = {fmt(q3-q1)}")
        st.success(f"Quartile Deviation = {fmt((q3-q1)/2)}")

    elif measure in [
        "Mean Deviation about Mean",
        "Mean Deviation about Median"
    ]:
        if measure == "Mean Deviation about Mean":
            center = mean
            name = "Mean"
        else:
            center, _, _, _, _ = grouped_quantile(lower, upper, f, 0.5)
            name = "Median"

        abs_dev = np.abs(midpoint - center)
        f_abs_dev = f * abs_dev
        md = f_abs_dev.sum() / N

        show_formula(r"MD=\frac{\sum f|x-A|}{N}")

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Midpoint (x)": midpoint,
            "|x − A|": abs_dev,
            "f|x − A|": f_abs_dev
        })
        st.dataframe(table, use_container_width=True)
        st.write(f"{name} (A) = {fmt(center)}")
        st.write(f"Sum of f|x − A| = {fmt(f_abs_dev.sum())}")
        st.success(f"Mean Deviation = {fmt(md)}")

    elif measure in [
        "Variance and Standard Deviation",
        "Coefficient of Variation"
    ]:
        denominator = N if variance_type == "Population" else N - 1
        if denominator <= 0:
            st.error("Insufficient observations for sample variance.")
            return

        sq_dev = (midpoint - mean) ** 2
        f_sq_dev = f * sq_dev
        variance = f_sq_dev.sum() / denominator
        sd = np.sqrt(variance)
        cv = sd / mean * 100 if mean != 0 else np.nan

        show_formula(
            r"\sigma^2=\frac{\sum f(x-\bar{x})^2}{N}"
            r"\quad\text{(population)}"
        )
        st.latex(
            r"s^2=\frac{\sum f(x-\bar{x})^2}{N-1}"
            r"\quad\text{(sample approximation)}"
        )

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Midpoint (x)": midpoint,
            "x − Mean": midpoint - mean,
            "(x − Mean)²": sq_dev,
            "f(x − Mean)²": f_sq_dev
        })
        st.dataframe(table, use_container_width=True)
        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Sum of f(x − Mean)² = {fmt(f_sq_dev.sum())}")
        st.success(f"{variance_type} Variance = {fmt(variance)}")
        st.success(f"{variance_type} Standard Deviation = {fmt(sd)}")

        if measure == "Coefficient of Variation":
            show_formula(r"CV=\frac{SD}{\bar{x}}\times100")
            if np.isfinite(cv):
                st.success(f"CV = {fmt(cv)}%")
            else:
                st.warning("CV is undefined because the mean is zero.")

    elif measure == "Karl Pearson Skewness":
        sd = np.sqrt(np.sum(f * (midpoint - mean) ** 2) / N)

        modal_idx = int(np.argmax(f))
        fm = f[modal_idx]
        f1 = f[modal_idx - 1] if modal_idx > 0 else 0
        f2 = f[modal_idx + 1] if modal_idx < len(f) - 1 else 0
        denom = 2 * fm - f1 - f2

        show_formula(r"Sk=\frac{\bar{x}-Mode}{SD}")

        st.write(f"Mean = {fmt(mean)}")
        st.write(f"Population SD = {fmt(sd)}")
        st.write(f"Modal class = {classes[modal_idx]}")

        if denom != 0:
            mode = lower[modal_idx] + (
                (fm - f1) / denom
            ) * width[modal_idx]

            st.write(f"Estimated Mode = {fmt(mode)}")

            if sd > 0:
                st.success(
                    f"Karl Pearson Skewness = {fmt((mean-mode)/sd)}"
                )
        else:
            st.warning("Grouped mode formula has a zero denominator.")

        median, _, _, _, _ = grouped_quantile(lower, upper, f, 0.5)
        show_formula(r"Sk=\frac{3(\bar{x}-Median)}{SD}")

        if sd > 0:
            st.success(
                "Alternative Pearson Skewness = "
                + fmt(3 * (mean-median)/sd)
            )

    elif measure == "Bowley Skewness":
        q1, *_ = grouped_quantile(lower, upper, f, 0.25)
        q2, *_ = grouped_quantile(lower, upper, f, 0.50)
        q3, *_ = grouped_quantile(lower, upper, f, 0.75)

        show_formula(r"Sk_B=\frac{Q_3+Q_1-2Q_2}{Q_3-Q_1}")

        st.write(f"Q1 = {fmt(q1)}")
        st.write(f"Q2 = {fmt(q2)}")
        st.write(f"Q3 = {fmt(q3)}")

        if q3 != q1:
            st.success(
                "Bowley Skewness = "
                + fmt((q3 + q1 - 2*q2)/(q3-q1))
            )
        else:
            st.warning("Undefined because Q3 equals Q1.")

    elif measure in ["Moment Coefficient of Skewness", "Kurtosis"]:
        mu2 = np.sum(f * (midpoint - mean) ** 2) / N

        if mu2 <= 0:
            st.warning("Shape measure is undefined when all midpoints are equal.")
            return

        if measure == "Moment Coefficient of Skewness":
            mu3 = np.sum(f * (midpoint - mean) ** 3) / N
            skew = mu3 / (mu2 ** 1.5)

            show_formula(r"\gamma_1=\frac{\mu_3}{\mu_2^{3/2}}")
            st.write(f"μ2 = {fmt(mu2)}")
            st.write(f"μ3 = {fmt(mu3)}")
            st.success(f"Moment Skewness = {fmt(skew)}")

        else:
            mu4 = np.sum(f * (midpoint - mean) ** 4) / N
            beta2 = mu4 / (mu2 ** 2)
            excess = beta2 - 3

            show_formula(r"\beta_2=\frac{\mu_4}{\mu_2^2}")
            st.write(f"μ2 = {fmt(mu2)}")
            st.write(f"μ4 = {fmt(mu4)}")
            st.write(f"Kurtosis β2 = {fmt(beta2)}")
            st.success(f"Excess Kurtosis = {fmt(excess)}")


# --------------------------------------------------
# INPUTS AND CALCULATION
# --------------------------------------------------

st.markdown("---")
st.subheader("Enter Sample Data")

try:
    if data_type == "Individual Series":
        raw = st.text_area(
            "Observations (comma-separated)",
            "10, 12, 15, 18, 20, 25"
        )

        if st.button("Calculate", type="primary"):
            values = [
                float(v.strip())
                for v in raw.replace("\n", ",").split(",")
                if v.strip()
            ]
            individual_calculation(values, measure, variance_type)

    elif data_type == "Discrete Frequency Distribution":
        sample = pd.DataFrame({
            "Value (x)": [10, 20, 30, 40, 50],
            "Frequency (f)": [2, 4, 6, 5, 3]
        })

        edited = st.data_editor(
            sample,
            num_rows="dynamic",
            use_container_width=True
        )

        if st.button("Calculate", type="primary"):
            values = pd.to_numeric(
                edited["Value (x)"], errors="raise"
            ).to_numpy()

            frequencies = pd.to_numeric(
                edited["Frequency (f)"], errors="raise"
            ).to_numpy()

            discrete_calculation(
                values, frequencies, measure, variance_type
            )

    else:
        sample = pd.DataFrame({
            "Class Interval": [
                "0-10", "10-20", "20-30",
                "30-40", "40-50"
            ],
            "Frequency (f)": [3, 7, 12, 8, 5]
        })

        edited = st.data_editor(
            sample,
            num_rows="dynamic",
            use_container_width=True
        )

        if st.button("Calculate", type="primary"):
            classes = edited["Class Interval"].astype(str).tolist()

            frequencies = pd.to_numeric(
                edited["Frequency (f)"], errors="raise"
            ).to_numpy()

            continuous_calculation(
                classes, frequencies, measure, variance_type
            )

except (ValueError, TypeError, ZeroDivisionError) as e:
    st.error(f"Please check your input: {e}")


# --------------------------------------------------
# INTERPRETATION GUIDE
# --------------------------------------------------

st.markdown("---")
st.header("Learning Notes")

with st.expander("Range and Quartile Deviation"):
    st.write(
        "Range measures the distance between the largest and "
        "smallest observations. Quartile deviation is half the "
        "interquartile range and focuses on the middle 50%."
    )

with st.expander("Mean Deviation"):
    st.write(
        "Mean deviation is the average of the absolute deviations "
        "from a chosen central value. Absolute values prevent "
        "positive and negative deviations from cancelling."
    )

with st.expander("Variance and Standard Deviation"):
    st.write(
        "Variance averages squared deviations from the mean. "
        "Standard deviation is the square root of variance and "
        "is expressed in the original measurement units."
    )

with st.expander("Population versus Sample"):
    st.write(
        "Population variance divides by N. The conventional "
        "unbiased sample variance divides by n − 1. For frequency "
        "data, N is the total frequency. In grouped data, calculations "
        "approximate the original observations using class midpoints."
    )

with st.expander("Coefficient of Variation"):
    st.write(
        "CV = SD / Mean × 100. It measures relative variability. "
        "Use caution when the mean is zero or negative."
    )

with st.expander("Skewness"):
    st.write(
        "Positive skewness indicates a longer right tail; negative "
        "skewness indicates a longer left tail. A value near zero "
        "suggests approximate symmetry, depending on the measure used."
    )

with st.expander("Kurtosis"):
    st.write(
        "Pearson kurtosis β₂ is 3 for a normal distribution. "
        "Excess kurtosis is β₂ − 3: positive indicates leptokurtic, "
        "negative indicates platykurtic, and zero indicates "
        "mesokurtic relative to the normal distribution."
    )

st.caption("Business Statistics Learning Lab | Part 2")
