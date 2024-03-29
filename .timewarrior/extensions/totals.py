#!/usr/bin/env python3
"""
    Modified from upstream example; extract a Job tag from the first
    comma-separated split of the full tag string and produce subtotals
    for each <jobname>

        ``$ timew start jobname,"factory reset patch"``

    then run ``timew totals today``
"""

import sys
from typing import Dict, List
from datetime import datetime, timedelta

from timewreport.parser import TimeWarriorParser

parser = TimeWarriorParser(sys.stdin)

totals: Dict[str, timedelta] = dict()
job_totals: Dict[str, timedelta] = dict()
job_tags = []

grand_total = timedelta(0)
oldest: datetime.date = None
newest: datetime.date = None

def strf_delta(td):
    '''
    String format a timedelta => (HH:MM:SS)
    '''
    h, r = divmod(int(td.total_seconds()), 60 * 60)
    m, s = divmod(r, 60)
    h, m, s = (str(x).zfill(2) for x in (h, m, s))
    return f"{h}:{m}:{s}"


def get_job_tags(tag):
    '''
    Extract job tags from full tag string
    '''
    job_tag = tag.split(',', maxsplit=1)
    if job_tag[0] not in job_tags:
        job_tags.append(job_tag[0])


for interval in parser.get_intervals():
    tracked = interval.get_duration()
    startd = interval.get_start_date()
    endd = interval.get_end_date() if not interval.is_open() else ''
    if oldest is None:
        oldest = startd
        newest = endd
    if startd < oldest:
        oldest = startd
    if endd > newest:
        newest = endd

    for tag in interval.get_tags():
        if tag in totals:
            totals[tag] += tracked
        else:
            totals[tag] = tracked
        get_job_tags(tag)
        for job in job_tags:
            if job in tag:
                if job in job_totals:
                    job_totals[job] += tracked
                else:
                    job_totals[job] = tracked


# Determine largest tag width.
max_width = len('Total')

for tag in totals:
    if len(tag) > max_width:
        max_width = len(tag)

if newest is not None:
    # Compose report header.
    if oldest == newest:
        print(f'Total by tag for {newest}\n')
    else:
        print(f'Total by tag for {oldest} to {newest}\n')

    # Compose table header.
    print('{:{width}} {:>10}'.format('Tag', 'Total', width=max_width))
    print('{} {}'.format('-' * max_width, '----------'))

    # Compose table rows.
    for tag in sorted(totals):
        formatted = totals[tag]
        grand_total += totals[tag]
        print('{:{width}} {:10}'.format(tag, str(formatted), width=max_width))

    # Compose job subtotal header.
    print('{:{width}} {:10}'.format('\nJob', ' Total', width=max_width))
    print('{} {}'.format('-' * max_width, '----------'))

    for job in sorted(job_totals):
        subtotals = job_totals[job]
        print('{:{width}} {:10}'.format(job, strf_delta(subtotals), width=max_width))

    # Compose total.
    print('{} {}'.format(' ' * max_width, '----------'))
    print('{:{width}} {:10}'.format('Total', strf_delta(grand_total), width=max_width))
