import streamlit as st
from sidebar.tab2_filters import display_sidebar_tab2
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query

def render_module_dashboard():
    data = {
        "SME Coupon": "18.6%",
        "Picture Overall": "99.7%",
        "Thumbnails Click": "99.7%",
        "Urgency Signal": "50.2%",
        "Image Enlarge Arrow Click": "99.7%",
        "Watch Icon on Image": "99.7%",
        "Main Image Click": "99.7%",
        "Main Image Scroll Arrow Click": "99.7%",
        "Image Thumbnails Arrow Click": "99.7%",
        "Seller Card ATF Overall": "99.7%",
        "Seller Logo": "99.7%",
        "Seller Name": "99.7%",
        "Seller Feedback": "99.7%",
        "Seller SOI": "99.7%",
        "Contact Seller": "99.7%",
        "Price Details": "11.2%",
        "Vibrancy Coupon": "4.1%",
        "Volume Pricing": "8.5%",
        "Buy It Now": "87.8%",
        "Place bid": "14.1%",
        "Add to cart": "87.8%"
    }

    # === SME Coupon Bar ===
    st.markdown(
        f"""
        <div style='background-color:#9ad3d4; padding:10px; font-size:18px;'>
            <b>SME Coupon:</b> {data['SME Coupon']}
        </div>
        """,
        unsafe_allow_html=True
    )

    # === Main Grid ===
    left_col, right_col = st.columns([4, 2])

    with left_col:
        st.markdown(
            f"""<div style='background-color:#1f3b73; color:white; padding:10px; font-size:16px;'>
            <b>Picture Overall:</b> {data['Picture Overall']}
            </div>""",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style='display:grid; grid-template-columns: 1fr 3fr; gap:2px;'>
            <div style='background-color:#17456f; color:white; writing-mode: vertical-rl; text-align:center; padding:10px;'>
                Thumbnails Click:<br>""" + data['Thumbnails Click'] + """</div>
            <div style='display:grid; grid-template-columns: repeat(2, 1fr); gap:4px;'>
                <div style='background-color:#50a4c8; padding:6px; font-size:14px;'>Urgency Signal: """ + data['Urgency Signal'] + """</div>
                <div style='background-color:#1f3b73; color:white; padding:6px;'>Image Enlarge Arrow Click:<br>""" + data['Image Enlarge Arrow Click'] + """</div>
                <div style='background-color:#1f3b73; color:white; padding:6px;'>Watch Icon on Image:<br>""" + data['Watch Icon on Image'] + """</div>
                <div style='grid-column: span 2; background-color:#1f3b73; color:white; text-align:center; padding:10px; font-size:16px;'>Main Image Click: """ + data['Main Image Click'] + """</div>
                <div style='grid-column: span 2; background-color:#1f3b73; color:white; padding:6px;'>Main Image Scroll Arrow Click:<br>""" + data['Main Image Scroll Arrow Click'] + """</div>
                <div style='grid-column: span 2; background-color:#1f3b73; color:white; padding:6px;'>Image Thumbnails Arrow Click:<br>""" + data['Image Thumbnails Arrow Click'] + """</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown(f"<div style='background-color:#1f3b73; color:white; padding:10px; font-size:16px;'><b>Seller Card ATF Overall:</b> {data['Seller Card ATF Overall']}</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:4px; margin-top:5px;'>
            <div style='background-color:#1f3b73; color:white; padding:6px;'>Seller Logo:<br>""" + data['Seller Logo'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:6px;'>Seller Name:<br>""" + data['Seller Name'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:6px;'>Seller Feedback:<br>""" + data['Seller Feedback'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:6px;'>Seller SOI:<br>""" + data['Seller SOI'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:6px;'>Contact Seller:<br>""" + data['Contact Seller'] + """</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:6px;'>
            <div style='background-color:#a0d6cc; padding:10px;'><b>Price Details :</b> """ + data['Price Details'] + """</div>
            <div style='background-color:#a0d6cc; padding:10px;'><b>Vibrancy Coupon :</b> """ + data['Vibrancy Coupon'] + """</div>
            <div style='background-color:#a0d6cc; padding:10px;'><b>Volume Pricing :</b> """ + data['Volume Pricing'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:10px;'><b>Buy It Now:</b> """ + data['Buy It Now'] + """</div>
            <div style='background-color:#a0d6cc; padding:10px;'><b>Place bid :</b> """ + data['Place bid'] + """</div>
            <div style='background-color:#1f3b73; color:white; padding:10px;'><b>Add to cart :</b> """ + data['Add to cart'] + """</div>
        </div>
        """, unsafe_allow_html=True)

def dweb_heatmap_tab():
    with st.sidebar:
        (
            auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site,
            traffic_source, session_date_range, metric_tab,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
            msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        ) = display_sidebar_tab2()

    # Collect all sidebar inputs first
    submit = st.sidebar.button("Submit", type="primary")
    sql = None
    if submit:
        # Just pass a dummy list to generate_mysql_query in place of platforms
        sql = generate_mysql_query(
            [], auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
            msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        )

    st.code(sql, language="sql")
    df_raw = load_data()
    # df_raw = load_data_hive()
    df_flat = reshape_data(df_raw)
    df_summary = calculate_percentage(df_flat)

    st.title("Module Engagement Treemap")
    render_module_dashboard()