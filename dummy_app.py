import pandas as pd
import streamlit as st
from datetime import date

# ===== Sidebar Filter UI =====
st.sidebar.header("🔍 Filter Conditions")

platforms = st.sidebar.multiselect("Platform", ["Apps: Android", "Apps: iOS", "dWeb", "mWeb", "other"], default=["Apps: Android", "Apps: iOS"])
auction_type = st.sidebar.selectbox("Auction Type", ["(All)", "Auction", "Fixed Price", "Best Offer"])
bsns_vrtcl_name = st.sidebar.selectbox("Bsns Vrtcl Name", ["(All)", "Electronics", "Fashion", "Collectibles"])
buyer_segment = st.sidebar.selectbox("Buyer Fm Segment", ["(All)", "Lifestage", "Gender", "Income"])
enthusiasts_yn = st.sidebar.selectbox("Enthusiasts YN", ["(All)", "Y", "N"])
new_buyer_yn = st.sidebar.selectbox("New Buyer YN", ["(All)", "Y", "N"])
price_bucket = st.sidebar.selectbox("Price Bucket", ["(All)", "$0-10", "$10-50", "$50+"])
site = st.sidebar.selectbox("Site", ["(All)", "US", "UK", "DE", "AU"])
traffic_source = st.sidebar.selectbox("Traffic Source Level1", ["(All)", "SEO", "SEM", "Email", "Push", "Direct"])
session_date_range = st.sidebar.slider("Session Start Dt", value=(date(2025, 4, 26), date(2025, 5, 2)))

# ===== Dummy SQL Generator =====
def generate_mysql_query(
    platforms, auction_type, bsns_vrtcl_name, buyer_segment,
    enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
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

# Show generated SQL
st.code(generate_mysql_query(
    platforms, auction_type, bsns_vrtcl_name, buyer_segment,
    enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
), language="sql")


# ===== Sample Data (Replace with actual query results if needed) =====
data = [
    ["BuyBox", "Add To Cart", "50.00%", "266.67%", "16.67%"],
    ["BuyBox", "Buy It Now", "62.50%", "200.00%", "40.00%"],
    ["Picture", "Main Image Click", "66.67%", "183.33%", "50.00%"],
    ["Picture", "Main Image Swipe", "57.14%", "225.00%", "25.00%"],
    ["Shipping", "Payment", "40.00%", "350.00%", "25.00%"],
    ["Shipping", "Shipping", "50.00%", "300.00%", "25.00%"],
]
columns = ["Bucket", "Sub Modules", "Surface Rate", "Surface to View Rate", "Surface to Engagement Rate"]
df = pd.DataFrame(data, columns=columns)

# Remove duplicate buckets for grouping display
df["Bucket"] = df["Bucket"].mask(df["Bucket"].duplicated(), "")

# ===== HTML Table Display =====
html = """
<style>
.custom-table {
    border-collapse: collapse;
    width: 100%;
    font-family: sans-serif;
}
.custom-table th, .custom-table td {
    padding: 8px 12px;
    text-align: left;
}
.custom-table td {
    border: none;
}
.custom-table th {
    border-bottom: 1px solid #ddd;
}
</style>
<table class="custom-table">
  <thead>
    <tr>
""" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr></thead><tbody>"

for _, row in df.iterrows():
    html += "<tr>" + "".join([f"<td>{val}</td>" for val in row]) + "</tr>"
html += "</tbody></table>"

# ===== Display Table =====
st.title("VI Modules Surface / View / Engagement")
st.markdown(html, unsafe_allow_html=True)
