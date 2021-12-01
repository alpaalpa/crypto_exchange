# crypto_exchange/OHLCV.py

from logging import getLogger

from munch import DefaultMunch

from .CryptoExchange import CryptoExchange, DEFAULT_EXCHANGE_ID

logger = getLogger(__name__)

DEFAULT_TIMEFRAME = '4h'
DEFAULT_PAIR = 'BTC/USD'
BTC_USD_PAIRS = ['BTC/USD', 'BTC/USDT', 'BTC/USDC', 'BTC/GUSD']

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

        return self.exchange.exchange_class.fetchOHLCV(self.pair, timeframe='1m', since=None, limit=None, params={})
