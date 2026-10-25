import streamlit as st
import pandas as pd
import numpy as np
import math

st.set_page_config(
    page_title="Business Statistics Learning Lab",
    page_icon="📊",
    layout="wide"
)

if st.button("🏠 Return to Home"):
    st.switch_page("home.py")
    
st.title("📊 Business Statistics Learning Lab")
st.subheader("Part 1: Measures of Central Tendency")

st.write(
    "Calculate Mean, Median, Mode, Geometric Mean and "
    "Harmonic Mean with step-by-step working."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

data_type = st.sidebar.selectbox(
    "Select Type of Data",
    [
        "Individual Series",
        "Discrete Frequency Distribution",
        "Continuous Frequency Distribution"
    ]
)

measure = st.sidebar.selectbox(
    "Select Measure",
    [
        "Mean",
        "Median",
        "Mode",
        "Geometric Mean",
        "Harmonic Mean"
    ]
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def parse_numbers(text):
    """Convert comma-separated input into numeric values."""
    try:
        values = [
            float(x.strip())
            for x in text.replace("\n", ",").split(",")
            if x.strip()
        ]

        if not values:
            raise ValueError("Enter at least one number.")

        return values

    except ValueError:
        raise ValueError(
            "Enter valid numbers separated by commas."
        )


def format_num(x):
    if isinstance(x, (int, np.integer)):
        return str(x)

    return f"{x:,.4f}"


def calculate_individual(values, measure):
    """Calculations for individual observations."""

    x = np.array(values, dtype=float)
    n = len(x)

    if measure == "Mean":
        total = x.sum()
        mean = total / n

        table = pd.DataFrame({
            "Observation (x)": x,
            "Working": [f"{v:g}" for v in x]
        })

        st.markdown("### Formula")
        st.latex(r"\bar{x}=\frac{\sum x}{n}")

        st.markdown("### Step-by-step calculation")
        st.write(f"Number of observations (n) = {n}")
        st.write(f"Sum of observations = {format_num(total)}")
        st.latex(
            rf"\bar{{x}}=\frac{{{format_num(total)}}}{{{n}}}"
            rf"={format_num(mean)}"
        )

        st.dataframe(table, use_container_width=True)
        st.success(f"Arithmetic Mean = {format_num(mean)}")

    elif measure == "Median":
        sorted_x = np.sort(x)

        table = pd.DataFrame({
            "Position": range(1, n + 1),
            "Sorted Observation": sorted_x
        })

        st.markdown("### Formula")
        st.latex(
            r"\text{Median}="
            r"\begin{cases}"
            r"x_{\left(\frac{n+1}{2}\right)}, & n\text{ odd}\\"
            r"\frac{x_{(n/2)}+x_{(n/2+1)}}{2}, & n\text{ even}"
            r"\end{cases}"
        )

        if n % 2 == 1:
            position = (n + 1) // 2
            median = sorted_x[position - 1]

            st.write(f"Number of observations = {n} (odd)")
            st.write(f"Median position = ({n} + 1) / 2 = {position}")
            st.write(f"Value at position {position} = {median:g}")

        else:
            p1 = n // 2
            p2 = p1 + 1
            v1 = sorted_x[p1 - 1]
            v2 = sorted_x[p2 - 1]
            median = (v1 + v2) / 2

            st.write(f"Number of observations = {n} (even)")
            st.write(f"Middle positions = {p1} and {p2}")
            st.write(f"Middle values = {v1:g} and {v2:g}")
            st.write(
                f"Median = ({v1:g} + {v2:g}) / 2 "
                f"= {format_num(median)}"
            )

        st.dataframe(table, use_container_width=True)
        st.success(f"Median = {format_num(median)}")

    elif measure == "Mode":
        counts = pd.Series(x).value_counts()
        max_frequency = counts.max()
        modes = sorted(counts[counts == max_frequency].index.tolist())

        table = (
            pd.DataFrame({
                "Value": counts.index,
                "Frequency": counts.values
            })
            .sort_values("Value")
            .reset_index(drop=True)
        )

        st.markdown("### Method")
        st.write(
            "The mode is the value that occurs most frequently."
        )

        st.dataframe(table, use_container_width=True)

        if max_frequency == 1:
            st.info(
                "Every value occurs once. There is no unique mode."
            )
        else:
            st.write(f"Highest frequency = {max_frequency}")
            st.write(f"Value(s) with highest frequency = {modes}")
            st.success(
                "Mode = " + ", ".join(format_num(v) for v in modes)
            )

    elif measure == "Geometric Mean":
        if np.any(x <= 0):
            st.error(
                "Geometric Mean requires all observations "
                "to be positive."
            )
            return

        logs = np.log(x)
        log_sum = logs.sum()
        gm = np.exp(log_sum / n)

        table = pd.DataFrame({
            "x": x,
            "ln(x)": logs
        })

        st.markdown("### Formula")
        st.latex(
            r"GM=\left(\prod x\right)^{1/n}"
            r"=\operatorname{antilog}"
            r"\left(\frac{\sum\ln x}{n}\right)"
        )

        st.write(f"Number of observations = {n}")
        st.write(f"Sum of natural logarithms = {format_num(log_sum)}")
        st.write(f"Average of logarithms = {format_num(log_sum / n)}")

        st.dataframe(table, use_container_width=True)
        st.latex(
            rf"GM=e^{{{format_num(log_sum / n)}}}"
            rf"={format_num(gm)}"
        )
        st.success(f"Geometric Mean = {format_num(gm)}")

    elif measure == "Harmonic Mean":
        if np.any(x <= 0):
            st.error(
                "Harmonic Mean requires all observations "
                "to be positive."
            )
            return

        reciprocals = 1 / x
        reciprocal_sum = reciprocals.sum()
        hm = n / reciprocal_sum

        table = pd.DataFrame({
            "x": x,
            "1/x": reciprocals
        })

        st.markdown("### Formula")
        st.latex(r"HM=\frac{n}{\sum(1/x)}")

        st.write(f"Number of observations = {n}")
        st.write(
            f"Sum of reciprocals = {format_num(reciprocal_sum)}"
        )

        st.dataframe(table, use_container_width=True)
        st.latex(
            rf"HM=\frac{{{n}}}{{{format_num(reciprocal_sum)}}}"
            rf"={format_num(hm)}"
        )
        st.success(f"Harmonic Mean = {format_num(hm)}")


def calculate_frequency(values, frequencies, measure):
    """Calculations for discrete frequency distributions."""

    x = np.array(values, dtype=float)
    f = np.array(frequencies, dtype=float)

    if len(x) != len(f):
        st.error("Each value must have a corresponding frequency.")
        return

    if np.any(f < 0) or np.any(f != np.floor(f)):
        st.error("Frequencies must be non-negative whole numbers.")
        return

    if f.sum() <= 0:
        st.error("The total frequency must be greater than zero.")
        return

    if len(set(x)) != len(x):
        st.error(
            "Please enter each distinct value only once. "
            "Combine frequencies for repeated values."
        )
        return

    order = np.argsort(x)
    x = x[order]
    f = f[order]

    N = int(f.sum())
    fx = f * x

    if measure == "Mean":
        total_fx = fx.sum()
        mean = total_fx / N

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "fx": fx
        })

        st.markdown("### Formula")
        st.latex(r"\bar{x}=\frac{\sum fx}{\sum f}")

        st.dataframe(table, use_container_width=True)
        st.write(f"Total frequency (N) = {N}")
        st.write(f"Sum of fx = {format_num(total_fx)}")

        st.latex(
            rf"\bar{{x}}=\frac{{{format_num(total_fx)}}}"
            rf"{{{N}}}={format_num(mean)}"
        )
        st.success(f"Arithmetic Mean = {format_num(mean)}")

    elif measure == "Median":
        cf = np.cumsum(f)

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "Cumulative Frequency": cf.astype(int)
        })

        # For integer frequencies, use the two middle observations
        # when N is even; otherwise use the single middle observation.
        if N % 2 == 1:
            positions = [(N + 1) // 2]
        else:
            positions = [N // 2, N // 2 + 1]

        middle_values = []
        for pos in positions:
            idx = np.searchsorted(cf, pos, side="left")
            middle_values.append(x[idx])

        median = float(np.mean(middle_values))

        st.markdown("### Formula")
        st.write(
            "Locate the middle observation(s) using cumulative "
            "frequency."
        )
        st.dataframe(table, use_container_width=True)
        st.write(f"Total frequency (N) = {N}")
        st.write(f"Middle position(s) = {positions}")
        st.write(f"Corresponding value(s) = {middle_values}")
        st.success(f"Median = {format_num(median)}")

    elif measure == "Mode":
        max_f = f.max()
        modes = x[f == max_f]

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int)
        })

        st.markdown("### Method")
        st.write("The mode is the value with the highest frequency.")
        st.dataframe(table, use_container_width=True)
        st.write(f"Highest frequency = {int(max_f)}")

        if len(modes) == len(x):
            st.info(
                "All values have the same frequency. "
                "There is no unique mode."
            )
        else:
            st.write(f"Modal value(s) = {modes.tolist()}")
            st.success(
                "Mode = " + ", ".join(format_num(v) for v in modes)
            )

    elif measure == "Geometric Mean":
        if np.any(x <= 0):
            st.error(
                "Geometric Mean requires positive values."
            )
            return

        logs = np.log(x)
        flog = f * logs
        sum_flog = flog.sum()
        gm = np.exp(sum_flog / N)

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "ln(x)": logs,
            "f × ln(x)": flog
        })

        st.markdown("### Formula")
        st.latex(
            r"GM=\operatorname{antilog}"
            r"\left(\frac{\sum f\log x}{N}\right)"
        )

        st.dataframe(table, use_container_width=True)
        st.write(f"Total frequency (N) = {N}")
        st.write(f"Sum of f ln(x) = {format_num(sum_flog)}")
        st.write(
            f"Average logarithm = {format_num(sum_flog / N)}"
        )

        st.success(f"Geometric Mean = {format_num(gm)}")

    elif measure == "Harmonic Mean":
        if np.any(x <= 0):
            st.error(
                "Harmonic Mean requires positive values."
            )
            return

        reciprocals = 1 / x
        f_reciprocal = f * reciprocals
        sum_f_reciprocal = f_reciprocal.sum()
        hm = N / sum_f_reciprocal

        table = pd.DataFrame({
            "x": x,
            "f": f.astype(int),
            "1/x": reciprocals,
            "f/x": f_reciprocal
        })

        st.markdown("### Formula")
        st.latex(r"HM=\frac{N}{\sum(f/x)}")

        st.dataframe(table, use_container_width=True)
        st.write(f"Total frequency (N) = {N}")
        st.write(
            f"Sum of f/x = {format_num(sum_f_reciprocal)}"
        )
        st.success(f"Harmonic Mean = {format_num(hm)}")


