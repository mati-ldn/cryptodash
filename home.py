import streamlit as st
import sys
from streamlit import runtime
from streamlit.web import cli as stcli
from datetime import datetime

from cryptodash.crypto import CryptoMarket
from cryptodash.utils.logging_config import get_logger
from cryptodash.utils.formatter import format_numeric_dataframe


logger = get_logger(__name__)


class CryptoDashboard:

    def run(self):
        logger.info('Starting CryptoDashboard')
        if runtime.exists():
            self.layout()
        else:
            sys.argv = ['streamlit', 'run', 'home.py']
            sys.exit(stcli.main())

    def layout(self):
        st.set_page_config(page_title='Crypto Mock App', layout='centered')

        st.title(':classical_building: Crypto Dashboard')
        st.write('Mock app to test deployment from GitHub')
        df = CryptoMarket().get_top_coins()
        df = format_numeric_dataframe(df)
        st.dataframe(df)
        st.caption(f'Updated: {datetime.utcnow()} UTC')

        cols = st.columns(6)
        with cols[-1]:
            st.write('MB :fr:')


if __name__ == '__main__':
    CryptoDashboard().run()
