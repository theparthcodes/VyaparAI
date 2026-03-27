import streamlit as st
import pandas as pd
from datetime import date

def show_dashboard():

    st.header("📊 Dashboard")

    df = pd.read_csv("data.csv")

    st.write(df)