import requests
import pandas as pd

from cryptodash.utils.logging_config import get_logger
from cryptodash.loaders.redis_base import RedisDataFrameLoader

logger = get_logger(__name__)


class CryptoMarket(RedisDataFrameLoader):
    BASE_URL = 'https://api.coingecko.com/api/v3'
    vs_currency = 'usd'

    def _load(self, n: int = 10) -> pd.DataFrame:
        return self.get_top_coins(n)

    def get_top_coins(self, n: int = 10) -> pd.DataFrame:
        '''
        Fetch top `n` coins by market capitalization.
        Returns a list of dicts with keys: id, symbol, name, current_price, market_cap
        '''
        url = f'{self.BASE_URL}/coins/markets'
        params = {
            'vs_currency': self.vs_currency,
            'order': 'market_cap_desc',
            'per_page': n,
            'page': 1,
        }
        logger.info(f'Fetching top {n} coins from {url}')
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        logger.info(f'Successfully fetched {len(data)} coins')

        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        df = pd.DataFrame(data)
        df['timestamp'] = timestamp
        return df


if __name__ == '__main__':
    df = CryptoMarket().get_top_coins()
    print(df)
    df2 = CryptoMarket().load()
    print(df)
