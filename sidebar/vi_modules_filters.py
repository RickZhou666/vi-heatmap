
import streamlit as st
from datetime import date

from sidebar.default_filters import display_sidebar_common_filters
from sidebar.session_date_filter import display_sidebar_date_filters

def display_sidebar_vi_modules_tab():
    st.sidebar.header("🔍 Filter Conditions")
    session_date_range = display_sidebar_date_filters()
    platforms = st.sidebar.multiselect("Platform", ["Apps: Android", "Apps: iOS", "dWeb", "mWeb", "other"], placeholder="(All)")
    (
        auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    ) = display_sidebar_common_filters()

    return (
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    )
