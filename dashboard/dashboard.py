import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def show_dashboard():

    # ---------------- CSS ----------------
    st.markdown("""
    <style>

    .main {
        background-color: #0b1120;
    }

    .big-title {
        font-size: 45px;
        font-weight: bold;
        color: white;
    }

    .metric-box {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.markdown(
        "<div class='big-title'>📊 VyaparAI Dashboard</div>",
        unsafe_allow_html=True
    )

    st.write("")

    # =====================================================
    # CSV UPLOAD
    # =====================================================

    st.sidebar.title("📂 Upload Business Data")

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="dashboard_upload"
    )

    # =====================================================
    # LOAD DATA
    # =====================================================

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.session_state["df"] = df

        st.success("CSV Uploaded Successfully ✅")

    elif "df" in st.session_state:

        df = st.session_state["df"]

    else:

        st.warning("Please upload a CSV file.")

        st.stop()

    # =====================================================
    # BUSINESS NAME
    # =====================================================

    if "business_name" in df.columns:

        business_name = df["business_name"].iloc[0]

    else:

        business_name = "Vyapar Business"

    st.markdown(f"""
    <h2 style='color:white;'>🏪 {business_name}</h2>
    """, unsafe_allow_html=True)

    # =====================================================
    # DATE CONVERSION
    # =====================================================

    df["date"] = pd.to_datetime(df["date"])

    # =====================================================
    # METRICS
    # =====================================================

    total_sales = df["sales"].sum()

    total_expenses = df["expenses"].sum()

    total_profit = df["profit"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>💰 Total Sales</h3>
            <h1>₹{total_sales}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>📉 Total Expenses</h3>
            <h1>₹{total_expenses}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>📈 Total Profit</h3>
            <h1>₹{total_profit}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # =====================================================
    # LINE GRAPH
    # =====================================================

    st.subheader("📈 Sales vs Expenses vs Profit")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["sales"],
        mode="lines+markers",
        name="Sales"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["expenses"],
        mode="lines+markers",
        name="Expenses"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["profit"],
        mode="lines+markers",
        name="Profit"
    ))

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Amount (₹)",
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # BAR CHART
    # =====================================================

    st.subheader("📦 Business Comparison")

    bar_fig = px.bar(
        df,
        x="date",
        y=["sales", "expenses", "profit"],
        barmode="group",
        template="plotly_dark"
    )

    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )

    # =====================================================
    # INSIGHTS
    # =====================================================

    st.subheader("🤖 Business Insights")

    best_day = df.loc[df["profit"].idxmax()]

    worst_day = df.loc[df["profit"].idxmin()]

    avg_profit = df["profit"].mean()

    st.success(
        f"Best Performing Day: {best_day['date'].date()} "
        f"with profit ₹{best_day['profit']}"
    )

    st.error(
        f"Worst Performing Day: {worst_day['date'].date()} "
        f"with profit ₹{worst_day['profit']}"
    )

    st.info(
        f"Average Profit: ₹{round(avg_profit, 2)}"
    )

    # =====================================================
    # DATA TABLE
    # =====================================================

    st.subheader("📋 Business Records")

    st.dataframe(
        df,
        use_container_width=True
    )

    # =====================================================
    # DOWNLOAD BUTTON
    # =====================================================

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Business Data",
        data=csv,
        file_name="business_data.csv",
        mime="text/csv"
    )