import streamlit as st
from sidebar.tab1_filters import display_sidebar_tab1
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query

def vi_modules_tab():
    with st.sidebar:
        (
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site,
            traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
            msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        ) = display_sidebar_tab1()

    def run_query_and_update_state():
        sql = generate_mysql_query(
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip, msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        )
        st.session_state.sql = sql
        st.code(sql, language="sql")
        with st.spinner("Data retrieving in progress..."):
            df_raw = load_data()
        df_flat = reshape_data(df_raw)
        df_summary = calculate_percentage(df_flat)
        df_render = format_display_table(df_summary)
        st.session_state.df_render = df_render
        st.session_state.data_loaded = True

    # Execute logic once at the very beginning
    if "first_run" not in st.session_state:
        st.session_state.first_run = True
        st.session_state.data_loaded = False
        run_query_and_update_state()
        st.session_state.first_run = False

    submit = st.sidebar.button("Submit", type="primary")

    if submit:
        run_query_and_update_state()

    # Display data only after submit, and keep showing until next submit
    if st.session_state.data_loaded and hasattr(st.session_state, "df_render"):
        st.title("Vi Modules Surface/ View/ Engagement")
        st.set_page_config(layout="wide")
        st.markdown(df_to_clean_html(st.session_state.df_render), unsafe_allow_html=True)
