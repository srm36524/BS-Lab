import streamlit as st

st.set_page_config(
    page_title="Business Statistics Learning Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("📊 Business Statistics Learning Lab")

st.subheader("Interactive Learning for B.Com and BBA Students")

st.markdown("""
Welcome to the Business Statistics Learning Lab!

Learn statistical concepts through editable sample data,
step-by-step calculations, formulas, tables and interpretations.

Select a module below to begin.
""")

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📚 Navigation")

st.sidebar.markdown("""
### Business Statistics
Choose a module from the Home Page.
""")

st.sidebar.info(
    "Each module runs as a separate Streamlit page. "
    "Your existing code files remain independent."
)

# -----------------------------
# MODULE CARDS
# -----------------------------

st.header("Learning Modules")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📌 Part 1: Central Tendency")

        st.write("""
        Learn how to calculate:
        - Arithmetic Mean
        - Median and Mode
        - Geometric Mean
        - Harmonic Mean

        Supports individual, discrete and continuous series.
        """)

        if st.button("Open Part 1", use_container_width=True):
            st.switch_page("app.py")

    with st.container(border=True):
        st.subheader("📉 Part 2: Dispersion and Shape")

        st.write("""
        Explore:
        - Range and Quartile Deviation
        - Mean Deviation
        - Variance and Standard Deviation
        - Coefficient of Variation
        - Skewness and Kurtosis
        """)

        if st.button("Open Part 2", use_container_width=True):
            st.switch_page("part2.py")

    with st.container(border=True):
        st.subheader("🔗 Part 3: Correlation and Regression")

        st.write("""
        Understand relationships between variables:
        - Karl Pearson Correlation
        - Spearman Rank Correlation
        - Simple Linear Regression
        - Multiple Linear Regression
        """)

        if st.button("Open Part 3", use_container_width=True):
            st.switch_page("part3.py")


with col2:
    with st.container(border=True):
        st.subheader("🧪 Part 4: Hypothesis Testing")

        st.write("""
        Practise:
        - One-Sample and Two-Sample Z-Tests
        - One-Sample t-Test
        - Independent Two-Sample t-Test
        - Paired t-Test
        """)

        if st.button("Open Part 4", use_container_width=True):
            st.switch_page("part4.py")

    with st.container(border=True):
        st.subheader("📊 Part 5: Tests and Distributions")

        st.write("""
        Study:
        - Chi-Square Tests
        - F-Test
        - One-Way ANOVA
        - Binomial Distribution
        - Poisson Distribution
        - Normal Distribution
        """)

        if st.button("Open Part 5", use_container_width=True):
            st.switch_page("part5.py")

    with st.container(border=True):
        st.subheader("📚 Part 6: Statistical Tables")

        st.write("""
        Look up critical values for:
        - Standard Normal Z
        - Student's t
        - Chi-Square
        - F-Distribution

        Includes probability calculations.
        """)

        if st.button("Open Part 6", use_container_width=True):
            st.switch_page("part6.py")


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.header("How to Use This Learning Lab")

st.markdown("""
1. Select the required module.
2. Edit the sample data or numerical inputs.
3. Observe the formulas and calculations.
4. Compare the results with the interpretation.
5. Experiment with different values to understand the concepts.
""")

st.success(
    "Learning tip: Change one input at a time and observe "
    "how the statistical result changes."
)

st.caption(
    "Business Statistics Learning Lab | Educational Resource for B.Com and BBA"
)
```
