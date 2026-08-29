#!/usr/bin/env python
"""Mapper: Busiest Routes
Creates a route key "PickupZone -> DropoffZone", emits (route, "total_amount") per trip.
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

    pu_id = fields[7]
    do_id = fields[8]
    total_amount = fields[16]

    try:
        total = float(total_amount)
    except ValueError:
        continue

    pu_zone = zones.get(pu_id, f"Unknown Zone {pu_id}")
    do_zone = zones.get(do_id, f"Unknown Zone {do_id}")

    route = f"{pu_zone} -> {do_zone}"

    print(f"{route}\t{total}")