import pytest
import requests

from cryptodash.crypto import get_btc_price_usd, COINGECKO_URL


def test_get_btc_price_success(requests_mock):
    mock_response = {"bitcoin": {"usd": 42000}}

    requests_mock.get(COINGECKO_URL, json=mock_response, status_code=200)

    price = get_btc_price_usd()

    assert price == 42000
    assert isinstance(price, (int, float))


def test_get_btc_price_http_error(requests_mock):
    requests_mock.get(COINGECKO_URL, status_code=500)

    with pytest.raises(requests.exceptions.HTTPError):
        get_btc_price_usd()


def test_get_btc_price_timeout(requests_mock):
    requests_mock.get(COINGECKO_URL, exc=requests.exceptions.Timeout)

    with pytest.raises(requests.exceptions.Timeout):
        get_btc_price_usd()


def test_get_btc_price_bad_payload(requests_mock):
    bad_response = {"foo": "bar"}

    requests_mock.get(COINGECKO_URL, json=bad_response, status_code=200)

    with pytest.raises(KeyError):
        get_btc_price_usd()
