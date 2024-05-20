"""
Sum time strings as timedeltas and print total
"""

from datetime import timedelta

h = ['3:00:00','1:07:00', '4:00:00', '4:05:00', '4:10:00', '4:03:00']

def to_td(h):
    ho, mi, se = h.split(':')
    return timedelta(hours=int(ho), minutes=int(mi), seconds=int(se))

print(str(sum(map(to_td, h), timedelta())))
