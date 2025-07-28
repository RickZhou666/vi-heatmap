import streamlit as st

def display_sidebar_common_filters():
    auction_type = st.sidebar.multiselect("Auction Type", ["Auction", "Fixed Price", "Best Offer"], placeholder="(All)")
    bsns_vrtcl_name = st.sidebar.multiselect("Bsns Vrtcl Name", ["Electronics", "Fashion", "Collectibles"], placeholder="(All)")
    buyer_fm_segment = st.sidebar.multiselect("Buyer Fm Segment", ["Lifestage", "Gender", "Income"], placeholder="(All)")
    enthusiasts_yn = st.sidebar.multiselect("Enthusiasts YN", ["Y", "N"], placeholder="(All)")
    new_buyer_yn = st.sidebar.multiselect("New Buyer YN", ["Y", "N"], placeholder="(All)")
    price_bucket = st.sidebar.multiselect("Price Bucket", ["$0-10", "$10-50", "$50+"], placeholder="(All)")
    site = st.sidebar.multiselect("Site", ["US", "UK", "DE", "AU"], placeholder="(All)")
    traffic_source = st.sidebar.multiselect("Traffic Source Level1", ["SEO", "SEM", "Email", "Push", "Direct"], placeholder="(All)")
    engmnt_lv1_desc = st.sidebar.multiselect("Engagement Level 1", ["Click", "Hover", "Scroll", "Expand"], placeholder="(All)")
    expertise_desc = st.sidebar.multiselect("Expertise Desc", ["Beginner", "Intermediate", "Advanced"], placeholder="(All)")
    b2c_c2c = st.sidebar.multiselect("B2C/C2C", ["B2C", "C2C"], placeholder="(All)")
    avip_cvip = st.sidebar.multiselect("AVIP/CVIP", ["AVIP", "CVIP"], placeholder="(All)")
    msku_ind = st.sidebar.multiselect("MSKU Indicator", ["Y", "N"], placeholder="(All)")
    fcsd_vrtcl_name = st.sidebar.multiselect("FCSD Vrtcl Name", ["Parts", "Accessories", "Tools"], placeholder="(All)")
    itm_condition = st.sidebar.multiselect("Item Condition", ["New", "Used", "Refurbished"], placeholder="(All)")
    viewport_width = st.sidebar.multiselect("Viewport Width", ["<=768px", "769-1024px", ">1024px"], placeholder="(All)")
    source_page_name = st.sidebar.multiselect("Source Page Name", ["Homepage", "Search", "View Item", "Cart"], placeholder="(All)")

    return (
        auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition, viewport_width, source_page_name
    )