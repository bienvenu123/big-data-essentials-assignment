#!/usr/bin/env python
"""Mapper: Hourly Taxi Demand
Reads cleaned trip records, extracts the pickup hour, emits (hour, 1).
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    # skip header row
    if fields[0] == "VendorID":
        continue

    if len(fields) < 3:
        continue

    pickup_dt = fields[1]  # tpep_pickup_datetime, e.g. 2024-01-01 00:57:55

    try:
        # extract hour portion, e.g. "2024-01-01 00:57:55" -> "00"
        hour = pickup_dt.split(" ")[1].split(":")[0]
        hour = int(hour)
        if 0 <= hour <= 23:
            print(f"{hour}\t1")
    except (IndexError, ValueError):
        continue