# app.py

import streamlit as st
import pandas as pd
import re


# TODO Step 1. assemble sql 


# Step 2. Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./data.csv")
        print("✅ Can read data.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find data.csv. Please make sure it's in the same directory.")
        st.stop()
df_raw = load_data()


# Step 3: Reshape into module structure
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


# Step 4: Calculate percentage
# Group by module1 + module2 
df_combined = df_flat.groupby(["module1", "module2"]).agg({
    "pv": "first",
    "serve": "first",
    "view": "first",
    "engage": "first",
    "dwelltime": "first"
}).reset_index()
st.write("🔍 pivoted Data:", df_combined)


# Fill NaN with 0 just in case
# Avoid divide by zero
# Calculate percentage
# Reset index for display
# Keep only necessary columns
# Surface Rate = serve / pv
# Surface to View Rate = view / serve
# Surface to Engagment Rate = engage / serve
# dwelltime

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

# Step 4.5: Module Overview Table - Bucket + Sub Modules
def camel_to_words(text):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

# 复制 summary 数据
df_display = df_summary.copy()

# 格式化列名
df_display = df_display.rename(columns={
    "module1": "Bucket",
    "module2": "Sub Modules"
})
df_display["Sub Modules"] = df_display["Sub Modules"].apply(camel_to_words)

# 格式化列顺序
df_display = df_display[[
    "Bucket", "Sub Modules",
    "Surface Rate",
    "Surface to View Rate",
    "Surface to Engagement Rate",
    "Dwell Time Per View (Sec)"
]]

# 格式化百分比显示
percent_cols = [
    "Surface Rate",
    "Surface to View Rate",
    "Surface to Engagement Rate"
]
float_cols = ["Dwell Time Per View (Sec)"]

# 自动格式化样式
style_format = {col: "{:.2%}" for col in percent_cols}
style_format.update({col: "{:.2f}" for col in float_cols})

styled_df = df_display.reset_index(drop=True).style.format(style_format)

# Display
st.title("📋 Full Module Metrics Table")
st.dataframe(styled_df, use_container_width=True)
