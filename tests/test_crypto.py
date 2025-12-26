import pytest
import pandas as pd
from cryptodash.crypto import CryptoMarket


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP error")


def test_get_top_coins_dataframe(monkeypatch):
    mock_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 82000,
            "market_cap": 1500000000,
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "current_price": 4200,
            "market_cap": 500000000,
        },
    ]

    def mock_get(*args, **kwargs):
        return MockResponse(mock_data)

    monkeypatch.setattr("requests.get", mock_get)

    cm = CryptoMarket()
    df = cm.get_top_coins(n=2)

    # Verify DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
    ]
    assert df.shape[0] == 2
    assert df.iloc[0]["id"] == "bitcoin"
    assert df.iloc[1]["symbol"] == "eth"


def test_get_top_coins_http_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse({}, status_code=500)

    monkeypatch.setattr("requests.get", mock_get)
    cm = CryptoMarket()

    with pytest.raises(Exception):
        cm.get_top_coins()


def test_get_top_coins_includes_daily_change(monkeypatch):
    mock_data = [
        {
            "name": "Bitcoin",
            "symbol": "btc",
            "current_price": 50000,
            "price_change_24h": 500,
            "price_change_percentage_24h": 1.0,
            "market_cap": 1_000_000_000,
        }
    ]

    class MockResponse:
        def json(self):
            return mock_data

        def raise_for_status(self):
            pass

    monkeypatch.setattr("requests.get", lambda *a, **k: MockResponse())

    cm = CryptoMarket()
    df = cm.get_top_coins(n=1)

    assert "24h Change (%)" in df.columns
    assert df.iloc[0]["24h Change (%)"] == 1.0
