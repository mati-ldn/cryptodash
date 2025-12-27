import streamlit as st
import pandas as pd
import sys
from streamlit import runtime
from streamlit.web import cli as stcli
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
        st.set_page_config(page_title='Crypto Dashboard', layout='centered')
        self.header()
        self._layout()
        self.footer()

    def header(self):
        cols = st.columns([3, 1])

        with cols[0]:
            st.title(':classical_building: Crypto Dashboard')
            st.write('Data from coingecko')

        with cols[1]:
            if st.button("Refresh"):
                # automatic re run on click
                pass
            timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            st.write(f'{timestamp} UTC')

    def footer(self):
        cols = st.columns(6)
        with cols[-1]:
            st.write('MB :fr:')

    def _layout(self):
        vw = CryptoViewer()

        tabs = st.tabs(['Main', 'Data'])

        with tabs[0]:
            cols = st.columns(2)
            with cols[0]:
                fig = vw.bar()
                st.plotly_chart(fig, use_container_width=True)

            with cols[1]:
                fig = vw.pie()
                st.plotly_chart(fig, use_container_width=True)
            df = vw.summary()
            df = format_numeric_dataframe(
                df, column_formats={'market_cap': '{:,.0f}'}
            )
            st.dataframe(df)

        with tabs[1]:
            df = vw.data
            df = format_numeric_dataframe(df)
            st.dataframe(df)


if __name__ == '__main__':
    CryptoDashboard().run()
