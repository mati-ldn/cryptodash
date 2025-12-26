import streamlit as st
import sys
from streamlit import runtime
from streamlit.web import cli as stcli
from datetime import datetime
import plotly.express as px

from cryptodash.viewer import CryptoViewer
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
        st.write('Data from coingecko')

        vw = CryptoViewer()

        cols = st.columns(2)
        with cols[0]:
            fig = vw.bar()
            st.plotly_chart(fig, use_container_width=True)

        with cols[1]:
            fig = vw.pie()
            st.plotly_chart(fig, use_container_width=True)

        df = vw.data
        df = format_numeric_dataframe(df)
        st.dataframe(df)
        st.caption(f'Updated: {datetime.utcnow()} UTC')

        cols = st.columns(6)
        with cols[-1]:
            st.write('MB :fr:')


if __name__ == '__main__':
    CryptoDashboard().run()
