import streamlit as st
import pandas as pd

def show_dashboard():

    st.header("Dashboard")

    df = pd.read_csv("data.csv")
    st.dataframe(df)
    