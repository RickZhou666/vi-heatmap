import streamlit as st
from datetime import date

def display_sidebar_tab2():
    st.sidebar.header("🔍 Filter Conditions")

    metric_tab = st.sidebar.radio("Metric Tab", [
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time Per View (Sec)"
    ], key="metric_tab")

    current_date = date.today()
    start_date = current_date.replace(year=current_date.year - 1)
    default_start = current_date.replace(day=1) if current_date.month == 1 else current_date.replace(month=current_date.month - 1)
    session_date_range = st.sidebar.slider(
        "Session Start Dt",
        value=(default_start, current_date),
        min_value=start_date,
        max_value=current_date
    )
    auction_type = st.sidebar.multiselect("Auction Type", ["Auction", "Fixed Price", "Best Offer"])
    bsns_vrtcl_name = st.sidebar.multiselect("Bsns Vrtcl Name", ["Electronics", "Fashion", "Collectibles"])
    buyer_segment = st.sidebar.multiselect("Buyer Fm Segment", ["Lifestage", "Gender", "Income"])
    enthusiasts_yn = st.sidebar.multiselect("Enthusiasts YN", ["Y", "N"])
    new_buyer_yn = st.sidebar.multiselect("New Buyer YN", ["Y", "N"])
    price_bucket = st.sidebar.multiselect("Price Bucket", ["$0-10", "$10-50", "$50+"])
    site = st.sidebar.multiselect("Site", ["US", "UK", "DE", "AU"])
    traffic_source = st.sidebar.multiselect("Traffic Source Level1", ["SEO", "SEM", "Email", "Push", "Direct"])
    engmnt_lv1_desc = st.sidebar.multiselect("Engagement Level 1", ["Click", "Hover", "Scroll", "Expand"])
    expertise_desc = st.sidebar.multiselect("Expertise Desc", ["Beginner", "Intermediate", "Advanced"])
    b2c_c2c = st.sidebar.multiselect("B2C/C2C", ["B2C", "C2C"])
    avip_cvip = st.sidebar.multiselect("AVIP/CVIP", ["AVIP", "CVIP"])
    msku_ind = st.sidebar.multiselect("MSKU Indicator", ["Y", "N"])
    fcsd_vrtcl_name = st.sidebar.multiselect("FCSD Vrtcl Name", ["Parts", "Accessories", "Tools"])
    itm_condition = st.sidebar.multiselect("Item Condition", ["New", "Used", "Refurbished"])
    viewport_width = st.sidebar.multiselect("Viewport Width", ["<=768px", "769-1024px", ">1024px"])
    source_page_name = st.sidebar.multiselect("Source Page Name", ["Homepage", "Search", "View Item", "Cart"])

    return (
        ["dWeb"], auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range, metric_tab,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    )