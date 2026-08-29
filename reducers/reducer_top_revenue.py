#!/usr/bin/env python
"""Reducer (Stage 2): Top 10 Revenue Zones
Collects all (zone, revenue) pairs and emits the top 10 by revenue.
"""
import sys

records = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        key, values = line.split("\t", 1)
        zone, revenue = values.rsplit(",", 1)
        revenue = float(revenue)
    except ValueError:
        continue

    records.append((zone, revenue))

records.sort(key=lambda x: x[1], reverse=True)

for rank, (zone, revenue) in enumerate(records[:10], start=1):
    print(f"{rank}\t{zone}\t{revenue:.2f}")