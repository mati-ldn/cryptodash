import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_btc_price_usd(timeout=10):
    params = {"ids": "bitcoin", "vs_currencies": "usd"}

    response = requests.get(COINGECKO_URL, params=params, timeout=timeout)
    response.raise_for_status()

    data = response.json()
    return data["bitcoin"]["usd"]
