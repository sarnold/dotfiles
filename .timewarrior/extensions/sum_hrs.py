"""
Sum time strings as timedeltas and print total
"""

import time
from datetime import timedelta


h = [
    '0:54:53',
    '6:26:41',
    '1:27:08',
    '0:36:28',
    '0:25:21',
    '3:17:35',
    '0:38:01',
    '3:34:35',
    '2:21:16',
    '0:59:22',
    '0:34:26',
]


def to_td(h):
    ho, mi, se = h.split(':')
    return timedelta(hours=int(ho), minutes=int(mi), seconds=int(se))


def strf_delta(td):
    '''
    String format a timedelta => (HH:MM:SS)
    '''
    h, r = divmod(int(td.total_seconds()), 60 * 60)
    m, s = divmod(r, 60)
    h, m, s = (str(x).zfill(2) for x in (h, m, s))
    return f"{h}:{m}:{s}"


delta = sum(map(to_td, h), timedelta())
# print(delta)

time_str = strf_delta(delta)
print(time_str)
