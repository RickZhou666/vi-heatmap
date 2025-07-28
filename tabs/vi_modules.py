import streamlit as st
import streamlit.components.v1 as components
from sidebar.vi_modules_filters import display_sidebar_vi_modules_tab
from utils.data_loader import load_data
from utils.data_transform import df_to_clean_html_with_sort, reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query

def run_query_and_update_state(filters: dict, processing_msg):
    sql = generate_mysql_query(**filters)
    st.session_state.sql = sql
    st.code(sql, language="sql")
    with st.spinner(processing_msg):
        df_raw = load_data()
        # df_raw = load_hive_data()
    df_flat = reshape_data(df_raw)
    df_summary = calculate_percentage(df_flat)
    df_render = format_display_table(df_summary)
    st.session_state.df_render = df_render
    st.session_state.data_loaded = True

def get_common_filters():
    (
        platforms, auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    ) = display_sidebar_vi_modules_tab()

    filters = {
        "platforms": platforms,
        "auction_type": auction_type,
        "bsns_vrtcl_name": bsns_vrtcl_name,
        "buyer_fm_segment": buyer_fm_segment,
        "enthusiasts_yn": enthusiasts_yn,
        "new_buyer_yn": new_buyer_yn,
        "price_bucket": price_bucket,
        "site": site,
        "traffic_source": traffic_source,
        "session_date_range": session_date_range,
        "engmnt_lv1_desc": engmnt_lv1_desc,
        "expertise_desc": expertise_desc,
        "b2c_c2c": b2c_c2c,
        "avip_cvip": avip_cvip,
        "msku_ind": msku_ind,
        "fcsd_vrtcl_name": fcsd_vrtcl_name,
        "itm_condition": itm_condition,
        "viewport_width": viewport_width,
        "source_page_name": source_page_name,
    }

    return filters

def vi_modules_tab():
    with st.sidebar:
        filters = get_common_filters()

    # Execute logic once at the very beginning
    if st.session_state.get("vi_modules_first_run", True):
        st.session_state["data_loaded"] = False
        run_query_and_update_state(filters, "vi_modules_first_run - Data retrieving in progress...")
        st.session_state["vi_modules_first_run"] = False

    submit = st.sidebar.button("Submit", type="primary")

    if submit:
        run_query_and_update_state(filters, "after submit - Data retrieving in progress...")

    # Display data only after submit, and keep showing until next submit
    if st.session_state.data_loaded and hasattr(st.session_state, "df_render"):
        st.title("Vi Modules Surface/ View/ Engagement")
        st.set_page_config(layout="wide")
        st.markdown(df_to_clean_html_with_sort(st.session_state.df_render), unsafe_allow_html=True)
        # components.html(df_to_clean_html_with_sort(st.session_state.df_render), height=2000, scrolling=True)
