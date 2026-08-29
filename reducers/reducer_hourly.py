#!/usr/bin/env python
"""Reducer: Hourly Taxi Demand
Sums trip counts per hour. Relies on Hadoop's shuffle/sort to group by key.
"""
import sys

current_hour = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        hour, count = line.split("\t")
        count = int(count)
    except ValueError:
        continue

    if current_hour == hour:
        current_count += count
    else:
        if current_hour is not None:
            print(f"{current_hour}\t{current_count}")
        current_hour = hour
        current_count = count

# emit the last group
if current_hour is not None:
    print(f"{current_hour}\t{current_count}")