#!/usr/bin/env python3
'''
    Modified from upstream example; extract a Job tag from the first
    comma-separated split of the full tag string and produce subtotals
    for each <jobname> where <jobname> is a short mnemonic for customer
    and/or task, for example::

        $ timew start xyz3D-sw,"factory reset patch"

    using a more specific task string in quotes following a comma.
    Then run ``timew oneline march`` or some other time interval.

    This report will output a oneline per day for each <jobname> format::

        -- xyz3D-cyber
        3/1 1.5h review security controls for yocto
        3/4 2.5h review security controls for yocto
        3/8 1h security meeting

        -- xyz3D-sw
        3/7 2h look for PCIe example project that works with Quartus 23
        3/12 0.5h simple system diagram for internal use

    Assumptions:

    1. report will be driven by arbitrary duration, ie, day, week, month
    2. a single timew interval cannot be longer than a workday
'''

import sys
from typing import Dict, List
from datetime import datetime, timedelta

from timewreport.parser import TimeWarriorParser

parser = TimeWarriorParser(sys.stdin)

totals: Dict[str, timedelta] = dict()
final_total = timedelta(hours=0)

job_days: List[str] = list()
job_tags: List[str] = list()
formatted = timedelta(0)


def strf_delta(td):
    '''
    String format a timedelta => (HH:MM:SS)
    '''
    h, r = divmod(int(td.total_seconds()), 60 * 60)
    m, s = divmod(r, 60)
    h, m, s = (str(x).zfill(2) for x in (h, m, s))
    return f"{h}:{m}:{s}"


def update_job_tags(tag):
    '''
    Extract job tags from full tag string
    '''
    job_tag = tag.split(',', maxsplit=1)
    if job_tag[0] not in job_tags:
        job_tags.append(job_tag[0])


def update_job_days(interval):
    '''
    Extract job days from interval start date
    '''
    job_day = interval.get_start_date()
    if job_day not in job_days:
        job_days.append(job_day)


# need to load data for job days/tags before starting report processing
for interval in parser.get_intervals():
    update_job_days(interval)
    for tag in interval.get_tags():
        update_job_tags(tag)


print(f'Duration has {len(job_days)} days with tags and {len(job_tags)} total job tags:')
print(sorted(job_tags))
print('')

for job_tag in sorted(job_tags):
    print(f'-- {job_tag}')
    tracked_total = timedelta(hours=0)
    for job_day in sorted(job_days):
        job_intervals = [x for x in parser.get_intervals() if x.get_start_date() == job_day]
        for interval in job_intervals:
            tracked_hrs = interval.get_duration()
            tags = [x for x in interval.get_tags() if x.split(',', maxsplit=1)[0] == job_tag]
            for tag in tags:
                if tag in totals:
                    totals[tag] += tracked_hrs
                else:
                    totals[tag] = tracked_hrs
                tracked_total += tracked_hrs

        for tag in sorted(totals):
            print(f'{job_day} {totals[tag]} {tag}')
        totals.clear()
    print('')
    final_total += tracked_total

    print(f'Total for {job_tag}: {strf_delta(tracked_total)} hrs\n')
print(f'Final total for all jobs in duration: {strf_delta(final_total)} hrs\n\n')
