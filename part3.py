import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Business Statistics Lab - Part 3",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Statistics Learning Lab")
st.header("Part 3: Correlation and Regression")

st.write(
    "Calculate correlation coefficients and regression equations "
    "with step-by-step working."
)

# ==========================================================
# SIDEBAR
# ==========================================================

method = st.sidebar.selectbox(
    "Select Statistical Method",
    [
        "Karl Pearson Correlation",
        "Spearman Rank Correlation",
        "Simple Linear Regression",
        "Multiple Linear Regression"
    ]
)

# ==========================================================
# COMMON FUNCTIONS
# ==========================================================

def fmt(value):
    return f"{value:,.4f}"


def get_data(text, name):
    try:
        values = [
            float(v.strip())
            for v in text.replace("\n", ",").split(",")
            if v.strip()
        ]
    except ValueError:
        raise ValueError(f"{name}: enter valid numbers separated by commas.")

    if len(values) < 2:
        raise ValueError(f"{name}: enter at least two observations.")

    return np.array(values, dtype=float)


def check_equal_lengths(*arrays):
    lengths = [len(a) for a in arrays]

    if len(set(lengths)) != 1:
        raise ValueError(
            "All variables must contain the same number of observations."
        )


def interpret_correlation(r):
    if abs(r) < 0.10:
        strength = "negligible linear association"
    elif abs(r) < 0.30:
        strength = "weak linear association"
    elif abs(r) < 0.50:
        strength = "moderate linear association"
    elif abs(r) < 0.70:
        strength = "substantial linear association"
    else:
        strength = "strong linear association"

    if r > 0:
        direction = "positive"
    elif r < 0:
        direction = "negative"
    else:
        direction = "zero"

    if r == 0:
        return "No linear correlation."

    return f"{strength.capitalize()}, with a {direction} direction."


# ==========================================================
# 1. KARL PEARSON CORRELATION
# ==========================================================

def pearson_correlation(x, y):
    n = len(x)

    xbar = np.mean(x)
    ybar = np.mean(y)

    dx = x - xbar
    dy = y - ybar

    dxdy = dx * dy
    dx2 = dx ** 2
    dy2 = dy ** 2

    sum_dxdy = np.sum(dxdy)
    sum_dx2 = np.sum(dx2)
    sum_dy2 = np.sum(dy2)

    denominator = np.sqrt(sum_dx2 * sum_dy2)

    if denominator == 0:
        st.error("Correlation is undefined when either variable is constant.")
        return

    r = sum_dxdy / denominator

    table = pd.DataFrame({
        "X": x,
        "Y": y,
        "X − Mean X": dx,
        "Y − Mean Y": dy,
        "(X − Mean X)(Y − Mean Y)": dxdy,
        "(X − Mean X)²": dx2,
        "(Y − Mean Y)²": dy2
    })

    st.markdown("### Formula")

    st.latex(
        r"r=\frac{\sum (X-\bar X)(Y-\bar Y)}"
        r"{\sqrt{\sum(X-\bar X)^2\sum(Y-\bar Y)^2}}"
    )

    st.markdown("### Step 1: Calculate the means")

    st.write(f"Number of pairs = {n}")
    st.write(f"Mean of X = {fmt(xbar)}")
    st.write(f"Mean of Y = {fmt(ybar)}")

    st.markdown("### Step 2: Calculate deviations and products")

    st.dataframe(table, use_container_width=True)

    st.write(f"Sum of deviation products = {fmt(sum_dxdy)}")
    st.write(f"Sum of squared X deviations = {fmt(sum_dx2)}")
    st.write(f"Sum of squared Y deviations = {fmt(sum_dy2)}")

    st.markdown("### Step 3: Calculate correlation")

    st.latex(
        rf"r=\frac{{{fmt(sum_dxdy)}}}"
        rf"{{\sqrt{{{fmt(sum_dx2)}\times{fmt(sum_dy2)}}}}}"
    )

    st.success(f"Karl Pearson correlation coefficient r = {fmt(r)}")

    st.write("**Interpretation:**", interpret_correlation(r))

    st.caption(
        "Correlation measures linear association. It does not establish "
        "that one variable causes the other."
    )


# ==========================================================
# 2. SPEARMAN RANK CORRELATION
# ==========================================================

