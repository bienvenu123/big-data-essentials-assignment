#!/usr/bin/env python
"""Mapper: Pickup Location Analysis
Loads taxi_zone_lookup.csv into memory, joins PULocationID -> Zone name,
emits (zone_name, 1).
"""
import sys
import csv

def load_zone_lookup(path="taxi_zone_lookup.csv"):
    zones = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 3:
                continue
            location_id = row[0]
            zone_name = row[2]
            zones[location_id] = zone_name
    return zones

zones = load_zone_lookup()

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 8:
        continue

    pu_location_id = fields[7]  # PULocationID
    zone_name = zones.get(pu_location_id, f"Unknown Zone {pu_location_id}")

    print(f"{zone_name}\t1")