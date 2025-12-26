import streamlit as st
import sys
from streamlit import runtime
from streamlit.web import cli as stcli
from datetime import datetime

from cryptodash.crypto import get_btc_price_usd


def main():
    st.set_page_config(page_title="Crypto Mock App", layout="centered")

    st.title("🚀 Streamlit Crypto App")
    st.write("Mock app to test deployment from GitHub")
    try:
        price = get_btc_price_usd()
        st.metric("Bitcoin Price (USD)", f"${price:,}")
        st.caption(f"Updated: {datetime.utcnow()} UTC")
    except Exception as e:
        st.error("Failed to fetch Bitcoin price")
        st.text(str(e))


if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ['streamlit', 'run', 'home.py']
        sys.exit(stcli.main())
