#!/usr/bin/env python
"""Mapper: Distance-Based Fare Analysis
Buckets trips into distance categories, emits (category, "distance,fare,total") per trip.
"""
import sys

def get_category(distance):
    if distance < 2:
        return "0-2 miles"
    elif distance < 5:
        return "2-5 miles"
    elif distance < 10:
        return "5-10 miles"
    elif distance < 20:
        return "10-20 miles"
    else:
        return "20+ miles"

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 17:
        continue

    trip_distance = fields[4]
    fare_amount = fields[10]
    total_amount = fields[16]

    try:
        distance = float(trip_distance)
        fare = float(fare_amount)
        total = float(total_amount)
    except ValueError:
        continue

    if distance <= 0:
        continue

    category = get_category(distance)

    print(f"{category}\t{distance},{fare},{total}")