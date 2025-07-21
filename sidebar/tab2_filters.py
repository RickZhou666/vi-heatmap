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

    session_date_range = st.sidebar.slider("Session Start Dt", value=(date(2025, 4, 26), date(2025, 5, 2)), key="session_date_range_2")
    auction_type = st.sidebar.selectbox("Auction Type", ["(All)", "Auction", "Fixed Price", "Best Offer"], key="auction_type_2")
    bsns_vrtcl_name = st.sidebar.selectbox("Bsns Vrtcl Name", ["(All)", "Electronics", "Fashion", "Collectibles"], key="bsns_vrtcl_name_2")
    buyer_segment = st.sidebar.selectbox("Buyer Fm Segment", ["(All)", "Lifestage", "Gender", "Income"], key="buyer_segment_2")
    enthusiasts_yn = st.sidebar.selectbox("Enthusiasts YN", ["(All)", "Y", "N"], key="enthusiasts_yn_2")
    new_buyer_yn = st.sidebar.selectbox("New Buyer YN", ["(All)", "Y", "N"], key="new_buyer_yn_2")
    price_bucket = st.sidebar.selectbox("Price Bucket", ["(All)", "$0-10", "$10-50", "$50+"], key="price_bucket_2")
    site = st.sidebar.selectbox("Site", ["(All)", "US", "UK", "DE", "AU"], key="site_2")
    traffic_source = st.sidebar.selectbox("Traffic Source Level1", ["(All)", "SEO", "SEM", "Email", "Push", "Direct"], key="traffic_source_2")
    engmnt_lv1_desc = st.sidebar.selectbox("Engagement Level 1", ["(All)", "Click", "Hover", "Scroll", "Expand"])
    expertise_desc = st.sidebar.selectbox("Expertise Desc", ["(All)", "Beginner", "Intermediate", "Advanced"])
    b2c_c2c = st.sidebar.selectbox("B2C/C2C", ["(All)", "B2C", "C2C"])
    avip_cvip = st.sidebar.selectbox("AVIP/CVIP", ["(All)", "AVIP", "CVIP"])
    msku_ind = st.sidebar.selectbox("MSKU Indicator", ["(All)", "Y", "N"])
    fcsd_vrtcl_name = st.sidebar.selectbox("FCSD Vrtcl Name", ["(All)", "Parts", "Accessories", "Tools"])
    itm_condition = st.sidebar.selectbox("Item Condition", ["(All)", "New", "Used", "Refurbished"])
    viewport_width = st.sidebar.selectbox("Viewport Width", ["(All)", "<=768px", "769-1024px", ">1024px"])
    source_page_name = st.sidebar.selectbox("Source Page Name", ["(All)", "Homepage", "Search", "View Item", "Cart"])

    return (
        auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range, metric_tab,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    )