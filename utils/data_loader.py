import random
import streamlit as st
import pandas as pd
from pyhive import hive
import time


@st.cache_data
def load_weekly_dates():
    try:
        time.sleep(0.5)
        df = pd.read_csv("./weekly_dates.csv")
        print("✅ Can read weekly_dates.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find weekly_dates.csv. Please make sure it's in the same directory.")
        st.stop()

@st.cache_data
def load_hive_weekly_dates():
    pass

# @st.cache_data
def load_data():
    try:
        time.sleep(1.5)
        df = pd.read_csv("./data.csv")
        print("✅ Can read data.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find data.csv. Please make sure it's in the same directory.")
        st.stop()

def load_data_by_cuts():
    filenames = ["./data_by_cuts_1.csv", "./data_by_cuts_2.csv"]
    selected_file = random.choice(filenames)

    try:
        time.sleep(1.5)
        df = pd.read_csv(selected_file)
        print(f"✅ Can read {selected_file}.")
        return df
    except FileNotFoundError:
        st.error(f"❌ Cannot find {selected_file} Please make sure it's in the same directory.")
        st.stop()


def load_hive_data():
    try:
        conn = hive.Connection(host='your_hive_host', port=10000, username='your_username', database='your_database')
        query = "SELECT * FROM your_table"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Hive query failed: {e}")
        st.stop()