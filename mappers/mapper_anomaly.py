#!/usr/bin/env python
"""Mapper: Anomaly Detection
Flags suspicious records on RAW (uncleaned) data using the same criteria
as the cleaning stage, plus extreme fare-per-mile.
Emits (anomaly_type, 1) for each issue found (a record can trigger multiple).
Also emits ("TOTAL_RECORDS", 1) for every record, to compute overall percentage.
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

    if len(fields) < 17:
        continue

    print("TOTAL_RECORDS\t1")

    passenger_count = fields[3]
    trip_distance = fields[4]
    fare_amount = fields[10]
    total_amount = fields[16]
    pickup_dt = fields[1]
    dropoff_dt = fields[2]

    is_anomaly = False

    # invalid passenger count
    try:
        pc = float(passenger_count)
        if pc <= 0 or pc > 6:
            print("invalid_passenger_count\t1")
            is_anomaly = True
    except ValueError:
        print("invalid_passenger_count\t1")
        is_anomaly = True

    # invalid distance
    try:
        dist = float(trip_distance)
        if dist <= 0:
            print("invalid_distance\t1")
            is_anomaly = True
    except ValueError:
        print("invalid_distance\t1")
        is_anomaly = True
        dist = None

    # invalid fare
    try:
        fare = float(fare_amount)
        total = float(total_amount)
        if fare <= 0 or total <= 0:
            print("invalid_fare\t1")
            is_anomaly = True
    except ValueError:
        print("invalid_fare\t1")
        is_anomaly = True
        fare = None

    # invalid duration / timestamps
    duration_min = None
    try:
        pu = datetime.strptime(pickup_dt, "%Y-%m-%d %H:%M:%S")
        do = datetime.strptime(dropoff_dt, "%Y-%m-%d %H:%M:%S")
        duration_sec = (do - pu).total_seconds()
        duration_min = duration_sec / 60.0
        if duration_sec <= 0 or duration_sec > 6 * 3600:
            print("invalid_duration\t1")
            is_anomaly = True
    except ValueError:
        print("invalid_duration\t1")
        is_anomaly = True

    # extreme fare-per-mile (only checkable when both are valid and positive)
    if dist is not None and fare is not None and dist > 0:
        fare_per_mile = fare / dist
        if fare_per_mile > 50:  # threshold: $50/mile is extreme
            print("extreme_fare_per_mile\t1")
            is_anomaly = True

    if is_anomaly:
        print("ANY_ANOMALY\t1")