def spearman_correlation(x, y):
    n = len(x)

    rx = pd.Series(x).rank(method="average").to_numpy()
    ry = pd.Series(y).rank(method="average").to_numpy()

    d = rx - ry
    d2 = d ** 2

    tie_x = len(np.unique(x)) < n
    tie_y = len(np.unique(y)) < n
    has_ties = tie_x or tie_y

    table = pd.DataFrame({
        "X": x,
        "Y": y,
        "Rank X": rx,
        "Rank Y": ry,
        "d = Rank X − Rank Y": d,
        "d²": d2
    })

    st.markdown("### Step 1: Rank the observations")

    st.write(
        "The smallest observation receives rank 1. Equal observations "
        "receive the average of the ranks they occupy."
    )

    st.dataframe(table, use_container_width=True)

    st.write(f"Sum of squared rank differences, Σd² = {fmt(d2.sum())}")

    st.markdown("### Step 2: Calculate Spearman correlation")

    if not has_ties:
        st.latex(
            r"r_s=1-\frac{6\sum d^2}{n(n^2-1)}"
        )

        rs = 1 - (6 * d2.sum()) / (n * (n**2 - 1))

        st.latex(
            rf"r_s=1-\frac{{6({fmt(d2.sum())})}}"
            rf"{{{n}({n}^2-1)}}"
            rf"={fmt(rs)}"
        )

        st.info(
            "No ties were found. The standard rank-difference formula "
            "is applicable."
        )

    else:
        st.warning(
            "Ties were detected. Average ranks have been assigned. "
            "For tied data, calculate Pearson correlation on the ranks "
            "rather than applying the uncorrected shortcut formula."
        )

        rxbar = rx.mean()
        rybar = ry.mean()

        numerator = np.sum((rx - rxbar) * (ry - rybar))
        denominator = np.sqrt(
            np.sum((rx - rxbar)**2) *
            np.sum((ry - rybar)**2)
        )

        if denominator == 0:
            st.error("Rank correlation is undefined.")
            return

        rs = numerator / denominator

        st.latex(
            r"r_s=\frac{\sum(R_X-\bar R_X)(R_Y-\bar R_Y)}"
            r"{\sqrt{\sum(R_X-\bar R_X)^2\sum(R_Y-\bar R_Y)^2}}"
        )

        st.write(f"Mean rank X = {fmt(rxbar)}")
        st.write(f"Mean rank Y = {fmt(rybar)}")
        st.write(f"Rank covariance numerator = {fmt(numerator)}")
        st.write(f"Rank denominator = {fmt(denominator)}")

    st.success(f"Spearman rank correlation coefficient = {fmt(rs)}")

    st.write("**Interpretation:**", interpret_correlation(rs))


# ==========================================================
# 3. SIMPLE LINEAR REGRESSION
# ==========================================================

