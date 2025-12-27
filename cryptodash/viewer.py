import pandas as pd
import plotly.express as px
from typing import Optional, Dict

from cryptodash.crypto import CryptoMarket


class CryptoViewer:

    def __init__(self):
        self.data = CryptoMarket().load()

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
            y="price_change_percentage_24h",
            text="price_change_percentage_24h",
            color="price_change_percentage_24h",
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
