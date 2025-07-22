import streamlit as st
from tabs.vi_modules import vi_modules_tab
from tabs.dweb_heatmap import dweb_heatmap_tab

st.set_page_config(layout="wide")

tab = st.radio(
        "Choose a dashboard",
        ["📋 VI Modules Surface/ View/ Engagement", "📊 dWeb Heatmap"],
        horizontal=True,
        label_visibility="collapsed"
    )

# dweb_heatmap_tab()

if tab == "📋 VI Modules Surface/ View/ Engagement":
    vi_modules_tab()

elif tab == "📊 dWeb Heatmap":
    dweb_heatmap_tab()