def simple_regression(x, y):
    n = len(x)

    xbar = np.mean(x)
    ybar = np.mean(y)

    dx = x - xbar
    dy = y - ybar

    dx2 = dx ** 2
    dxdy = dx * dy

    sum_dx2 = np.sum(dx2)
    sum_dxdy = np.sum(dxdy)

    if sum_dx2 == 0:
        st.error("Regression is undefined because X is constant.")
        return

    b = sum_dxdy / sum_dx2
    a = ybar - b * xbar

    yhat = a + b * x
    residual = y - yhat
    residual2 = residual ** 2

    sse = np.sum(residual2)
    sst = np.sum((y - ybar) ** 2)

    r2 = 1 - sse / sst if sst > 0 else np.nan

    table = pd.DataFrame({
        "X": x,
        "Y": y,
        "X − Mean X": dx,
        "Y − Mean Y": dy,
        "(X − Mean X)²": dx2,
        "(X − Mean X)(Y − Mean Y)": dxdy,
        "Predicted Y": yhat,
        "Residual (Y − Predicted Y)": residual
    })

    st.markdown("### Regression formula")

    st.latex(r"\hat Y=a+bX")

    st.latex(
        r"b=\frac{\sum(X-\bar X)(Y-\bar Y)}"
        r{\sum(X-\bar X)^2}"
    )

    st.latex(r"a=\bar Y-b\bar X")

    st.markdown("### Step 1: Calculate the means")

    st.write(f"Mean X = {fmt(xbar)}")
    st.write(f"Mean Y = {fmt(ybar)}")

    st.markdown("### Step 2: Calculate the slope")

    st.write(f"Σ(X − Mean X)² = {fmt(sum_dx2)}")
    st.write(
        "Σ(X − Mean X)(Y − Mean Y) = "
        + fmt(sum_dxdy)
    )

    st.latex(
        rf"b=\frac{{{fmt(sum_dxdy)}}}{{{fmt(sum_dx2)}}}"
        rf"={fmt(b)}"
    )

    st.markdown("### Step 3: Calculate the intercept")

    st.latex(
        rf"a={fmt(ybar)}-({fmt(b)}\times{fmt(xbar)})"
        rf"={fmt(a)}"
    )

    st.markdown("### Step 4: Regression calculation table")

    st.dataframe(table, use_container_width=True)

    st.success(
        f"Regression equation: Ŷ = {fmt(a)} + ({fmt(b)})X"
    )

    st.write(f"R² = {fmt(r2)}")

    if np.isfinite(r2):
        st.write(
            f"Approximately {r2 * 100:.2f}% of the variation "
            "in Y is explained by this fitted linear model in the sample."
        )

    st.markdown("### Predict Y")

    prediction_x = st.number_input(
        "Enter an X value for prediction",
        value=float(x[-1])
    )

    prediction_y = a + b * prediction_x

    st.success(
        f"When X = {fmt(prediction_x)}, predicted Y = {fmt(prediction_y)}"
    )

    st.caption(
        "Predictions outside the observed X range are extrapolations "
        "and may be unreliable."
    )


# ==========================================================
# 4. MULTIPLE LINEAR REGRESSION
# ==========================================================

def multiple_regression(x1, x2, y):
    n = len(y)

    X = np.column_stack([
        np.ones(n),
        x1,
        x2
    ])

    if np.linalg.matrix_rank(X) < X.shape[1]:
        st.error(
            "The predictors are perfectly collinear or there are "
            "too few independent observations. The coefficients "
            "cannot be uniquely estimated."
        )
        return

    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    a, b1, b2 = beta

    yhat = X @ beta
    residual = y - yhat

    sse = np.sum(residual ** 2)
    sst = np.sum((y - np.mean(y)) ** 2)

    r2 = 1 - sse / sst if sst > 0 else np.nan

    p = X.shape[1]

    if n > p and sst > 0:
        adjusted_r2 = 1 - (
            (1 - r2) * (n - 1) / (n - p)
        )
    else:
        adjusted_r2 = np.nan

    table = pd.DataFrame({
        "X1": x1,
        "X2": x2,
        "Actual Y": y,
        "Predicted Y": yhat,
        "Residual": residual
    })

    st.markdown("### Regression model")

    st.latex(
        r"\hat Y=a+b_1X_1+b_2X_2"
    )

    st.write(
        "The coefficients are calculated using ordinary least squares. "
        "The app chooses the coefficients that minimize the sum of "
        "squared residuals."
    )

    st.markdown("### Estimated coefficients")

    coefficients = pd.DataFrame({
        "Coefficient": ["Intercept (a)", "X1 coefficient (b1)", "X2 coefficient (b2)"],
        "Estimate": [a, b1, b2]
    })

    st.dataframe(coefficients, use_container_width=True)

    st.success(
        f"Regression equation: Ŷ = {fmt(a)} "
        f"+ ({fmt(b1)})X1 + ({fmt(b2)})X2"
    )

    st.markdown("### Predicted values and residuals")

    st.dataframe(table, use_container_width=True)

    st.write(f"Sum of squared residuals = {fmt(sse)}")
    st.write(f"R² = {fmt(r2)}")

    if np.isfinite(adjusted_r2):
        st.write(f"Adjusted R² = {fmt(adjusted_r2)}")

    if np.isfinite(r2):
        st.write(
            f"R² indicates that approximately {r2 * 100:.2f}% "
            "of the sample variation in Y is explained by the fitted model."
        )

    st.markdown("### Predict Y")

    col1, col2 = st.columns(2)

    with col1:
        pred_x1 = st.number_input(
            "Enter X1",
            value=float(x1[-1]),
            key="pred_x1"
        )

    with col2:
        pred_x2 = st.number_input(
            "Enter X2",
            value=float(x2[-1]),
            key="pred_x2"
        )

    prediction = a + b1 * pred_x1 + b2 * pred_x2

    st.success(
        f"Predicted Y = {fmt(prediction)}"
    )

    st.caption(
        "A coefficient describes the estimated change in Y for a "
        "one-unit increase in that predictor, holding the other "
        "predictor constant. Association alone does not establish causation."
    )


