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

def format_display_table(df_summary):
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
    <div class="table-container">
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
    html += "</tbody></table></div>"
    return html