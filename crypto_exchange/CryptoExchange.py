# crypto_exchange/CryptoExchange.py

from logging import getLogger

import ccxt
from munch import DefaultMunch

logger = getLogger(__name__)

DEFAULT_EXCHANGE_ID = 'bitstamp'
DEFAULT_TIMEFRAME = '4h'
DEFAULT_PAIR = 'BTC/USD'
BTC_USD_PAIRS = ['BTC/USD', 'BTC/USDT', 'BTC/USDC', 'BTC/GUSD']


EXCHANGE_MAPPING = {
    'binance': ccxt.binance,
    'bitmex': ccxt.bitmex,
    'bitstamp': ccxt.bitstamp,
    'gemini': ccxt.gemini,
    'huobipro': ccxt.huobipro
}

def load_exchange_class(exchange_id: str, config: dict = {}):
    if exchange_id in EXCHANGE_MAPPING.keys():
        return EXCHANGE_MAPPING[exchange_id](config={})
    else:
        if not exchange_id in ccxt.exchanges:
            logger.error(f"Exchange ID '{exchange_id}' not supported.")
            return None
        try:
            exchange_class = getattr(ccxt, exchange_id)
            return exchange_class
        except AttributeError as e:
            logger.error(f"Exchange ID '{exchange_id}' not supported.")
            return None



class CryptoExchangeException(Exception):
    pass


class CryptoExchange():
    """CryptoExchange is a wrapper of the CCXT library"""
    def __init__(self, exchange_id: str = DEFAULT_EXCHANGE_ID, config: dict = {}):
        self.exchange_id = exchange_id
        self.exchange_class = None
        self.markets = None
        self.symbols = None
        self.has = None  # results of the exchange .has method
        self.timeframes = None # results of the exchange .timeframes method
        self.setup(config=config)

    def setup(self, config: dict={}):
        self.exchange_class = load_exchange_class(self.exchange_id, config=config)
        if self.exchange_class is None:
            msg = f"Invalid exchange_id={self.exchange_id}"
            logger.error(msg)
            raise CryptoExchangeException(msg)
        self.markets = self.exchange_class.load_markets()
        self.symbols = self.exchange_class.symbols
        self.has = DefaultMunch(None).fromDict(self.exchange_class.has)
        self.timeframes = self.exchange_class.timeframes
        self.exchange_class.enableRateLimit = True
