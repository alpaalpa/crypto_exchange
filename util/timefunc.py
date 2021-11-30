# util/timefunc.py
from datetime import datetime, timezone, timedelta
from logging import getLogger
import time

logger = getLogger(__name__)

# library for time stamp related functions.
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo

# Supported timeframes name and their equivalent in seconds
TIMEFRAMES = {
    '1m': 60,
    '5m': 5 * 60,
    '10m': 10 * 60,
    '15m': 15 * 60,
    '30m': 30 * 60,
    '60m': 60 * 60,
    '1h': 60 * 60,
    '2h': 2 * 60 * 60,
    '3h': 3 * 60 * 60,
    '4h': 4 * 60 * 60,
    '6h': 6 * 60 * 60,
    '12h': 12 * 60 * 60,
    '24h': 24 * 60 * 60,
    '1d': 24 * 60 * 60,
}

DEFAULT_TIMEFRAME = '4h'


def now_ms():
    ''' Return current timestamp in milliseconds
    '''
    return int(time.time() * 1000)


def ms2str(ts: int, local=False):
    ''' Convert timestamp to string. Use UTC by default

    Parameters
    ==========

    ts: int
        timestamp in milliseconds
    local: bool
        If True, return time in local timezone
    '''

    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    if local:
        return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def get_ms(year=2009, month=1, day=1, hour=0, minute=0, second=0, local=False):
    ''' Get time in milliseconds for a particular time.
    '''
    if local:
        dt = datetime(year, month, day, hour, minute, second,
                      tzinfo=LOCAL_TIMEZONE)
    else:
        dt = datetime(year, month, day, hour, minute, second,
                      tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def get_begin_next(ts: int = now_ms(), timeframe=DEFAULT_TIMEFRAME):
    ''' Returns a tuple of (begin_timestamp, end_timestamp) where
    a partifular timestamp (in ms) falls in for a particular
    timeframe.

    Note, this is for UTC only.  E.g., chosing timeframe of '1d'
    will returns beginning of the day in UTC not local timezone.

    E.g. ms = 2020-02-22 13:34:00
        timeframe = '4h'
        begin = 2020-02-22 12:00:00
        end = 2020-02-22 16:00:00

        both returned values are in milliseconds

    Parameters
    ==========
    ms: int
        timestamp in milliseconds
    timeframe: str (one of TIMEFRAMES)
        a string representing a timeframe (e.g. 1m, 2h, 4h, 1d)

    Returns
    =======
    (int, int)
        A tuple contain the begin timestamp of the current and
        next timeframe

    '''

    timeframe_seconds = TIMEFRAMES.get(timeframe, None)
    if timeframe_seconds is None:
        logger.error(f"{timeframe} is not a valid timeframes")
        return None, None

    dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
    logger.debug(f'TS:    {dt.strftime("%Y-%m-%d %H:%M:%S %Z")}')
    logger.debug(f'Local: {ms2str(ts, local=True)}')
    dt = dt.replace(second=0, microsecond=0).replace(tzinfo=None)

    delta = timedelta(seconds=timeframe_seconds)

    begin_dt = dt - (dt - datetime.min) % delta
    next_dt = dt + (datetime.min - dt) % delta

    logger.debug(f'Begin: {begin_dt.strftime("%Y-%m-%d %H:%M:%S %Z")}')
    logger.debug(f'Next:  {next_dt.strftime("%Y-%m-%d %H:%M:%S %Z")}')

    begin_dt = begin_dt.replace(tzinfo=timezone.utc)
    next_dt = next_dt.replace(tzinfo=timezone.utc)

    logger.debug(f'Begin: {begin_dt.strftime("%Y-%m-%d %H:%M:%S %Z")}')
    logger.debug(f'Next:  {next_dt.strftime("%Y-%m-%d %H:%M:%S %Z")}')

    begin_ts = int(begin_dt.timestamp() * 1000)
    next_ts = int(next_dt.timestamp() * 1000)

    logger.debug(ms2str(begin_ts, local=True))
    logger.debug(ms2str(next_ts, local=True))

    return begin_ts, next_ts
