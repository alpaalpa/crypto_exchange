# crypto_exchange/OHLCV.py

from logging import getLogger

from munch import DefaultMunch
import pandas as pd

from .CryptoExchange import CryptoExchange, DEFAULT_EXCHANGE_ID
from util.timefunc import ms2str

logger = getLogger(__name__)

DEFAULT_TIMEFRAME = '4h'
DEFAULT_PAIR = 'BTC/USD'
BTC_USD_PAIRS = ['BTC/USD', 'BTC/USDT', 'BTC/USDC', 'BTC/GUSD']
DEFAULT_LIMIT = 100

class OHLCVException(Exception):
    pass

class OHLCV():
    def __init__(self, exchange_id: str = DEFAULT_EXCHANGE_ID,
                 pair: str = DEFAULT_PAIR,
                 timeframe: str = DEFAULT_TIMEFRAME):
        self.exchange_id = exchange_id
        self.pair = pair
        self.timeframe = timeframe
        self.exchange = CryptoExchange(exchange_id=exchange_id)
        if self.exchange is None:
            raise OBLCVException(f"{exchange_id} is not a valid exchange")
        if not self.exchange.has.fetchOHLCV:
            raise OHLCVException(f"Exchange {exchange_id} does not support OHLCV call")
        if pair not in self.exchange.symbols:
            raise OHLCVException(f"Exchange {exchange_id} does not support {pair} trading pair")

    def fetch(self, timeframe=None, since=None, limit=None, params={}):
        if timeframe is None:
            timeframe = self.timeframe

        print(f"{since=}")
        print(f"{limit=}")

        all_results = []
        done = False
        last_since = since
        while not done:
            results = self.exchange.exchange_class.fetchOHLCV(self.pair, timeframe=self.timeframe,
                                                              since=last_since, limit=None, params={})
            num_fetched = len(results)
            print(f"fetched: {num_fetched}")
            if num_fetched > 1:
                last_since = results[-1][0]
                print(f"Last since = {ms2str(last_since)}")
                all_results.extend(results)
            else:
                done = True

        df = pd.DataFrame(all_results, columns=['timestamp', 'open', 'high', 'low', 'close', 'volumne'])
        df['datetime'] = pd.to_datetime(df.timestamp, unit='ms')

        return df

