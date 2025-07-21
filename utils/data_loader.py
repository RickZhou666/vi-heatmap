import streamlit as st
import pandas as pd
from pyhive import hive
import time

# @st.cache_data
def load_data():
    try:
        time.sleep(1)
        df = pd.read_csv("./data.csv")
        print("✅ Can read data.csv.")
        return df
    except FileNotFoundError:
        st.error("❌ Cannot find data.csv. Please make sure it's in the same directory.")
        st.stop()


def load_data_hive():
    try:
        conn = hive.Connection(host='your_hive_host', port=10000, username='your_username', database='your_database')
        query = "SELECT * FROM your_table"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Hive query failed: {e}")
        st.stop()