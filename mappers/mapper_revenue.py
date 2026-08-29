#!/usr/bin/env python
"""Mapper: Revenue by Pickup Location
Emits (zone_name, "distance,fare,tip,total") per trip for the reducer to aggregate.
"""
import sys
import csv

def load_zone_lookup(path="taxi_zone_lookup.csv"):
    zones = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 3:
                continue
            zones[row[0]] = row[2]
    return zones

zones = load_zone_lookup()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 17:
        continue

    pu_location_id = fields[7]
    trip_distance = fields[4]
    fare_amount = fields[10]
    tip_amount = fields[13]
    total_amount = fields[16]

    try:
        float(trip_distance)
        float(fare_amount)
        float(tip_amount)
        float(total_amount)
    except ValueError:
        continue

    zone_name = zones.get(pu_location_id, f"Unknown Zone {pu_location_id}")

    print(f"{zone_name}\t{trip_distance},{fare_amount},{tip_amount},{total_amount}")