import streamlit as st
from sidebar.mweb_heatmap_filters import display_sidebar_mweb_heatmap_tab
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query
from utils.color_render import get_shaded_blue, render_colored_block, to_float
import pandas as pd

def render_module_dashboard(source_data):
    # normalize color rendering value
    source_data["value_numeric"] = source_data.iloc[:, 1].apply(to_float)
    max_val = source_data["value_numeric"].max()
    source_data["normalized"] = source_data["value_numeric"] / max_val
    # st.write("after convert", source_data)

    required_modules = [
        "Picture Overall","Urgency Signal","Main Image Click","Watch Icon on Image","Main Image Swipe",
        "Thumbnails Click","Thumbnails Scroll","Product Star Rating",
        "SellerCardATF: Seller Card ATF Overall","SellerCardATF: Seller Logo Name Feedback","SellerCardATF: Contact Seller",
        "Price Details","Vibrancy Coupon","Volume Pricing","Buy It Now","Place bid","Add to cart","Make offer",
        "Add to Watchlist","Conversational Signals","SME Coupon","Item Specifics","Item Description from the Seller",
        "Sell Now","Shipping Returns Payment","Shop With Confidence",
        "SellerCardBTF: Seller Card BTF Overall","SellerCardBTF: Seller Logo Name Feedback", "SellerCardBTF: Save Seller","SellerCardBTF: Seller SOI", "SellerCardBTF: Contact Seller",
        "SellerFeedbackBTF: Seller Feedback BTF Overall","SellerFeedbackBTF: This Item",
        "SellerFeedbackBTF: All Items","SellerFeedbackBTF: See All Feedback"
    ]

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
    # st.write("data", data)
    # st.write("data_color", data_color)

    # st.write("data_color['Picture Overall']", data_color['Picture Overall'])
    # st.write("data_color['Price Details']", data_color['Price Details'])
    # st.write("data_color['Add to Watchlist']", data_color['Add to Watchlist'])

    common_style = "border-radius:4px; margin-bottom:10px;"

    # === Main Grid ===
    st.markdown(
        f"""
        <div style='{common_style} background-color:{get_shaded_blue(data_color['Picture Overall'])}; color:white; padding:10px; font-size:16px; border-radius:4px; margin-bottom:10px;'>
            <b>Picture Overall:</b> {data['Picture Overall']}
        </div>
        <div style='{common_style} display: grid; grid-template-columns: 5fr 1fr; gap: 6px; height: 400px;'>
            <div style='{common_style} position: relative; background-color:{get_shaded_blue(data_color['Picture Overall'])}; color:white; padding:10px; height:400px; width:100%; border:1px solid white;'>
                <div style='{common_style} position: absolute; top: 10px; left: 10px; background-color:{get_shaded_blue(data_color['Urgency Signal'])}; padding:6px; font-size:14px; border: 3px solid white;'>
                    Urgency Signal: {data['Urgency Signal']}
                </div>
                <div style='{common_style} position: absolute; bottom: 10px; right: 0px; background-color:{get_shaded_blue(data_color['Watch Icon on Image'])}; color:white; padding:6px; width:150px; border: 3px solid white;'>
                    Watch Icon on Image:<br>{data['Watch Icon on Image']}
                </div>
                <div style='{common_style} color:white; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size:18px; font-weight:bold; text-align: center;'>
                    Main Image Click: {data['Main Image Click']}
                </div>
            </div>
            <!-- Right: Main Image Swipe -->
            <div style='{common_style} background-color:{get_shaded_blue(data_color['Main Image Swipe'])}; color:white; display:flex; align-items:center; justify-content:center; text-align:center; padding:10px; font-weight:bold; border:1px solid white;'>
                Main Image Swipe: {data['Main Image Swipe']}
            </div>
        </div>
        <div style='{common_style} display: flex; gap: 6px; margin-top: 10px;'>
            <div style='{common_style} flex: 4; background-color:{get_shaded_blue(data_color["Thumbnails Click"])}; color:white; padding:10px; border: 3px solid white; display: flex; align-items: center; justify-content: center; font-weight: bold;'>
                Thumbnails Click: {data["Thumbnails Click"]}
            </div>
        </div>
        <div style='{common_style} background-color:{get_shaded_blue(data_color['Product Star Rating'])}; color:white; display:flex; align-items:center; justify-content:center; text-align:center; padding:10px; font-weight:bold; border:1px solid white;'>
            Product Star Rating: {data['Product Star Rating']}
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(f"""
    <div style='{common_style} background-color:{get_shaded_blue(data_color['SellerCardATF: Seller Card ATF Overall'])}; color:white; padding:10px; font-size:16px; border: 2px solid white;'>
        <b>Seller Card ATF Overall:</b> {data['SellerCardATF: Seller Card ATF Overall']}
        <div style='{common_style} display:grid; grid-template-columns: repeat(3, 1fr); gap:4px; margin-top:10px;'>
            <div style='{common_style} background-color:{get_shaded_blue(data_color['SellerCardATF: Seller Logo Name Feedback'])}; color:white; padding:6px; border:1px solid white;'>Seller Logo Name Feedback:<br>{data['SellerCardATF: Seller Logo Name Feedback']}</div>
            <div style='{common_style} background-color:{get_shaded_blue(data_color['SellerCardATF: Contact Seller'])}; color:white; padding:6px; border:1px solid white;'>Contact Seller<br>{data['SellerCardATF: Contact Seller']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    right_col_blocks = "".join([
    render_colored_block(key, data[key], data_color[key]) for key in [
        "Price Details", "Vibrancy Coupon", "Volume Pricing", "Buy It Now", "Place bid",
        "Add to cart", "Make offer", "Add to Watchlist", "Conversational Signals", "SME Coupon",
        "Item Specifics", "Item Description from the Seller",
        "Sell Now", "Shipping Returns Payment", "Shop With Confidence"
        ]
    ])

    st.markdown(f"""
    <div style='{common_style} color:white; padding:10px 0; display:flex; flex-direction:column; gap:8px;'>
        {right_col_blocks}
    </div>
    """, unsafe_allow_html=True)

    # === Second Grid ===
    st.markdown(
        f"""
        <div style='{common_style} flex: 1; background-color:{get_shaded_blue(data_color['SellerCardBTF: Seller Card BTF Overall'])}; color:white; padding:10px; font-size:16px; display: flex; flex-direction: column; justify-content: space-between; height: 400px; border-radius:4px; margin-bottom:10px'>
            <div>
                <b>Seller Card BTF Overall:</b> {data['SellerCardBTF: Seller Card BTF Overall']}
                <div style='margin-top:10px; margin-left: 70px; display: flex; flex-direction: column; gap:10px; width: 60%;'>
                    <div style='{common_style} display: flex; gap:5px; margin-top:10px;'>
                        <div style='{common_style} flex:3; background-color:{get_shaded_blue(data_color["SellerCardBTF: Seller Logo Name Feedback"])}; color:white; border:2px solid white; padding:6px;'>Seller Logo Name Feedback: {data['SellerCardBTF: Seller Logo Name Feedback']}</div>
                        <div style='{common_style} flex:7; background-color:{get_shaded_blue(data_color["SellerCardBTF: Save Seller"])}; color:white; border:2px solid white; padding:6px;'>Save Seller: {data['SellerCardBTF: Save Seller']}</div>
                    </div>
                    <div style='{common_style} margin-top:5px; background-color:{get_shaded_blue(data_color["SellerCardBTF: Seller SOI"])}; color:white; border:2px solid white; padding:6px;'>Seller SOI: {data['SellerCardBTF: Seller SOI']}</div>
                    <div style='{common_style} background-color:{get_shaded_blue(data_color["SellerCardBTF: Contact Seller"])}; color:white; border:2px solid white; padding:6px;'>Contact Seller: {data['SellerCardBTF: Contact Seller']}</div>
                </div>
            </div>
            <div style='{common_style} height:30px;'></div>
        </div>
        <div style='{common_style} flex: 1; background-color:{get_shaded_blue(data_color["SellerFeedbackBTF: Seller Feedback BTF Overall"])}; color:white; padding:10px; font-size:16px; position: relative; height: 400px; padding:10px; border-radius:4px'>
            <b>Seller Feedback BTF Overall:</b> {data['SellerFeedbackBTF: Seller Feedback BTF Overall']}
            <div style='margin-top:10px; display: flex; flex-direction: column; gap:10px; width: 60%;'>
                <div style='{common_style} display: flex; gap:10px; margin-top:10px;'>
                    <div style='{common_style} flex:1; background-color:{get_shaded_blue(data_color["SellerFeedbackBTF: This Item"])}; color:white; border:2px solid white; padding:6px;'>This Item: {data['SellerFeedbackBTF: This Item']}</div>
                    <div style='{common_style} flex:1; background-color:{get_shaded_blue(data_color["SellerFeedbackBTF: All Items"])}; color:white; border:2px solid white; padding:6px;'>All Items: {data['SellerFeedbackBTF: All Items']}</div>
                </div>
                <div style='margin-top:150px; background-color:{get_shaded_blue(data_color["SellerFeedbackBTF: See All Feedback"])}; color:white; border:2px solid white; padding:8px; border-radius:4px; display: inline-block;'>
                    <b>See All Feedback:</b> {data["SellerFeedbackBTF: See All Feedback"]}
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
    df_render = format_display_table(df_summary, False)

    # 保存到 session_state
    st.session_state.df_render = df_render
    st.session_state.data_loaded = True

def get_common_filters():
    (
        platforms, auction_type, bsns_vrtcl_name, buyer_fm_segment,
        enthusiasts_yn, new_buyer_yn, price_bucket, site,
        traffic_source, session_date_range, metric_tab,
        engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
        msku_ind, fcsd_vrtcl_name, itm_condition,
        viewport_width, source_page_name
    ) = display_sidebar_mweb_heatmap_tab()

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
        "source_page_name": source_page_name
    }

    return filters, metric_tab


def mweb_heatmap_tab():
    with st.sidebar:
        filters, metric_tab = get_common_filters()

    # Only run on first entry or Submit
    if st.session_state.get("mweb_heatmap_first_run", True):
        st.session_state["data_loaded"] = False
        run_query_and_update_state(filters, "mweb_heatmap_first_run - Graph rendering in progress...")
        st.session_state["mweb_heatmap_first_run"] = False

    # 重新提交按钮
    submit = st.sidebar.button("Submit", type="primary")
    if submit:
        run_query_and_update_state(filters, "mweb_heatmap after submit - Graph rendering in progress...")

    # 如果已有数据，允许自由切换 metric_tab 展示
    if st.session_state.get("data_loaded", False):
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

            # 合成唯一标识字段：如果是 SellerCardATF/BTF/FeedbackBTF 则加上 Bucket 前缀
            duplicate_bucket_prefixes = ["SellerCardATF", "SellerCardBTF", "SellerFeedbackBTF"]
            select_data["Sub Modules"] = select_data.apply(
                lambda row: f"{row['Bucket']}: {row['Sub Modules']}"
                if row["Bucket"] in duplicate_bucket_prefixes else row["Sub Modules"],
                axis=1
            )
            select_data = select_data.drop(columns=["Bucket"])
            st.title("Native/ mWeb Heatmap")
            render_module_dashboard(select_data)
        else:
            st.error("Invalid Metric Tab selected.")
