import streamlit as st
from datetime import date

def display_sidebar_date_filters():
    current_date = date.today()
    start_date = current_date.replace(year=current_date.year - 1)
    default_start = current_date.replace(day=1) if current_date.month == 1 else current_date.replace(month=current_date.month - 1)
    session_date_range = st.sidebar.slider(
        "Session Start Dt",
        value=(default_start, current_date),
        min_value=start_date,
        max_value=current_date
    )
    
    return session_date_range
