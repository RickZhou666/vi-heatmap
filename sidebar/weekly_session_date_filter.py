import streamlit as st

from utils.data_loader import load_hive_weekly_dates, load_weekly_dates

def display_sidebar_weekly_date_slider():
    df = load_weekly_dates()
    # df = load_hive_weekly_dates()

    date_list = df["RETAIL_WK_END_DATE"].dropna().astype(str).tolist()
    date_list = sorted(date_list)

    if len(date_list) >= 2:
        default_start, default_end = date_list[-2], date_list[-1]
    else:
        default_start = default_end = date_list[-1]

    retail_wk_end_date = st.sidebar.select_slider(
        "Retail week end date range",
        options=date_list,
        value=(default_start, default_end)
    )

    # st.code(f"Selected Range: {retail_wk_end_date}, Type: {type(retail_wk_end_date)}")
    return retail_wk_end_date