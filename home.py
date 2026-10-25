import streamlit as st

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Business Statistics Learning Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# HOME PAGE
# ==========================================================

st.title("📊 Business Statistics Learning Lab")

st.subheader(
    "Interactive Step-by-Step Statistics for B.Com & BBA Students"
)

st.markdown("""
Welcome to the **Business Statistics Learning Lab**.

This application is designed to help students understand statistics
through **sample data, formulas, step-by-step calculations,
statistical tables and plain-English interpretations**.

Choose a module below to begin.
""")

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📚 Statistics Lab")

st.sidebar.markdown("""
### Learning Modules

Use the navigation menu to move between:

- Central Tendency
- Dispersion & Shape
- Correlation & Regression
- Hypothesis Testing
- Probability Distributions
- Statistical Tables
""")

st.sidebar.divider()

st.sidebar.info(
    "💡 Learning Tip\n\n"
    "Change the sample values and observe how the "
    "statistical result changes."
)

# ==========================================================
# PART 1
# ==========================================================

st.header("1️⃣ Central Tendency")

st.markdown("""
Learn how to find the **average or central value** of a dataset.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Mean")
    st.write("""
    Arithmetic Mean for:
    - Individual series
    - Discrete frequency series
    - Continuous/grouped series
    """)

with col2:
    st.subheader("Median & Mode")
    st.write("""
    Find the middle and most frequently occurring values
    using appropriate methods for different data formats.
    """)

with col3:
    st.subheader("GM & HM")
    st.write("""
    Geometric Mean and Harmonic Mean with
    step-by-step calculations.
    """)

st.page_link(
    "pages/app.py",
    label="📌 Open Part 1 — Central Tendency",
    icon="➡️"
)

st.divider()

# ==========================================================
# PART 2
# ==========================================================

st.header("2️⃣ Dispersion, Skewness & Kurtosis")

st.markdown("""
Measure the **spread, variability and shape** of a distribution.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Dispersion")
    st.write("""
    - Range
    - Quartile Deviation
    - Mean Deviation
    - Variance
    - Standard Deviation
    """)

with col2:
    st.subheader("Relative Measures")
    st.write("""
    - Sample vs Population variance
    - Sample vs Population SD
    - Coefficient of Variation
    """)

with col3:
    st.subheader("Shape")
    st.write("""
    - Karl Pearson Skewness
    - Bowley Skewness
    - Kurtosis
    """)

st.page_link(
    "pages/part2.py",
    label="📉 Open Part 2 — Dispersion & Shape",
    icon="➡️"
)

st.divider()

# ==========================================================
# PART 3
# ==========================================================

st.header("3️⃣ Correlation & Regression")

st.markdown("""
Study the relationship between variables and predict one variable
from another.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 Correlation")

    st.write("""
    **Karl Pearson Correlation**

    **Spearman Rank Correlation**
    - Without ties
    - With ties
    - Tie correction
    """)

with col2:
    st.subheader("📈 Regression")

    st.write("""
    **Simple Linear Regression**

    **Multiple Linear Regression**

    Includes an easy-to-understand calculation approach.
    """)

st.page_link(
    "pages/part3.py",
    label="🔗 Open Part 3 — Correlation & Regression",
    icon="➡️"
)

st.divider()

# ==========================================================
# PART 4
# ==========================================================

st.header("4️⃣ Hypothesis Testing")

st.markdown("""
Learn how sample evidence is used to make decisions about
population parameters.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Z Tests")

    st.write("""
    - One-sample Z test
    - Two-sample Z test
    - Right-tailed
    - Left-tailed
    - Two-tailed
    """)

with col2:
    st.subheader("t Tests")

    st.write("""
    - One-sample t test
    - Two-sample t test
    - Paired t test
    """)

with col3:
    st.subheader("Other Tests")

    st.write("""
    - Chi-square
    - F test
    - One-way ANOVA
    """)

st.page_link(
    "pages/part4.py",
    label="🧪 Open Part 4 — Hypothesis Testing",
    icon="➡️"
)

st.divider()

# ==========================================================
# PART 5
# ==========================================================

st.header("5️⃣ Probability Distributions")

st.markdown("""
Calculate probabilities using commonly used discrete and continuous
probability distributions.
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Binomial")

    st.write("""
    Calculate probabilities for a fixed number
    of independent success/failure trials.
    """)

with col2:
    st.subheader("Poisson")

    st.write("""
    Calculate probabilities for the number
    of events occurring in a fixed interval.
    """)

with col3:
    st.subheader("Normal")

    st.write("""
    Calculate probabilities using the normal
    distribution and Z-scores.
    """)

st.page_link(
    "pages/part5.py",
    label="📊 Open Part 5 — Probability Distributions",
    icon="➡️"
)

st.divider()

# ==========================================================
# PART 6
# ==========================================================

st.header("6️⃣ Statistical Distribution Tables")

st.markdown("""
Interactive reference tables for finding critical values.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Z Table")
    st.write("""
    Standard Normal distribution
    and Z critical values.
    """)

with col2:
    st.subheader("t Table")
    st.write("""
    Student's t-distribution
    for different degrees of freedom.
    """)

with col3:
    st.subheader("χ² Table")
    st.write("""
    Chi-square critical values
    for different degrees of freedom.
    """)

with col4:
    st.subheader("F Table")
    st.write("""
    F-distribution critical values
    for numerator and denominator df.
    """)

st.page_link(
    "pages/part6.py",
    label="📚 Open Part 6 — Statistical Tables",
    icon="➡️"
)

st.divider()

# ==========================================================
# QUICK REFERENCE
# ==========================================================

st.header("🧭 Quick Reference")

st.dataframe(
    {
        "Part": [
            "Part 1",
            "Part 2",
            "Part 3",
            "Part 4",
            "Part 5",
            "Part 6"
        ],
        "Topic": [
            "Central Tendency",
            "Dispersion, Skewness & Kurtosis",
            "Correlation & Regression",
            "Hypothesis Testing",
            "Probability Distributions",
            "Statistical Tables"
        ],
        "Main Purpose": [
            "Find the central/average value",
            "Measure variability and distribution shape",
            "Measure relationships and make predictions",
            "Test statistical hypotheses",
            "Calculate probabilities",
            "Find critical values"
        ]
    },
    width="stretch",
    hide_index=True
)

# ==========================================================
# LEARNING WORKFLOW
# ==========================================================

st.header("🎓 Suggested Learning Workflow")

st.markdown("""
### Step 1 — Understand the concept
Read the explanation and formula.

### Step 2 — Study the sample
Start with the built-in sample data.

### Step 3 — Follow the calculation
Look at every intermediate step rather than only the final answer.

### Step 4 — Change the data
Replace the sample data with your own values.

### Step 5 — Interpret the result
Understand what the calculated statistic actually means.

### Step 6 — Verify using statistical tables
For hypothesis tests, compare the calculated statistic with
the appropriate critical value.
""")

st.success(
    "📌 The objective is not just to obtain an answer — "
    "it is to understand how the answer was obtained."
)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Business Statistics Learning Lab | "
    "Interactive educational resource for B.Com & BBA"
)

st.caption(
    "Mean • Median • Mode • GM • HM • Dispersion • "
    "Correlation • Regression • Hypothesis Testing • "
    "Probability • Statistical Tables"
)
