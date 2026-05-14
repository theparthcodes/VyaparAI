import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import warnings

warnings.filterwarnings("ignore")


def show_future():

    # ---------------------------------------------------
    # CUSTOM CSS
    # ---------------------------------------------------
    st.markdown("""
    <style>

    .main {
        background-color: #f8f9fa;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # TITLE
    # ---------------------------------------------------
    st.title("🔮 Vyapar AI - Predictive Sales Forecasting")

    st.markdown(
        "*Transform Sales Data into Intelligent Business Forecasts*"
    )

    # ---------------------------------------------------
    # SIDEBAR
    # ---------------------------------------------------
    st.sidebar.title("⚙️ Prediction Settings")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Prediction CSV",
        type=["csv"],
        key="prediction_upload"
    )

    forecast_days = st.sidebar.slider(
        "Forecast Period (Days)",
        7,
        180,
        30
    )

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state["prediction_df"] = df

        st.success("Prediction CSV Uploaded Successfully ✅")

    elif "prediction_df" in st.session_state:

        df = st.session_state["prediction_df"]

    elif "df" in st.session_state:

        df = st.session_state["df"]

        st.info("Using Dashboard Uploaded CSV")

    else:

        st.warning(
            "Please upload CSV in Dashboard or Prediction section."
        )

        st.stop()

    # ---------------------------------------------------
    # DATE CONVERSION
    # ---------------------------------------------------
    df["date"] = pd.to_datetime(df["date"])

    # ---------------------------------------------------
    # SORT DATA
    # ---------------------------------------------------
    df = df.sort_values("date")

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "📈 Forecast",
        "📊 Trend Analysis",
        "🤖 Business Insights"
    ])

    # ===================================================
    # TAB 1 - FORECAST
    # ===================================================
    with tab1:

        st.subheader("📈 Future Sales Forecast")

        # X AND Y
        X = np.arange(len(df)).reshape(-1, 1)

        y = df["sales"].values

        # MODEL
        poly = PolynomialFeatures(degree=2)

        X_poly = poly.fit_transform(X)

        model = LinearRegression()

        model.fit(X_poly, y)

        # FUTURE PREDICTION
        future_x = np.arange(
            len(df),
            len(df) + forecast_days
        ).reshape(-1, 1)

        future_poly = poly.transform(future_x)

        forecast = model.predict(future_poly)

        forecast = np.maximum(forecast, 0)

        # FUTURE DATES
        future_dates = pd.date_range(
            start=df["date"].max() + timedelta(days=1),
            periods=forecast_days,
            freq="D"
        )

        # FORECAST DATAFRAME
        forecast_df = pd.DataFrame({
            "date": future_dates,
            "forecast": forecast
        })

        # GRAPH
        fig = go.Figure()

        # HISTORICAL SALES
        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["sales"],
            mode="lines+markers",
            name="Historical Sales",
            line=dict(
                color="#667eea",
                width=3
            )
        ))

        # PREDICTION
        fig.add_trace(go.Scatter(
            x=forecast_df["date"],
            y=forecast_df["forecast"],
            mode="lines+markers",
            name="Predicted Sales",
            line=dict(
                color="#ff4b4b",
                width=3,
                dash="dash"
            )
        ))

        fig.update_layout(
            title="Future Sales Forecast",
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Sales Amount (₹)",
            template="plotly_dark",
            height=550
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ---------------------------------------------------
        # METRICS
        # ---------------------------------------------------

        col1, col2, col3 = st.columns(3)

        avg_sales = int(df["sales"].mean())

        growth = (
            (forecast[-1] - avg_sales)
            / avg_sales
        ) * 100

        peak_sales = int(max(forecast))

        with col1:
            st.metric(
                "Average Sales",
                f"₹{avg_sales}"
            )

        with col2:
            st.metric(
                "Predicted Growth",
                f"{growth:.1f}%"
            )

        with col3:
            st.metric(
                "Peak Forecast",
                f"₹{peak_sales}"
            )

    # ===================================================
    # TAB 2 - TREND ANALYSIS
    # ===================================================
    with tab2:

        st.subheader("📊 Trend Analysis")

        trend_type = st.selectbox(
            "Select Trend",
            [
                "Sales Volume",
                "Growth Rate",
                "Volatility"
            ]
        )

        trend_fig = go.Figure()

        if trend_type == "Sales Volume":

            y_vals = df["sales"]

        elif trend_type == "Growth Rate":

            y_vals = (
                df["sales"]
                .pct_change()
                .fillna(0)
            ) * 100

        else:

            y_vals = (
                df["sales"]
                .rolling(3)
                .std()
                .fillna(0)
            )

        trend_fig.add_trace(go.Scatter(
            x=df["date"],
            y=y_vals,
            mode="lines+markers",
            name=trend_type
        ))

        trend_fig.update_layout(
            title=trend_type,
            template="plotly_dark",
            hovermode="x unified",
            height=500
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

    # ===================================================
    # TAB 3 - BUSINESS INSIGHTS
    # ===================================================
    with tab3:

        st.subheader("🤖 Business Insights")

        best_day = df.loc[
            df["sales"].idxmax()
        ]

        worst_day = df.loc[
            df["sales"].idxmin()
        ]

        st.success(
            f"Highest Sales Day: {best_day['date'].date()} "
            f"with sales ₹{best_day['sales']}"
        )

        st.error(
            f"Lowest Sales Day: {worst_day['date'].date()} "
            f"with sales ₹{worst_day['sales']}"
        )

        if growth > 0:

            st.info(
                "Business trend indicates future growth."
            )

        else:

            st.warning(
                "Business growth trend is slowing down."
            )

        # ---------------------------------------------------
        # DATA TABLE
        # ---------------------------------------------------

        st.subheader("📋 Business Data")

        st.dataframe(
            df,
            use_container_width=True
        )

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------

    st.markdown("---")

    st.markdown(
        "**Vyapar AI** | AI-Based Sales Forecasting System | Capstone Project"
    )