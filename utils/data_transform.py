import streamlit as st
import pandas as pd
import re

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

def reshape_data_by_cuts(df_raw):
    rows = []
    group_col = df_raw.columns[0]  # 动态获取第一列的列名

    for col in df_raw.columns[1:]:  # 跳过第一列
        try:
            prefix, module1, module2 = col.split("_", 2)
            for _, row in df_raw.iterrows():
                rows.append({
                    group_col: row[group_col],  # 用动态列名提取值
                    "module1": module1,
                    "module2": module2,
                    prefix: row[col]
                })
        except Exception as e:
            st.warning(f"Skip column: {col} ({e})")

    return pd.DataFrame(rows)

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


def calculate_percentage_by_cuts(df_flat):
    group_col = df_flat.columns[0]
    df_combined = df_flat.groupby([group_col, "module1", "module2"]).agg({
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
        group_col, "module1", "module2",
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

sub_module_mapping = {
    "Addtocart": "Add to cart",
    "AddtoWatchlist": "Add to Watchlist",
    "AllItems": "All Items",
    "AllRatings": "All Ratings",
    "BuyBox": "Buy Box",
    "BuyBoxCTA": "Buy Box CTA",
    "BuyItNow": "Buy It Now",
    "ContactSeller": "Contact Seller",
    "ConversationalSignals": "Conversational Signals",
    "ImageEnlargeArrowClick": "Image Enlarge Arrow Click",
    "ImageThumbnailsArrowClick": "Image Thumbnails Arrow Click",
    "ItemDescriptionfromtheSeller": "Item Description from the Seller",
    "ItemSpecifics": "Item Specifics",
    "MainImageClick": "Main Image Click",
    "MainImageScrollArrowClick": "Main Image Scroll Arrow Click",
    "MainImageSwipe": "Main Image Swipe",
    "Makeoffer": "Make offer",
    "Payment": "Payment",
    "Picture": "Picture",
    "PictureOverall": "Picture Overall",
    "Placebid": "Place bid",
    "PriceDetails": "Price Details",
    "ProductStarRating": "Product Star Rating",
    "Promotions": "Promotions",
    "Returns": "Returns",
    "SaveSeller": "Save Seller",
    "SeeAllFeedback": "See All Feedback",
    "SellerCardATF": "Seller Card ATF",
    "SellerCardATFOverall": "Seller Card ATF Overall",
    "SellerCardBTFOverall": "Seller Card BTF Overall",
    "SellerCardShevron": "Seller Card Shevron",
    "SellerFeedback": "Seller Feedback",
    "SellerFeedbackBTFOverall": "Seller Feedback BTF Overall",
    "SellerLogo": "Seller Logo",
    "SellerLogoNameFeedback": "Seller Logo Name Feedback",
    "SellerName": "Seller Name",
    "SellerSOI": "Seller SOI",
    "SellNow": "Sell Now",
    "Shipping": "Shipping",
    "ShippingReturnsPayment": "Shipping Returns Payment",
    "ShopWithConfidence": "Shop With Confidence",
    "SMECoupon": "SME Coupon",
    "StoreCategories": "Store Categories",
    "ThisItem": "This Item",
    "ThumbnailsClick": "Thumbnails Click",
    "ThumbnailsScroll": "Thumbnails Scroll",
    "UrgencySignal": "Urgency Signal",
    "VibrancyCoupon": "Vibrancy Coupon",
    "VisitStore": "Visit Store",
    "VolumePricing": "Volume Pricing",
    "WatchIcononImage": "Watch Icon on Image"
}

def format_display_table(df_summary, remove_dup_bucket=True):
    df_display = df_summary.copy()
    df_display = df_display.rename(columns={
        "module1": "Bucket",
        "module2": "Sub Modules"
    })
    # df_display["Sub Modules"] = df_display["Sub Modules"].apply(camel_to_words)
    df_display["Sub Modules"] = df_display["Sub Modules"].map(sub_module_mapping).fillna(df_display["Sub Modules"])
    df_display = df_display[[
        "Bucket", "Sub Modules",
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time Per View (Sec)"
    ]]

    if remove_dup_bucket:
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

    if remove_dup_bucket:
        df_render["Bucket"] = df_render["Bucket"].mask(df_render["Bucket"].duplicated(), "")
    return df_render


def format_display_table_by_cuts(df_summary, remove_dup_bucket=True):
    group_col = df_summary.columns[0]
    df_display = df_summary.copy()
    df_display = df_display.rename(columns={
        "module1": "Bucket",
        "module2": "Sub Modules"
    })
    # df_display["Sub Modules"] = df_display["Sub Modules"].apply(camel_to_words)
    df_display["Sub Modules"] = df_display["Sub Modules"].map(sub_module_mapping).fillna(df_display["Sub Modules"])
    df_display = df_display[[
        group_col, "Bucket", "Sub Modules",
        "Surface Rate",
        "Surface to View Rate",
        "Surface to Engagement Rate",
        "Dwell Time Per View (Sec)"
    ]]

    if remove_dup_bucket:
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

    if remove_dup_bucket:
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
        /* font-family: "Impact", "Comic Sans MS", fantasy; */
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
    <!-- Tablesort.js CDN -->
    <script src="https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js"></script>
    <div class="table-container">
    <table class="custom-table" id="sortable-table">
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
    html += """
        </tbody>
        </table>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            new Tablesort(document.getElementById('sortable-table'));
        });
        </script>
    """
    return html

def df_to_clean_html_by_cuts(df):
    html = """
    <style>
    .table-container {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        margin: auto;
        white-space: nowrap;
    }
    .custom-table {
        border-collapse: collapse;
        width: max-content;
        font-family: sans-serif;
        font-size: 15px;
        table-layout: auto;
    }
    .custom-table th, .custom-table td {
        padding: 8px 12px;
        text-align: left;
        word-break: break-word;
        border: none;
        white-space: nowrap;
    }
    .custom-table th {
        border-bottom: 1px solid #ccc;
    }
    </style>
    <script src="https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js"></script>
    <div class="table-container">
    <table class="custom-table" id="sortable-table">
    <thead><tr>
    """
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    last_bucket = None
    for _, row in df.iterrows():
        html += "<tr>"
        bucket = row["Bucket"]
        html += f"<td>{bucket if bucket != last_bucket else ''}</td>"  # 合并重复Bucket
        for val in row[1:]:  # skip Bucket, already printed
            html += f"<td>{val}</td>"
        html += "</tr>"
        last_bucket = bucket
    html += """
        </tbody>
        </table>
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            new Tablesort(document.getElementById('sortable-table'));
        });
        </script>
    """
    return html

def df_to_clean_html_with_sort(df):
    html = """
    <style>
    .table-container {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
        margin: auto;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .custom-table {
        border-collapse: collapse;
        width: 100%;
        font-size: 16px;
        table-layout: auto;
        background-color: #121212;  /* 黑色背景 */
        color: white;               /* 白色字体 */
    }
    .custom-table th, .custom-table td {
        padding: 10px 14px;
        text-align: left;
        word-break: break-word;
        background-color: #121212;  /* 保证格子背景也是黑的 */
        color: white;               /* 确保字体是白色 */
    }
    .custom-table th {
        border-bottom: 3px solid #ff4d4d;  /* 红色下划线 */
        cursor: pointer;
        position: relative;
        font-weight: bold;
    }
    .custom-table th.sort-asc::after {
        content: " ▲";
        position: absolute;
        right: 10px;
    }
    .custom-table th.sort-desc::after {
        content: " ▼";
        position: absolute;
        right: 10px;
    }
    .custom-table tr:hover {
        background-color: #1f1f1f;
    }
    </style>
    <script src="https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js"></script>
    <div class="table-container">
    <table class="custom-table" id="sortable-table">
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
    html += """
        </tbody></table></div>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
            const table = document.getElementById('sortable-table');
            new Tablesort(table);

            table.querySelectorAll('th').forEach(th => {
                th.addEventListener('click', () => {
                    setTimeout(() => {
                        table.querySelectorAll('th').forEach(el => {
                            el.classList.remove('sort-asc', 'sort-desc');
                        });
                        const sortedTh = table.querySelector('th[aria-sort]');
                        if (sortedTh) {
                            if (sortedTh.getAttribute('aria-sort') === 'ascending') {
                                sortedTh.classList.add('sort-asc');
                            } else if (sortedTh.getAttribute('aria-sort') === 'descending') {
                                sortedTh.classList.add('sort-desc');
                            }
                        }
                    }, 0);
                });
            });
        });
        </script>
    """
    return html