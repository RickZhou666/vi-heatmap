import streamlit as st
import pandas as pd
import re
from datetime import date

def assemble_sql():
    # Step 1. Get filter values from sidebar
    (
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
    ) = display_sidebar()

    # Step 2. Generate SQL
    sql = generate_mysql_query(
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
    )

    # Step 3. Show SQL in sidebar and main area
    st.code(sql, language="sql")
    st.write("Generated SQL Query:")
    st.write(sql)

def display_sidebar():
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

    return (
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range
    )

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

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./data.csv")
        print("✅ Can read data.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find data.csv. Please make sure it's in the same directory.")
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
    st.write("🔍 Flattened Data:", df_flat)
    return df_flat

def calculate_percentage(df_flat):
    df_combined = df_flat.groupby(["module1", "module2"]).agg({
        "pv": "first",
        "serve": "first",
        "view": "first",
        "engage": "first",
        "dwelltime": "first"
    }).reset_index()
    st.write("🔍 pivoted Data:", df_combined)

    df_combined["Surface Rate"] = df_combined["serve"] / df_combined["pv"]
    df_combined["Surface to View Rate"] = df_combined["view"] / df_combined["serve"]
    df_combined["Surface to Engagement Rate"] = df_combined["engage"] / df_combined["serve"]
    df_combined["Dwell Time"] = df_combined["dwelltime"]

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
    .custom-table {
        border-collapse: collapse;
        width: 100%;
        font-family: sans-serif;
        font-size: 15px;
    }
    .custom-table th, .custom-table td {
        padding: 8px 12px;
        text-align: left;
    }
    .custom-table td {
        border: none;
    }
    .custom-table th {
        border-bottom: 1px solid #ccc;
    }
    </style>
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
    html += "</tbody></table>"
    return html


def main():
    assemble_sql()  # Placeholder for Step 1
    df_raw = load_data()
    df_flat = reshape_data(df_raw)
    df_summary = calculate_percentage(df_flat)
    df_render = format_display_table(df_summary)
    st.title("Vi Modules Surface/ View/ Engagement")
    st.markdown(df_to_clean_html(df_render), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
