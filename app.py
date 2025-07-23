import streamlit as st
from tabs.vi_modules import vi_modules_tab
from tabs.dweb_heatmap import dweb_heatmap_tab
from tabs.vi_modules_by_cuts import vi_modules_by_cuts_tab

st.set_page_config(layout="wide")

tab = st.radio(
        "Choose a dashboard",
        ["📋 VI Modules Surface/ View/ Engagement", "📊 dWeb Heatmap", "📋 VI Modules Surface/ View/ Engagement by Cuts"],
        horizontal=True,
        label_visibility="collapsed"
    )
# dweb_heatmap_tab()
# vi_modules_by_cuts_tab()

if tab == "📋 VI Modules Surface/ View/ Engagement":
    vi_modules_tab()

elif tab == "📊 dWeb Heatmap":
    dweb_heatmap_tab()

elif tab == "📋 VI Modules Surface/ View/ Engagement by Cuts":
    vi_modules_by_cuts_tab()
