#!/usr/bin/env python
"""Mapper (Stage 2): Top 10 Revenue Zones
Reads Stage 1 output (zone, count, total_fare, total_tips, total_revenue, avg_fare, avg_distance).
Emits (constant_key, "zone,total_revenue") so all records land in one reducer for ranking.
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        zone, count, total_fare, total_tips, total_revenue, avg_fare, avg_distance = line.rsplit("\t", 6)
    except ValueError:
        continue

    try:
        rev = float(total_revenue)
    except ValueError:
        continue

    print(f"ALL\t{zone},{rev}")