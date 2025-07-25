import streamlit as st
from sidebar.dweb_heatmap_filters import display_sidebar_dweb_heatmap_tab
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query
from utils.color_render import get_shaded_blue, render_colored_block, to_float
import pandas as pd

def render_module_dashboard(source_data):
    source_data["value_numeric"] = source_data.iloc[:, 1].apply(to_float)
    max_val = source_data["value_numeric"].max()
    source_data["normalized"] = source_data["value_numeric"] / max_val

    required_modules = [
        "SME Coupon", "Picture Overall", "Thumbnails Click", "Urgency Signal",
        "Image Enlarge Arrow Click", "Watch Icon on Image", "Main Image Click",
        "Main Image Scroll Arrow Click", "Image Thumbnails Arrow Click",
        "Seller Card ATF Overall", "Seller Logo", "Seller Name", "Seller Feedback",
        "Seller SOI", "Contact Seller", "Price Details", "Vibrancy Coupon",
        "Volume Pricing", "Buy It Now", "Place bid", "Add to cart", "Make offer",
        "Add to Watchlist", "Conversational Signals", "Shipping", "Returns",
        "Payment", "Shop With Confidence", "Sell Now", "Item Specifics",
        "Item Description from the Seller", "Seller Card BTF Overall", "Visit Store",
        "Save Seller", "Store Categories", "Seller Feedback BTF Overall",
        "See All Feedback"
    ]

    # filter out non-required key that might exist multiple time due to diff Bucket
    blacklist = ["Seller Logo Name Feedback"]

    source_data = source_data[~source_data["Sub Modules"].isin(blacklist)]
    # 保留只需要的列
    if "Sub Modules" not in source_data.columns:
        st.error("❌ Missing required column 'Sub Modules' in input_data")
        return
    
    # 先转换成 dict，便于查找
    input_dict = source_data.set_index("Sub Modules").to_dict("index")

    # 构造标准化 dataframe
    output_dict = {}
    data_color = {}
    for module in required_modules:
        if module in input_dict:
            values = input_dict[module]
            raw_value = values.get(source_data.columns[1], "N/A")
            normalized_val = values.get("normalized", 0.0)
            output_dict[module] = raw_value
            data_color[module] = normalized_val
        else:
            output_dict[module] = "N/A"
            data_color[module] = 0.0

    # st.write("🔍 output_dict:", output_dict)
    data = output_dict


    common_style = "border-radius:4px; margin-bottom:10px;"

    # === SME Coupon Bar ===
    st.markdown(
        f"""
        <div style='{common_style} background-color:{get_shaded_blue(data_color['SME Coupon'])}; padding:10px; font-size:18px;'>
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
            <div style='{common_style} background-color:{get_shaded_blue(data_color['Picture Overall'])}; color:white; padding:10px; padding-bottom: 50px; font-size:16px; border: 3px solid black;'>
                <b>Picture Overall:</b> {data['Picture Overall']}
                <div style='{common_style} display:grid; grid-template-columns: 1fr 7fr; gap:2px; margin-top:10px;'>
                    <div style='{common_style} display: grid; grid-template-rows: 7fr 3fr; height: 400px;'>
                        <div style='{common_style} background-color:{get_shaded_blue(data_color['Thumbnails Click'])}; color:white; writing-mode: sideways-lr; text-align:right; padding:10px; border: 3px solid white;'>
                            Thumbnails Click:<br>{data['Thumbnails Click']}
                        </div>
                        <div style='{common_style} background-color:{get_shaded_blue(data_color['Image Thumbnails Arrow Click'])}; color:white; writing-mode: sideways-lr; text-align:right; padding:6px; border: 3px solid white;'>
                            Image Thumbnails Arrow Click:<br>{data['Image Thumbnails Arrow Click']}
                        </div>
                    </div>
                    <div style='{common_style} position: relative; background-color:{get_shaded_blue(data_color['Picture Overall'])}; color:white; padding:10px; height:400px; width:100%; border:1px solid white;'>
                        <div style='{common_style} position: absolute; top: 10px; left: 10px; background-color:{get_shaded_blue(data_color['Urgency Signal'])}; padding:6px; font-size:14px; border: 3px solid white;'>
                            Urgency Signal: {data['Urgency Signal']}
                        </div>
                        <div style='{common_style} position: absolute; top: 10px; right: 155px; background-color:{get_shaded_blue(data_color['Image Enlarge Arrow Click'])}; color:white; padding:6px; width:150px; border: 3px solid white;'>
                            Image Enlarge Arrow Click:<br>{data['Image Enlarge Arrow Click']}
                        </div>
                        <div style='{common_style} position: absolute; top: 10px; right: 0px; background-color:{get_shaded_blue(data_color['Watch Icon on Image'])}; color:white; padding:6px; width:150px; border: 3px solid white;'>
                            Watch Icon on Image:<br>{data['Watch Icon on Image']}
                        </div>
                        <div style='{common_style} position: absolute; top: 40%; right: 0px; background-color:{get_shaded_blue(data_color['Main Image Scroll Arrow Click'])}; color:white; padding:6px; width:170px; border: 3px solid white;'>
                            Main Image Scroll Arrow Click:<br>{data['Main Image Scroll Arrow Click']}
                        </div>
                        <div style='{common_style} position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size:18px; font-weight:bold; text-align: center;'>
                            Main Image Click: {data['Main Image Click']}
                        </div>
                    </div>
                </div>
            </div>
            <div style='{common_style} background-color:{get_shaded_blue(data_color['Sell Now'])}; padding:10px; font-size:18px; color:white;'>
                <b>Sell Now:</b> {data['Sell Now']}
            </div>
            """, unsafe_allow_html=True
        )


    with right_col:
        header_color = get_shaded_blue(data_color['Seller Card ATF Overall'])
        st.markdown(f"""
        <div style='{common_style} background-color:{header_color}; color:white; padding:10px; font-size:16px; border: 2px solid white;'>
            <b>Seller Card ATF Overall:</b> {data['Seller Card ATF Overall']}
            <div style='{common_style} display:grid; grid-template-columns: repeat(3, 1fr); gap:4px; margin-top:10px;'>
                <div style='{common_style} background-color:{get_shaded_blue(data_color['Seller Logo'])}; color:white; padding:6px; border:1px solid white;'>Seller Logo:<br>{data['Seller Logo']}</div>
                <div style='{common_style} background-color:{get_shaded_blue(data_color['Seller Name'])}; color:white; padding:6px; border:1px solid white;'>Seller Name:<br>{data['Seller Name']}</div>
                <div style='{common_style} background-color:{get_shaded_blue(data_color['Seller Feedback'])}; color:white; padding:6px; border:1px solid white;'>Seller Feedback:<br>{data['Seller Feedback']}</div>
                <div style='{common_style} background-color:{get_shaded_blue(data_color['Seller SOI'])}; color:white; padding:6px; border:1px solid white;'>Seller SOI:<br>{data['Seller SOI']}</div>
                <div style='{common_style} background-color:{get_shaded_blue(data_color['Contact Seller'])}; color:white; padding:6px; border:1px solid white;'>Contact Seller:<br>{data['Contact Seller']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        right_col_blocks = "".join([
        render_colored_block(key, data[key], data_color[key]) for key in [
            "Price Details", "Vibrancy Coupon", "Volume Pricing", "Buy It Now", "Place bid",
            "Add to cart", "Make offer", "Add to Watchlist", "Conversational Signals",
            "Shipping", "Returns", "Payment", "Shop With Confidence"
            ]
        ])

        st.markdown(f"""
        <div style='{common_style} padding:10px 0; display:flex; flex-direction:column; gap:8px;'>
            {right_col_blocks}
        </div>
        """, unsafe_allow_html=True)

    # === Middile Grid ===
    st.markdown(
        f"""
        <div style='{common_style} background-color:{get_shaded_blue(data_color['Item Specifics'])}; color:white; padding:20px; font-size:18px; margin-bottom:10px; height: 200px'>
            <b>Item Specifics:</b> {data['Item Specifics']}
        </div>

        <div style='{common_style} background-color:{get_shaded_blue(data_color['Item Description from the Seller'])}; color:white; padding:20px; font-size:18px; margin-bottom:10px; height: 400px'>
            <b>Item Description from the Seller:</b> {data['Item Description from the Seller']}
        </div>
        """,
        unsafe_allow_html=True
    )


    # === Second Grid ===
    st.markdown(
        f"""
        <div style='{common_style} display: flex; gap: 10px;'>
            <div style='{common_style} flex: 1; background-color:{get_shaded_blue(data_color['Seller Card BTF Overall'])}; color:white; padding:10px; font-size:16px; display: flex; flex-direction: column; justify-content: space-between; height: 600px;'>
                <div>
                    <b>Seller Card BTF Overall:</b> {data['Seller Card BTF Overall']}
                    <div style='{common_style} display: flex; gap:5px; margin-top:10px;'>
                        <div style='{common_style} flex:3; background-color:{get_shaded_blue(data_color["Seller Logo"])}; border:2px solid white; padding:6px;'>Seller Logo: {data['Seller Logo']}</div>
                        <div style='{common_style} flex:7; background-color:{get_shaded_blue(data_color["Seller Name"])}; border:2px solid white; padding:6px;'>Seller Name: {data['Seller Name']}</div>
                    </div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["Visit Store"])}; border:2px solid white; padding:6px;'>Visit Store: {data['Visit Store']}</div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["Seller SOI"])}; border:2px solid white; padding:6px;'>Seller SOI: {data['Seller SOI']}</div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["Contact Seller"])}; border:2px solid white; padding:6px;'>Contact Seller: {data['Contact Seller']}</div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["Save Seller"])}; border:2px solid white; padding:6px;'>Save Seller: {data['Save Seller']}</div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["Store Categories"])}; border:2px solid white; padding:6px;'>Store Categories: {data['Store Categories']}</div>
                </div>
                <div style='{common_style} height:30px;'></div>
            </div>
            <div style='{common_style} flex: 1; background-color:{get_shaded_blue(data_color["Seller Feedback BTF Overall"])}; color:white; padding:10px; font-size:16px; position: relative; height: 600px;'>
                <b>Seller Feedback BTF Overall:</b> {data['Seller Feedback BTF Overall']}
                <div style='{common_style} position: absolute; bottom: 10px; left: 10px; background-color:{get_shaded_blue(data_color["See All Feedback"])}; border:2px solid white; padding:6px;'>
                    See All Feedback: {data['See All Feedback']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


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

    # 保存到 session_state
    st.session_state.df_render = df_render
    st.session_state.data_loaded = True

def get_common_filters():
    (
        platforms, auction_type, bsns_vrtcl_name, buyer_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range, metric_tab,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    ) = display_sidebar_dweb_heatmap_tab()

    filters = {
        "platforms": platforms,
        "auction_type": auction_type,
        "bsns_vrtcl_name": bsns_vrtcl_name,
        "buyer_segment": buyer_segment,
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
        "source_page_name": source_page_name
    }

    return filters, metric_tab

def dweb_heatmap_tab():
    with st.sidebar:
        filters, metric_tab = get_common_filters()

    # Only run on first entry or Submit
    if st.session_state.get("dweb_heatmap_first_run", True):
        st.session_state["data_loaded"] = False
        run_query_and_update_state(filters, "dweb_heatmap_first_run - Graph rendering in progress...")
        st.session_state["dweb_heatmap_first_run"] = False

    # 重新提交按钮
    submit = st.sidebar.button("Submit", type="primary")
    if submit:
        run_query_and_update_state(filters, "after submit - Graph rendering in progress...")

    # 如果已有数据，允许自由切换 metric_tab 展示
    if st.session_state.get("data_loaded", True):
        df_render = st.session_state.df_render

        metric_column_map = {
            "Surface Rate": "Surface Rate",
            "Surface to View Rate": "Surface to View Rate",
            "Surface to Engagement Rate": "Surface to Engagement Rate",
            "Dwell Time Per View (Sec)": "Dwell Time Per View (Sec)"
        }

        selected_metric = metric_tab
        if selected_metric in metric_column_map:
            selected_column = metric_column_map[selected_metric]
            select_data = df_render[["Sub Modules", "Bucket", selected_column]].rename(
                columns={selected_column: selected_metric}
            )
            # Contact Seller 特例保留 BTF
            mask = (select_data["Sub Modules"] == "Contact Seller")
            select_data = pd.concat([
                select_data[mask & (select_data["Bucket"] == "SellerCardBTF")],
                select_data[~mask]
            ], ignore_index=True)
            select_data = select_data.drop(columns=["Bucket"])

            st.title("Module Engagement Treemap")
            render_module_dashboard(select_data)
        else:
            st.error("Invalid Metric Tab selected.")
