import streamlit as st
import pandas as pd


def show_tracker():

    st.title("📊 Vyapar Daily Tracker")

    # =====================================================
    # CHECK IF DATA EXISTS
    # =====================================================

    if "df" not in st.session_state:

        st.warning(
            "Please upload CSV in Dashboard first."
        )

        st.stop()

    # =====================================================
    # LOAD DATAFRAME
    # =====================================================

    df = st.session_state["df"]
    df.to_csv("data.csv", index=False)

    # =====================================================
    # BUSINESS NAME
    # =====================================================

    if "business_name" in df.columns:

        business_name = df["business_name"].iloc[0]

    else:

        business_name = "Vyapar Business"

    st.success(
        f"🏪 Connected Business: {business_name}"
    )

    # =====================================================
    # INPUT SECTION
    # =====================================================

    st.header("📝 Daily Business Entry")

    entry_date = st.date_input("Date")

    sales = st.number_input(
        "Today's Sales (₹)",
        min_value=0.0,
        step=100.0
    )

    expenses = st.number_input(
        "Today's Expenses (₹)",
        min_value=0.0,
        step=50.0
    )

    # =====================================================
    # SAVE ENTRY
    # =====================================================

    if st.button("Save Entry"):

        profit = sales - expenses

        # -------------------------------------------------
        # CREATE NEW ROW
        # -------------------------------------------------

        new_row = pd.DataFrame({

            "business_name": [business_name],

            "date": [str(entry_date)],

            "sales": [sales],

            "expenses": [expenses],

            "profit": [profit]

        })

        # -------------------------------------------------
        # APPEND TO EXISTING DATA
        # -------------------------------------------------

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        # -------------------------------------------------
        # UPDATE SESSION STATE
        # -------------------------------------------------

        st.session_state["df"] = df

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        st.success(
            "✅ Entry Saved Successfully!"
        )

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Sales",
            f"₹{sales:.2f}"
        )

        col2.metric(
            "Expenses",
            f"₹{expenses:.2f}"
        )

        col3.metric(
            "Profit",
            f"₹{profit:.2f}"
        )

        st.rerun()

    # =====================================================
    # SHOW DATA
    # =====================================================

    st.subheader("📋 Updated Business Records")

    # SAFE DISPLAY COPY
    display_df = df.copy()

    display_df["date"] = (
        display_df["date"]
        .astype(str)
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # =====================================================
    # DOWNLOAD UPDATED CSV
    # =====================================================

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download Updated CSV",
        data=csv,
        file_name="updated_business_data.csv",
        mime="text/csv"
    )