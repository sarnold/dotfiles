#!/usr/bin/env python3
"""
Wrapper for timew extension totals.py (a cheesy way to get daily
sub-totals of job tags for a month).
"""
import subprocess as sp

from datetime import date, datetime, timedelta
from shlex import split


def datespan(startDate, endDate, delta=timedelta(days=1)):
    """
    Date generator for each day in the interval as YYYY-MM-DD.
    """
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

today = date.today()
tomorrow = date(today.year, today.month, today.day + 1)
month_start = date(today.year, today.month, 1)

start_val = month_start
end_val = tomorrow

for day in datespan(start_val, end_val, delta=timedelta(days=1)):
    if day is not None:
        timew_cmd_str = "timew totals" + f" {day}"
        timew_cmd = timew_cmd_str.split()

        sp.run(timew_cmd)
