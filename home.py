import streamlit as st
import sys
from streamlit import runtime
from streamlit.web import cli as stcli
from datetime import datetime

from cryptodash.crypto import CryptoMarket


class CryptoDashboard:

    def run(self):
        if runtime.exists():
            self.layout()
        else:
            sys.argv = ['streamlit', 'run', 'home.py']
            sys.exit(stcli.main())

    def layout(self):
        st.set_page_config(page_title="Crypto Mock App", layout="centered")

        st.title(":classical_building: Crypto Dashboard")
        st.write("Mock app to test deployment from GitHub")
        try:
            df = CryptoMarket().get_top_coins()
            st.dataframe(df)
            st.caption(f"Updated: {datetime.utcnow()} UTC")
        except Exception as e:
            st.error("Failed to fetch")
            st.text(str(e))

        cols = st.columns(6)
        with cols[-1]:
            st.write('MB :fr:')


if __name__ == '__main__':
    CryptoDashboard().run()