# ==========================================================
# INPUTS
# ==========================================================

st.markdown("---")
st.subheader("Enter or Edit Sample Data")

try:

    if method in [
        "Karl Pearson Correlation",
        "Spearman Rank Correlation",
        "Simple Linear Regression"
    ]:

        if method == "Karl Pearson Correlation":
            default_x = "10, 20, 30, 40, 50"
            default_y = "15, 25, 35, 45, 60"

        elif method == "Spearman Rank Correlation":
            default_x = "10, 20, 30, 40, 50"
            default_y = "15, 25, 20, 45, 60"

        else:
            default_x = "1, 2, 3, 4, 5"
            default_y = "3, 5, 7, 8, 11"

        x_text = st.text_area(
            "Enter X values (comma-separated)",
            default_x
        )

        y_text = st.text_area(
            "Enter Y values (comma-separated)",
            default_y
        )

        if st.button("Calculate", type="primary"):
            x = get_data(x_text, "X")
            y = get_data(y_text, "Y")

            check_equal_lengths(x, y)

            if method == "Karl Pearson Correlation":
                pearson_correlation(x, y)

            elif method == "Spearman Rank Correlation":
                spearman_correlation(x, y)

            else:
                simple_regression(x, y)

    else:

        st.info(
            "For multiple regression, enter three columns: X1, X2 and Y. "
            "Use the sample dataset or edit it."
        )

        sample = pd.DataFrame({
            "X1": [1, 2, 3, 4, 5, 6],
            "X2": [2, 1, 4, 3, 5, 4],
            "Y":  [10, 12, 17, 18, 23, 24]
        })

        edited = st.data_editor(
            sample,
            num_rows="dynamic",
            use_container_width=True
        )

        if st.button("Calculate", type="primary"):
            x1 = pd.to_numeric(
                edited["X1"], errors="raise"
            ).to_numpy(dtype=float)

            x2 = pd.to_numeric(
                edited["X2"], errors="raise"
            ).to_numpy(dtype=float)

            y = pd.to_numeric(
                edited["Y"], errors="raise"
            ).to_numpy(dtype=float)

            check_equal_lengths(x1, x2, y)

            if len(y) < 4:
                st.error(
                    "Use at least four observations for this model. "
                    "More observations are generally preferable."
                )
            else:
                multiple_regression(x1, x2, y)

except (ValueError, TypeError, np.linalg.LinAlgError) as e:
    st.error(f"Please check the input data: {e}")


# ==========================================================
# LEARNING NOTES
# ==========================================================

st.markdown("---")
st.header("Quick Learning Notes")

with st.expander("1. Correlation"):
    st.write(
        "Correlation measures the direction and strength of association. "
        "Karl Pearson measures linear association using actual values. "
        "Spearman measures monotonic association using ranks."
    )

with st.expander("2. Spearman ties"):
    st.write(
        "When observations are tied, assign each tied observation the "
        "average of the ranks they occupy. Calculate Pearson correlation "
        "on the resulting rank columns. The simple formula using Σd² "
        "without tie adjustments should not be applied blindly."
    )

with st.expander("3. Regression slope"):
    st.write(
        "In simple regression, b tells us the predicted change in Y for "
        "a one-unit increase in X. The intercept a is the predicted Y "
        "when X equals zero."
    )

with st.expander("4. Multiple regression"):
    st.write(
        "Multiple regression estimates Y using two or more predictors. "
        "Each slope describes the relationship with Y while holding "
        "the other included predictors constant."
    )

with st.expander("5. R-squared"):
    st.write(
        "R² measures the proportion of sample variation in Y explained "
        "by the fitted model. Adding predictors cannot reduce ordinary "
        "R² in standard least-squares regression, so adjusted R² is "
        "also useful when comparing models with different numbers "
        "of predictors."
    )

st.caption("Business Statistics Learning Lab | Part 3")
