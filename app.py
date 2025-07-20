import streamlit as st
import pandas as pd
import re
from datetime import date
import random
from pyhive import hive

# def assemble_sql():
#     # Step 1. Get filter values from sidebar
#     (
#         platforms, auction_type, bsns_vrtcl_name, buyer_segment,
#         enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
#     ) = display_sidebar()

#     # Step 2. Generate SQL
#     sql = generate_mysql_query(
#         platforms, auction_type, bsns_vrtcl_name, buyer_segment,
#         enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
#     )

#     # Step 3. Show SQL in sidebar and main area
#     st.code(sql, language="sql")
#     st.write("Generated SQL Query:")
#     st.write(sql)

def display_sidebar_tab1():
    st.sidebar.header("🔍 Filter Conditions")

    session_date_range = st.sidebar.slider("Session Start Dt", value=(date(2025, 4, 26), date(2025, 5, 2)))
    platforms = st.sidebar.multiselect("Platform", ["Apps: Android", "Apps: iOS", "dWeb", "mWeb", "other"], default=["Apps: Android", "Apps: iOS"])
    auction_type = st.sidebar.selectbox("Auction Type", ["(All)", "Auction", "Fixed Price", "Best Offer"])
    bsns_vrtcl_name = st.sidebar.selectbox("Bsns Vrtcl Name", ["(All)", "Electronics", "Fashion", "Collectibles"])
    buyer_segment = st.sidebar.selectbox("Buyer Fm Segment", ["(All)", "Lifestage", "Gender", "Income"])
    enthusiasts_yn = st.sidebar.selectbox("Enthusiasts YN", ["(All)", "Y", "N"])
    new_buyer_yn = st.sidebar.selectbox("New Buyer YN", ["(All)", "Y", "N"])
    price_bucket = st.sidebar.selectbox("Price Bucket", ["(All)", "$0-10", "$10-50", "$50+"])
    site = st.sidebar.selectbox("Site", ["(All)", "US", "UK", "DE", "AU"])
    traffic_source = st.sidebar.selectbox("Traffic Source Level1", ["(All)", "SEO", "SEM", "Email", "Push", "Direct"])
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
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    )

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

# ===== Dummy SQL Generator =====
def generate_mysql_query(
    platforms, auction_type, bsns_vrtcl_name, buyer_segment,
    enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
    engmnt_lv1_desc=None, expertise_desc=None, b2c_c2c=None, avip_cvip=None, msku_ind=None, fcsd_vrtcl_name=None, itm_condition=None,
    viewport_width=None, source_page_name=None
):
    filters = []

    def build_condition(field, value):
        if value == "(All)" or not value:
            return None
        return f"{field} = '{value}'"

    filters.append(build_condition("auction_type", auction_type))
    filters.append(build_condition("business_vertical", bsns_vrtcl_name))
    filters.append(build_condition("buyer_segment", buyer_segment))
    filters.append(build_condition("enthusiasts_flag", enthusiasts_yn))
    filters.append(build_condition("new_buyer_flag", new_buyer_yn))
    filters.append(build_condition("price_bucket", price_bucket))
    filters.append(build_condition("site", site))
    filters.append(build_condition("traffic_source", traffic_source))

    # Add new variables to filter logic
    filters.append(build_condition("engagement_lv1_desc", engmnt_lv1_desc))
    filters.append(build_condition("expertise_desc", expertise_desc))
    filters.append(build_condition("b2c_c2c", b2c_c2c))
    filters.append(build_condition("avip_cvip", avip_cvip))
    filters.append(build_condition("msku_indicator", msku_ind))
    filters.append(build_condition("fcsd_vertical_name", fcsd_vrtcl_name))
    filters.append(build_condition("item_condition", itm_condition))
    filters.append(build_condition("viewport_width", viewport_width))
    filters.append(build_condition("source_page_name", source_page_name))

    if platforms:
        platform_condition = "platform IN (" + ",".join(f"'{p}'" for p in platforms) + ")"
        filters.append(platform_condition)

    start, end = session_date_range
    filters.append(f"session_start_date BETWEEN '{start}' AND '{end}'")

    where_clause = " AND ".join([f for f in filters if f])
    query = f"""
        SELECT *
        FROM vi_module_metrics
        WHERE {where_clause}
    """
    return query.strip()

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./data.csv")
        print("✅ Can read data.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find data.csv. Please make sure it's in the same directory.")
        st.stop()


def load_data_hive():
    try:
        conn = hive.Connection(host='your_hive_host', port=10000, username='your_username', database='your_database')
        query = "SELECT * FROM your_table"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Hive query failed: {e}")
        st.stop()

