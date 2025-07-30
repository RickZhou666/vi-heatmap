import streamlit as st
from sidebar.default_filters import display_sidebar_common_filters
from sidebar.weekly_session_date_filter import display_sidebar_weekly_date_slider

def display_sidebar_dweb_heatmap_tab():
    st.sidebar.header("🔍 Filter Conditions")
    retail_wk_end_date = display_sidebar_weekly_date_slider()
    
    metric_tab = st.sidebar.radio("Metric Tab", [
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time Per View (Sec)"
        ], 
        key="metric_tab"
    )

    (
        auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    ) = display_sidebar_common_filters()
    
    return (
        ["dWeb"], auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, retail_wk_end_date, metric_tab,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    )