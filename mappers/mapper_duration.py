#!/usr/bin/env python
"""Mapper: Trip Duration Analysis
Computes trip duration in minutes, buckets it, emits (category, "duration,fare,distance,tip") per trip.
"""
import sys
from datetime import datetime

def get_category(minutes):
    if minutes < 5:
        return "0-5 min"
    elif minutes < 15:
        return "5-15 min"
    elif minutes < 30:
        return "15-30 min"
    elif minutes < 60:
        return "30-60 min"
    else:
        return "60+ min"

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 17:
        continue

    pickup_dt = fields[1]
    dropoff_dt = fields[2]
    trip_distance = fields[4]
    fare_amount = fields[10]
    tip_amount = fields[13]

    try:
        pu = datetime.strptime(pickup_dt, "%Y-%m-%d %H:%M:%S")
        do = datetime.strptime(dropoff_dt, "%Y-%m-%d %H:%M:%S")
        distance = float(trip_distance)
        fare = float(fare_amount)
        tip = float(tip_amount)
    except ValueError:
        continue

    duration_min = (do - pu).total_seconds() / 60.0

    if duration_min <= 0:
        continue

    category = get_category(duration_min)

    print(f"{category}\t{duration_min},{fare},{distance},{tip}")