def reshape_data(df_raw):
    rows = []
    for col in df_raw.columns:
        try:
            prefix, module1, module2 = col.split("_")
            value = df_raw[col].iloc[0]
            rows.append({
                "module1": module1,
                "module2": module2,
                prefix: value
            })
        except Exception as e:
            st.warning(f"Skip column: {col} ({e})")
    df_flat = pd.DataFrame(rows)
    # st.write("🔍 Flattened Data:", df_flat)
    return df_flat

def calculate_percentage(df_flat):
    df_combined = df_flat.groupby(["module1", "module2"]).agg({
        "pv": "first",
        "serve": "first",
        "view": "first",
        "engage": "first",
        "dwelltime": "first"
    }).reset_index()
    # st.write("🔍 pivoted Data:", df_combined)

    df_combined["Surface Rate"] = df_combined["serve"] / df_combined["pv"]
    df_combined["Surface to View Rate"] = df_combined["view"] / df_combined["serve"]
    df_combined["Surface to Engagement Rate"] = df_combined["engage"] / df_combined["serve"]
    df_combined["Dwell Time"] = df_combined["dwelltime"] / df_combined["view"]

    # Remove rows where all four metrics are null
    metrics = ["Surface Rate", "Surface to View Rate", "Surface to Engagement Rate", "Dwell Time"]
    df_combined = df_combined.dropna(subset=metrics, how="all")

    df_summary = df_combined[[
        "module1", "module2",
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time"
    ]].rename(columns={
        "Dwell Time": "Dwell Time Per View (Sec)"
    })

    return df_summary

def camel_to_words(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

def format_display_table(df_summary):
    df_display = df_summary.copy()
    df_display = df_display.rename(columns={
        "module1": "Bucket",
        "module2": "Sub Modules"
    })
    df_display["Sub Modules"] = df_display["Sub Modules"].apply(camel_to_words)
    df_display = df_display[[
        "Bucket", "Sub Modules",
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time Per View (Sec)"
    ]]
    df_display["Bucket"] = df_display["Bucket"].mask(df_display["Bucket"].duplicated(), "")

    percent_cols = [
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate"
    ]
    float_cols = ["Dwell Time Per View (Sec)"]

    df_render = df_display.copy()
    for col in percent_cols:
        df_render[col] = df_render[col].apply(lambda x: f"{x:.2%}")
    for col in float_cols:
        df_render[col] = df_render[col].apply(lambda x: f"{x:.2f}")

    df_render["Bucket"] = df_render["Bucket"].mask(df_render["Bucket"].duplicated(), "")
    return df_render

def df_to_clean_html(df):
    html = """
    <style>
    .table-container {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        margin: auto;
    }
    .custom-table {
        border-collapse: collapse;
        width: 100%;
        font-family: sans-serif;
        font-size: 15px;
        table-layout: auto;
    }
    .custom-table th, .custom-table td {
        padding: 8px 12px;
        text-align: left;
        word-break: break-word;
    }
    .custom-table td {
        border: none;
    }
    .custom-table th {
        border-bottom: 1px solid #ccc;
    }
    </style>
    <div class="table-container">
    <table class="custom-table">
    <thead><tr>
    """
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    return html

import plotly.express as px


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================

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



def main():
    # using tabs
    tab_selection = st.radio(
    "Choose a dashboard",
    ["📋 VI Modules Surface/ View/ Engagement", "📊 dWeb Heatmap"],
    horizontal=True,
    label_visibility="collapsed"
)

    if tab_selection == "📋 VI Modules Surface/ View/ Engagement":
        with st.sidebar:
            (
                platforms, auction_type, bsns_vrtcl_name, buyer_segment,
                enthusiasts_yn, new_buyer_yn, price_bucket, site,
                traffic_source, session_date_range,
                engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
                msku_ind, fcsd_vrtcl_name, itm_condition,
                viewport_width, source_page_name
            ) = display_sidebar_tab1()

        # Collect all sidebar inputs first
        submit = st.sidebar.button("Submit", type="primary")
        sql = None
        if submit:
            sql = generate_mysql_query(
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip, msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
            )

        st.code(sql, language="sql")
        df_raw = load_data()
        # df_raw = load_data_hive()
        df_flat = reshape_data(df_raw)
        df_summary = calculate_percentage(df_flat)
        df_render = format_display_table(df_summary)

        st.title("Vi Modules Surface/ View/ Engagement")
        st.set_page_config(layout="wide")
        st.markdown(df_to_clean_html(df_render), unsafe_allow_html=True)

    elif tab_selection == "📊 dWeb Heatmap":
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

if __name__ == "__main__":
    main()