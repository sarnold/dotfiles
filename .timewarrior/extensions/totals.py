#!/usr/bin/env python3
import sys
from datetime import timedelta

from timewreport.parser import TimeWarriorParser

parser = TimeWarriorParser(sys.stdin)
totals = dict()
job_list = []
job_totals = []


def strf_delta(td):
    """
    String format a timedelta => (HH;MM:SS)
    """
    h, r = divmod(int(td.total_seconds()), 60*60)
    m, s = divmod(r, 60)
    h, m, s = (str(x).zfill(2) for x in (h, m, s))
    return f"{h}:{m}:{s}"

def get_job_tags(tag):
    """
    Extract job tags from full tag
    """
    job_tag = tag.split(',', maxsplit=1)
    if job_tag[0] not in job_list:
        job_list.append(job_tag[0])

for interval in parser.get_intervals():
    tracked = interval.get_duration()

    for tag in interval.get_tags():
        get_job_tags(tag)
        if tag in totals:
            totals[tag] += tracked
        else:
            totals[tag] = tracked

# Determine largest tag width.
max_width = len('Total')

for tag in totals:
    if len(tag) > max_width:
        max_width = len(tag)

print("Job tags: {}\n".format(job_list))

# Compose report header.
print('Total by Tag\n')

# Compose table header.
print('{:{width}} {:>10}'.format('Tag', 'Total', width=max_width))
print('{} {}'.format('-' * max_width, '----------'))

# Compose table rows.
grand_total = timedelta(0)

for tag in sorted(totals):
    formatted = totals[tag]
    grand_total += totals[tag]
    print('{:{width}} {:10}'.format(tag, str(formatted), width=max_width))

# Compose total.
print('{} {}'.format(' ' * max_width, '----------'))
print('{:{width}} {:10}'.format('Total', strf_delta(grand_total), width=max_width))
