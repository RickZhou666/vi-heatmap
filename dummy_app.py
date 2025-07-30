import streamlit as st

dates = ["2025-07-29", "2025-07-22", "2025-07-15"]
range_selection = st.select_slider("Pick a date range", options=dates, value=(dates[1], dates[0]))
st.write(range_selection)