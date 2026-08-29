#!/usr/bin/env python
"""Reducer: Daily Demand
Sums trip counts per day of week.
"""
import sys

current_day = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        day, count = line.split("\t")
        count = int(count)
    except ValueError:
        continue

    if current_day == day:
        current_count += count
    else:
        if current_day is not None:
            print(f"{current_day}\t{current_count}")
        current_day = day
        current_count = count

if current_day is not None:
    print(f"{current_day}\t{current_count}")