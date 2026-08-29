#!/usr/bin/env python
"""Mapper: Daily Demand
Extracts day of week from pickup timestamp, emits (day_name, 1).
"""
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 3:
        continue

    pickup_dt = fields[1]  # e.g. 2024-01-01 00:57:55

    try:
        dt = datetime.strptime(pickup_dt, "%Y-%m-%d %H:%M:%S")
        day_name = dt.strftime("%A")  # e.g. "Monday"
        print(f"{day_name}\t1")
    except ValueError:
        continue