def calculate_continuous(classes, frequencies, measure):
    """Calculations for grouped continuous frequency distributions."""

    rows = []

    for item in classes:
        try:
            lower, upper = map(float, item.split("-"))
        except ValueError:
            st.error(
                "Enter class intervals in the format 0-10, 10-20, etc."
            )
            return

        if upper <= lower:
            st.error("Each upper class boundary must exceed its lower boundary.")
            return

        rows.append((lower, upper))

    f = np.array(frequencies, dtype=float)

    if len(rows) != len(f):
        st.error(
            "The number of class intervals must match the number "
            "of frequencies."
        )
        return

    if np.any(f < 0) or np.any(f != np.floor(f)):
        st.error("Frequencies must be non-negative whole numbers.")
        return

    if f.sum() <= 0:
        st.error("The total frequency must be greater than zero.")
        return

    lower = np.array([r[0] for r in rows])
    upper = np.array([r[1] for r in rows])

    if np.any(lower[1:] < lower[:-1]) or np.any(
        lower[1:] < upper[:-1]
    ):
        st.error(
            "Please enter ordered, non-overlapping class intervals."
        )
        return

    width = upper - lower
    midpoint = (lower + upper) / 2
    N = int(f.sum())
    cf = np.cumsum(f)

    if measure == "Mean":
        fx = f * midpoint
        sum_fx = fx.sum()
        mean = sum_fx / N

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Midpoint (x)": midpoint,
            "fx": fx
        })

        st.markdown("### Formula")
        st.latex(r"\bar{x}=\frac{\sum fx}{N}")

        st.dataframe(table, use_container_width=True)
        st.write(f"Total frequency (N) = {N}")
        st.write(f"Sum of fx = {format_num(sum_fx)}")
        st.success(f"Mean = {format_num(mean)}")

    elif measure == "Median":
        median_idx = int(np.searchsorted(cf, N / 2, side="left"))

        L = lower[median_idx]
        F = cf[median_idx - 1] if median_idx > 0 else 0
        fm = f[median_idx]
        h = width[median_idx]

        median = L + ((N / 2 - F) / fm) * h

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Cumulative Frequency": cf.astype(int),
            "Lower Boundary (L)": lower,
            "Class Width (h)": width
        })

        st.markdown("### Formula")
        st.latex(
            r"\text{Median}=L+\left(\frac{N/2-F}{f_m}\right)h"
        )

        st.dataframe(table, use_container_width=True)
        st.write(f"N = {N}; N/2 = {N / 2:g}")
        st.write(f"Median class = {classes[median_idx]}")
        st.write(f"L = {L:g}, F = {F:g}, fm = {fm:g}, h = {h:g}")
        st.latex(
            rf"\text{{Median}}={L:g}"
            rf"+\left(\frac{{{N/2:g}-{F:g}}}"
            rf"{{{fm:g}}}\right){h:g}"
            rf"={format_num(median)}"
        )
        st.success(f"Median = {format_num(median)}")

    elif measure == "Mode":
        idx = int(np.argmax(f))

        if idx == 0 or idx == len(f) - 1:
            st.warning(
                "The modal class is at an end of the distribution. "
                "The grouped mode formula can be unreliable here."
            )

        L = lower[idx]
        h = width[idx]
        fm = f[idx]
        f1 = f[idx - 1] if idx > 0 else 0
        f2 = f[idx + 1] if idx < len(f) - 1 else 0

        denominator = 2 * fm - f1 - f2

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int)
        })

        st.markdown("### Formula")
        st.latex(
            r"\text{Mode}=L+\frac{f_m-f_1}"
            r"{2f_m-f_1-f_2}\,h"
        )

        st.dataframe(table, use_container_width=True)
        st.write(f"Modal class = {classes[idx]}")
        st.write(f"L = {L:g}, fm = {fm:g}, f1 = {f1:g}, f2 = {f2:g}, h = {h:g}")

        if denominator == 0:
            st.warning(
                "The denominator is zero, so the grouped mode "
                "formula cannot be applied."
            )
            return

        mode = L + ((fm - f1) / denominator) * h
        st.success(f"Estimated Mode = {format_num(mode)}")

    elif measure == "Geometric Mean":
        if np.any(midpoint <= 0):
            st.error(
                "Geometric Mean requires positive class midpoints."
            )
            return

        logs = np.log(midpoint)
        flog = f * logs
        sum_flog = flog.sum()
        gm = np.exp(sum_flog / N)

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Midpoint (x)": midpoint,
            "ln(x)": logs,
            "f × ln(x)": flog
        })

        st.markdown("### Formula")
        st.latex(
            r"GM=\operatorname{antilog}"
            r"\left(\frac{\sum f\log x}{N}\right)"
        )

        st.dataframe(table, use_container_width=True)
        st.write(f"Sum of f ln(x) = {format_num(sum_flog)}")
        st.success(f"Geometric Mean = {format_num(gm)}")

    elif measure == "Harmonic Mean":
        if np.any(midpoint <= 0):
            st.error(
                "Harmonic Mean requires positive class midpoints."
            )
            return

        f_reciprocal = f / midpoint
        sum_f_reciprocal = f_reciprocal.sum()
        hm = N / sum_f_reciprocal

        table = pd.DataFrame({
            "Class Interval": classes,
            "f": f.astype(int),
            "Midpoint (x)": midpoint,
            "1/x": 1 / midpoint,
            "f/x": f_reciprocal
        })

        st.markdown("### Formula")
        st.latex(r"HM=\frac{N}{\sum(f/x)}")

        st.dataframe(table, use_container_width=True)
        st.write(f"Sum of f/x = {format_num(sum_f_reciprocal)}")
        st.success(f"Harmonic Mean = {format_num(hm)}")


