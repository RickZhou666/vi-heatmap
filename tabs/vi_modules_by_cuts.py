import streamlit as st
from sidebar.vi_modules_by_cuts_filters import display_sidebar_vi_modules_by_cuts_tab
from utils.data_loader import load_data_by_cuts
from utils.data_transform import reshape_data_by_cuts, calculate_percentage_by_cuts, format_display_table_by_cuts, df_to_clean_html_by_cuts
from utils.query_generator import generate_mysql_query
import pandas as pd

def run_query_and_update_state(filters: dict, processing_msg):
    sql = generate_mysql_query(**filters)
    st.session_state.sql = sql
    st.code(sql, language="sql")

    with st.spinner(processing_msg):
        df_raw = load_data_by_cuts()
        # df_raw = load_hive_data()

    df_flat = reshape_data_by_cuts(df_raw)
    df_summary = calculate_percentage_by_cuts(df_flat)
    df_render_by_cuts = format_display_table_by_cuts(df_summary, False)

    st.session_state.df_render_by_cuts = df_render_by_cuts
    st.session_state.data_loaded = True


def get_common_filters():
    (
        platforms, auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name, metric_tab, cut_by
    ) = display_sidebar_vi_modules_by_cuts_tab()

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
        "cut_by": cut_by
    }

    return filters, metric_tab

def vi_modules_by_cuts_tab():
    with st.sidebar:
        filters, metric_tab = get_common_filters()

    if st.session_state.get("vi_modules_by_cuts_first_run", True):
        st.session_state["data_loaded"] = False
        run_query_and_update_state(filters, "vi_modules_by_cuts_first_run - Data retrieving in progress...")
        st.session_state["vi_modules_by_cuts_first_run"] = False

    if st.sidebar.button("Submit", type="primary"):
        run_query_and_update_state(filters, "after submit - Data retrieving in progress...")


    # 如果已有数据，允许自由切换 metric_tab 展示
    if st.session_state.get("data_loaded", True):
        df_render_by_cuts = st.session_state.df_render_by_cuts

        metric_column_map = {
            "Surface Rate": "Surface Rate",
            "Surface to View Rate": "Surface to View Rate",
            "Surface to Engagement Rate": "Surface to Engagement Rate",
            "Dwell Time Per View (Sec)": "Dwell Time Per View (Sec)"
        }

        selected_metric = metric_tab
        if selected_metric in metric_column_map:
            selected_column = metric_column_map[selected_metric]
            group_col = df_render_by_cuts.columns[0]

            # Pivot 表格
            pivot_df = df_render_by_cuts.pivot_table(
                index=["Bucket", "Sub Modules"],
                columns=group_col,
                values=selected_column,
                aggfunc="first"  # 假设每个 Bucket-SubModule-group_col 唯一
            ).reset_index()

            # 保证列顺序：Bucket, Sub Module, 其它 group_col
            columns = ["Bucket", "Sub Modules"] + [col for col in pivot_df.columns if col not in ["Bucket", "Sub Modules"]]
            pivot_df = pivot_df[columns]

            st.title("📊 Vi Modules Surface/ View/ Engagement by Cuts")
            st.markdown(df_to_clean_html_by_cuts(pivot_df), unsafe_allow_html=True)

        else:
            st.error("Invalid Metric Tab selected.")
