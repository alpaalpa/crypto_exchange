# util/timefunc.py
from datetime import datetime
import time

# library for time stamp related functions.


def now():
    ''' Return current timestamp in milliseconds
    '''
    return int(time.time() * 1000)

def ms2str(ts: int, local=False):
    ''' Convert timestamp to string. Use UTC by default
    '''
    Parameters
    ==========
    ts: int
        timestamp in milliseconds
    local: bool
        If True, return time in local timezone

    dt_object = datetime.fromtimestamp(ts / 1000)