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
        "Add to cart": "87.8%",
        "Make offer": "36.4%",
        "Add to Watchlist": "99.9%",
        "Conversational Signals": "84.0%",
        "Shipping": "99.5%",
        "Returns": "98.0%",
        "Payment": "99.4%",
        "Shop With Confidence": "95.1%",
        "Sell Now": "85.5%",
        "Item Specifics": "99.0%",
        "Item Description from the Seller": "99.7%",
        "Seller Card BTF Overall": "99.5%",
        "Visit Store": "99.5%",
        "Save Seller": "99.5%",
        "Store Categories": "99.5%",
        "Seller Feedback BTF Overall": "99.5%",
        "See All Feedback": "99.5%"
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
    left_col, right_col = st.columns([6, 2])

    with left_col:
        st.markdown(
            f"""
            <div style='background-color:#1f3b73; color:white; padding:10px; padding-bottom: 50px; font-size:16px; border: 3px solid black;'>
                <b>Picture Overall:</b> {data['Picture Overall']}
                <div style='display:grid; grid-template-columns: 1fr 7fr; gap:2px; margin-top:10px;'>
                    <div style='display: grid; grid-template-rows: 7fr 3fr; height: 400px;'>
                        <div style='background-color:#17456f; color:white; writing-mode: sideways-lr; text-align:right; padding:10px; border: 3px solid white;'>
                            Thumbnails Click:<br>{data['Thumbnails Click']}
                        </div>
                        <div style='background-color:#1f3b73; color:white; writing-mode: sideways-lr; text-align:right; padding:6px; border: 3px solid white;'>
                            Image Thumbnails Arrow Click:<br>{data['Image Thumbnails Arrow Click']}
                        </div>
                    </div>
                    <div style='position: relative; background-color:#1f3b73; color:white; padding:10px; height:400px; width:100%; border:1px solid white;'>
                        <div style='position: absolute; top: 10px; left: 10px; background-color:#50a4c8; padding:6px; font-size:14px; border: 3px solid white;'>
                            Urgency Signal: {data['Urgency Signal']}
                        </div>
                        <div style='position: absolute; top: 10px; right: 155px; background-color:#1f3b73; color:white; padding:6px; width:150px; border: 3px solid white;'>
                            Image Enlarge Arrow Click:<br>{data['Image Enlarge Arrow Click']}
                        </div>
                        <div style='position: absolute; top: 10px; right: 0px; background-color:#1f3b73; color:white; padding:6px; width:150px; border: 3px solid white;'>
                            Watch Icon on Image:<br>{data['Watch Icon on Image']}
                        </div>
                        <div style='position: absolute; top: 40%; right: 0px; background-color:#1f3b73; color:white; padding:6px; width:170px; border: 3px solid white;'>
                            Main Image Scroll Arrow Click:<br>{data['Main Image Scroll Arrow Click']}
                        </div>
                        <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size:18px; font-weight:bold; text-align: center;'>
                            Main Image Click: {data['Main Image Click']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )


    with right_col:
        st.markdown(f"""
        <div style='background-color:#1f3b73; color:white; padding:10px; font-size:16px; border: 2px solid white;'>
            <b>Seller Card ATF Overall:</b> {data['Seller Card ATF Overall']}
            <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:4px; margin-top:10px;'>
                <div style='background-color:#1f3b73; color:white; padding:6px; border:1px solid white;'>Seller Logo:<br>{data['Seller Logo']}</div>
                <div style='background-color:#1f3b73; color:white; padding:6px; border:1px solid white;'>Seller Name:<br>{data['Seller Name']}</div>
                <div style='background-color:#1f3b73; color:white; padding:6px; border:1px solid white;'>Seller Feedback:<br>{data['Seller Feedback']}</div>
                <div style='background-color:#1f3b73; color:white; padding:6px; border:1px solid white;'>Seller SOI:<br>{data['Seller SOI']}</div>
                <div style='background-color:#1f3b73; color:white; padding:6px; border:1px solid white;'>Contact Seller:<br>{data['Contact Seller']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color:#a0d6cc; padding:10px;'><b>Price Details :</b> """ + data['Price Details'] + """</div>
        <div style='background-color:#a0d6cc; padding:10px;'><b>Vibrancy Coupon :</b> """ + data['Vibrancy Coupon'] + """</div>
        <div style='background-color:#a0d6cc; padding:10px;'><b>Volume Pricing :</b> """ + data['Volume Pricing'] + """</div>
        <div style='background-color:#1f3b73; color:white; padding:10px;'><b>Buy It Now:</b> """ + data['Buy It Now'] + """</div>
        <div style='background-color:#a0d6cc; padding:10px;'><b>Place bid :</b> """ + data['Place bid'] + """</div>
        <div style='background-color:#1f3b73; color:white; padding:10px;'><b>Add to cart :</b> """ + data['Add to cart'] + """</div>
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