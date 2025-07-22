import streamlit as st
from sidebar.tab2_filters import display_sidebar_tab2
from utils.data_loader import load_data
from utils.data_transform import reshape_data, calculate_percentage, format_display_table, df_to_clean_html
from utils.query_generator import generate_mysql_query
import pandas as pd

def render_module_dashboard(source_data):
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
    for module in required_modules:
        if module in input_dict:
            value = next(iter(input_dict[module].values()), "N/A")
            output_dict[module] = value
        else:
            output_dict[module] = "N/A"

    # st.write("🔍 output_dict:", output_dict)
    data = output_dict

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
            <div style='background-color:#3c7397; padding:10px; font-size:18px; color:white;'>
                <b>Sell Now:</b> {data['Sell Now']}
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
        <div style="padding:10px 0; display:flex; flex-direction:column; gap:8px;">
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Price Details :</b> """ + data['Price Details'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Vibrancy Coupon :</b> """ + data['Vibrancy Coupon'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Volume Pricing :</b> """ + data['Volume Pricing'] + """
            </div>
            <div style="background-color:#1f3b73; color:white; padding:10px; border-radius:4px;">
                <b>Buy It Now:</b> """ + data['Buy It Now'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Place bid :</b> """ + data['Place bid'] + """
            </div>
            <div style="background-color:#1f3b73; color:white; padding:10px; border-radius:4px;">
                <b>Add to cart :</b> """ + data['Add to cart'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Make offer :</b> """ + data['Make offer'] + """
            </div>
            <div style="background-color:#1f3b73; color:white; padding:10px; border-radius:4px;">
                <b>Add to Watchlist :</b> """ + data['Add to Watchlist'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Conversational Signals :</b> """ + data['Conversational Signals'] + """
            </div>
            <div style="background-color:#1f3b73; color:white; padding:10px; border-radius:4px;">
                <b>Shipping :</b> """ + data['Shipping'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Returns :</b> """ + data['Returns'] + """
            </div>
            <div style="background-color:#1f3b73; color:white; padding:10px; border-radius:4px;">
                <b>Payment :</b> """ + data['Payment'] + """
            </div>
            <div style="background-color:#a0d6cc; padding:10px; border-radius:4px;">
                <b>Shop With Confidence :</b> """ + data['Shop With Confidence'] + """
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === Middile Grid ===
    st.markdown(
        f"""
        <div style='background-color:#32688a; color:white; padding:20px; font-size:18px; margin-bottom:10px; height: 200px'>
            <b>Item Specifics:</b> 99.0%
        </div>

        <div style='background-color:#32688a; color:white; padding:20px; font-size:18px; margin-bottom:10px; height: 400px'>
            <b>Item Description from the Seller:</b> 99.7%
        </div>
        """,
        unsafe_allow_html=True
    )


    # === Second Grid ===
    st.markdown(
    f"""
    <div style='display: flex; gap: 10px;'>
        <!-- 左侧 Seller Card BTF -->
        <div style='flex: 1; background-color:#1f3b73; color:white; padding:10px; font-size:16px; display: flex; flex-direction: column; justify-content: space-between; height: 600px;'>
            <div>
                <b>Seller Card BTF Overall:</b> {data['Seller Card BTF Overall']}
                <div style='display: flex; gap:5px; margin-top:10px;'>
                    <div style='flex:3; border:2px solid white; padding:6px;'>Seller Logo: {data['Seller Logo']}</div>
                    <div style='flex:7; border:2px solid white; padding:6px;'>Seller Name: {data['Seller Name']}</div>
                </div>
                <div style='margin-top:5px; border:2px solid white; padding:6px; padding-bottom:20px; margin-top:16px'>Visit Store: {data['Visit Store']}</div>
                <div style='margin-top:5px; border:2px solid white; padding:6px; padding-bottom:20px'>Seller SOI: {data['Seller SOI']}</div>
                <div style='margin-top:5px; border:2px solid white; padding:6px; padding-bottom:20px'>Contact Seller: {data['Contact Seller']}</div>
                <div style='margin-top:5px; border:2px solid white; padding:6px; padding-bottom:20px'>Save Seller: {data['Save Seller']}</div>
                <div style='margin-top:5px; border:2px solid white; padding:6px; padding-bottom:20px'>Store Categories: {data['Store Categories']}</div>
            </div>
            <div style='height:30px;'><!-- padding at bottom --></div>
        </div>
        <!-- 右侧 Seller Feedback BTF -->
        <div style='flex: 1; background-color:#1f3b73; color:white; padding:10px; font-size:16px; position: relative; height: 600px;'>
            <b>Seller Feedback BTF Overall:</b> {data['Seller Feedback BTF Overall']}
            <div style='position: absolute; bottom: 10px; left: 10px; border:2px solid white; padding:6px; padding-bottom:20px'>
                See All Feedback: {data['See All Feedback']}
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True
)

def dweb_heatmap_tab():
    with st.sidebar:
        (
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site,
            traffic_source, session_date_range, metric_tab,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip,
            msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        ) = display_sidebar_tab2()

    def run_query_and_update_state():
        sql = generate_mysql_query(
            platforms, auction_type, bsns_vrtcl_name, buyer_segment,
            enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
            engmnt_lv1_desc, expertise_desc, b2c_c2c, avip_cvip, msku_ind, fcsd_vrtcl_name, itm_condition,
            viewport_width, source_page_name
        )
        st.session_state.sql = sql
        st.code(sql, language="sql")
        with st.spinner("Graph rendering in progress..."):
            df_raw = load_data()
            # df_raw = load_hive_data()
        df_flat = reshape_data(df_raw)
        df_summary = calculate_percentage(df_flat)
        df_render = format_display_table(df_summary)

        # 保存到 session_state
        st.session_state.df_render = df_render
        st.session_state.data_loaded = True

    # ⚠️ 初始化状态，首次访问自动触发 query
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
        run_query_and_update_state()

    # 重新提交按钮
    submit = st.sidebar.button("Submit", type="primary")
    if submit:
        run_query_and_update_state()

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