# --------------------------------------------------
# INPUT AREA
# --------------------------------------------------

st.markdown("---")
st.header("Enter or Edit Sample Data")

try:

    if data_type == "Individual Series":

        sample = "10, 12, 15, 18, 20, 25"

        raw = st.text_area(
            "Enter observations separated by commas",
            value=sample,
            height=100
        )

        values = parse_numbers(raw)

        st.caption(f"Number of observations: {len(values)}")

        if st.button("Calculate", type="primary"):
            calculate_individual(values, measure)

    elif data_type == "Discrete Frequency Distribution":

        sample = pd.DataFrame({
            "Value (x)": [10, 20, 30, 40, 50],
            "Frequency (f)": [2, 4, 6, 5, 3]
        })

        edited = st.data_editor(
            sample,
            num_rows="dynamic",
            use_container_width=True,
            key="discrete_editor"
        )

        if st.button("Calculate", type="primary"):
            values = pd.to_numeric(
                edited["Value (x)"], errors="raise"
            ).to_numpy()

            frequencies = pd.to_numeric(
                edited["Frequency (f)"], errors="raise"
            ).to_numpy()

            calculate_frequency(values, frequencies, measure)

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
            use_container_width=True,
            key="continuous_editor"
        )

        if st.button("Calculate", type="primary"):
            classes = edited["Class Interval"].astype(str).tolist()

            frequencies = pd.to_numeric(
                edited["Frequency (f)"], errors="raise"
            ).to_numpy()

            calculate_continuous(classes, frequencies, measure)

