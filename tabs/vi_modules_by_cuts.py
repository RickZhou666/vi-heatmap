import streamlit as st
from sidebar.tab3_filters import display_sidebar_tab3
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query
import pandas as pd

def vi_modules_by_cuts_tab():
    import streamlit as st

    with st.sidebar:
        (
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site,
            traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
            msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name, metric_tab, cut_by
        ) = display_sidebar_tab3()

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

        # Cache all cut_by × metric_tab combinations
        cut_options = {
            "Auction Type": "auction_type",
            "Bsns Vrtcl Name": "bsns_vrtcl_name",
            "Enthusiasts YN": "enthusiasts_yn",
            "Buyer Fm Segment": "buyer_segment",
            "Platform": "platforms",
            "Site": "site",
            "Traffic Source Level1": "traffic_source",
            "Price Bucket": "price_bucket",
            "New Buyer YN": "new_buyer_yn"
        }

        metric_list = [
            "Surface Rate",
            "Surface to View Rate",
            "Surface to Engagement Rate",
            "Dwell Time Per View (Sec)"
        ]

        cut_col = cut_options[cut_by]
        group_values = eval(cut_col) or ["All"]

        render_dict = {}

        for cut in group_values:
            for metric in metric_list:
                temp_df = df_summary.copy()
                if cut != "All":
                    temp_df = temp_df[temp_df[cut_col] == cut] if cut_col in temp_df.columns else temp_df
                display_df = temp_df[["module1", "module2", metric]].copy()
                display_df = display_df.rename(columns={
                    "module1": "Bucket",
                    "module2": "Sub Modules",
                    metric: cut
                })
                pivot_df = display_df.pivot_table(index=["Bucket", "Sub Modules"], values=cut, aggfunc="first")
                pivot_df = pivot_df.reset_index()
                render_dict[(metric, cut)] = pivot_df

        st.session_state.df_render_by_metric_cut = render_dict
        st.session_state.data_loaded = True

    # Only run on first entry or Submit
    tab_key = "tab3_first_run"
    if tab_key not in st.session_state:
        st.session_state.first_run = True
        st.session_state.data_loaded = False
        run_query_and_update_state()
        st.session_state.first_run = False

    if st.sidebar.button("Submit", type="primary"):
        run_query_and_update_state()

    # Display cached version with dynamic tab switching
    if st.session_state.data_loaded and "df_render_by_metric_cut" in st.session_state:
        st.set_page_config(layout="wide")
        st.title("VI Modules Surface / View / Engagement by Cuts")

        key = (metric_tab, cut_by)
        match_keys = [k for k in st.session_state.df_render_by_metric_cut.keys() if k[0] == metric_tab]

        # Merge all columns under current metric
        merged_df = None
        for k in match_keys:
            df = st.session_state.df_render_by_metric_cut[k]
            df = df.rename(columns={k[1]: k[1]})  # use cut value as col
            if merged_df is None:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on=["Bucket", "Sub Modules"], how="outer")

        # Format percent
        for col in merged_df.columns:
            if col not in ["Bucket", "Sub Modules"]:
                merged_df[col] = pd.to_numeric(merged_df[col], errors="coerce")
                merged_df[col] = merged_df[col].map(lambda x: f"{x:.1%}" if pd.notnull(x) else "")

        st.markdown(df_to_clean_html(merged_df), unsafe_allow_html=True)
