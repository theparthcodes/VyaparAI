import streamlit as st
from dashboard.dashboard import show_dashboard
from tracker.tracker import show_tracker
from reports.reports import show_reports
from ai.ai import show_chatbot

st.set_page_config(page_title="VyaparAI", layout="wide")
st.title("🚀 VyaparAI ")

menu = st.sidebar.radio("Navigation" , ["Dashboard","Tracker","AI Chatbot","Reports"])

if menu == "Dashboard":
    show_dashboard()
elif menu == "Tracker":
    show_tracker()
elif menu == "AI Chatbot":
    show_chatbot()
elif menu == "Reports":
    show_reports()