except (ValueError, TypeError, ZeroDivisionError) as e:
    st.error(f"Please check the input data: {e}")

# --------------------------------------------------
# LEARNING NOTES
# --------------------------------------------------

st.markdown("---")
st.header("Quick Learning Notes")

with st.expander("1. Arithmetic Mean"):
    st.write(
        "The arithmetic mean is the sum of all observations "
        "divided by the number of observations. For frequency "
        "data, multiply each value by its frequency first."
    )

with st.expander("2. Median"):
    st.write(
        "The median is the middle value after arranging the data "
        "in ascending order. For a continuous grouped distribution, "
        "use the median-class formula."
    )

with st.expander("3. Mode"):
    st.write(
        "The mode is the most frequently occurring value. For "
        "continuous grouped data, estimate it using the modal "
        "class and the grouped mode formula."
    )

with st.expander("4. Geometric Mean"):
    st.write(
        "The geometric mean is useful for growth rates, ratios and "
        "compound changes. All values must be positive in this app."
    )

with st.expander("5. Harmonic Mean"):
    st.write(
        "The harmonic mean is useful for averaging rates when the "
        "same distance or quantity is involved, such as average "
        "speed over equal distances. All values must be positive."
    )

st.caption(
    "Business Statistics Learning Lab | Part 1: Central Tendency"
)
