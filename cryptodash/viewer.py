import pandas as pd
import plotly.express as px
from typing import Optional, Dict

from cryptodash.crypto import CryptoMarket


class CryptoViewer:

    def __init__(self):
        self.data = CryptoMarket().get_top_coins()

    def pie(self):
        df = self.data
        fig = px.pie(
            df,
            names='symbol',
            values="market_cap",
            hover_data=["symbol", "current_price"],
            title="Market Cap Distribution",
        )
        return fig

    def bar(self):
        df = self.data
        fig = px.bar(
            df,
            x='symbol',
            y="24h Change (%)",
            text="24h Change (%)",
            color="24h Change (%)",
            color_continuous_scale=px.colors.diverging.RdYlGn,
            title="24h Returns (%)",
        )
        fig.update_traces(
            texttemplate='%{text:.2f}%', textposition='outside'
        )
        return fig


if __name__ == '__main__':
    df = CryptoViewer().data
    print(df)
