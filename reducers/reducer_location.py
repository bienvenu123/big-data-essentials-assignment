#!/usr/bin/env python
"""Reducer: Pickup Location Analysis
Sums trip counts per pickup zone.
"""
import sys

current_zone = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        zone, count = line.rsplit("\t", 1)
        count = int(count)
    except ValueError:
        continue

    if current_zone == zone:
        current_count += count
    else:
        if current_zone is not None:
            print(f"{current_zone}\t{current_count}")
        current_zone = zone
        current_count = count

if current_zone is not None:
    print(f"{current_zone}\t{current_count}")