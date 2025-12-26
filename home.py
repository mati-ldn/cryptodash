import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Crypto Mock App", layout="centered")

st.title("🚀 Streamlit Crypto Mock App")

st.markdown("This is a mock app to test deployment.")

# Simple BTC price fetch (US-safe)
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin",
    "vs_currencies": "usd"
}

try:
    response = requests.get(url, params=params, timeout=10)
    price = response.json()["bitcoin"]["usd"]
    st.metric("Bitcoin Price (USD)", f"${price:,}")
    st.caption(f"Last updated: {datetime.utcnow()} UTC")
except Exception as e:
    st.error("Failed to fetch price")
    st.text(e)
