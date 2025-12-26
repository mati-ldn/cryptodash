import requests
import logging
import pandas as pd

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Optional: add console handler if not already configured
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class CryptoMarket:
    BASE_URL = 'https://api.coingecko.com/api/v3'
    vs_currency = 'usd'

    def get_top_coins(self, n: int = 10) -> pd.DataFrame:
        """
        Fetch top `n` coins by market capitalization.
        Returns a list of dicts with keys: id, symbol, name, current_price, market_cap
        """
        url = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": self.vs_currency,
            "order": "market_cap_desc",
            "per_page": n,
            "page": 1,
        }
        logger.info(f"Fetching top {n} coins from {url}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        logger.info(f"Successfully fetched {len(data)} coins")

        df = pd.DataFrame(
            [
                {
                    "id": coin["id"],
                    "symbol": coin["symbol"],
                    "name": coin["name"],
                    "current_price": coin["current_price"],
                    "market_cap": coin["market_cap"],
                }
                for coin in data
            ]
        )
        return df


if __name__ == '__main__':
    df = CryptoMarket().get_top_coins()
    print(df)
