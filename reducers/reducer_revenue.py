#!/usr/bin/env python
"""Reducer: Revenue by Pickup Location
Aggregates trip count, total fare, total tips, total revenue,
average fare, average distance per zone.
"""
import sys

current_zone = None
count = 0
sum_distance = 0.0
sum_fare = 0.0
sum_tip = 0.0
sum_total = 0.0

def emit(zone, count, sum_distance, sum_fare, sum_tip, sum_total):
    avg_fare = sum_fare / count if count else 0
    avg_distance = sum_distance / count if count else 0
    print(f"{zone}\t{count}\t{sum_fare:.2f}\t{sum_tip:.2f}\t{sum_total:.2f}\t{avg_fare:.2f}\t{avg_distance:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        zone, values = line.rsplit("\t", 1)
        distance, fare, tip, total = values.split(",")
        distance, fare, tip, total = float(distance), float(fare), float(tip), float(total)
    except ValueError:
        continue

    if current_zone == zone:
        count += 1
        sum_distance += distance
        sum_fare += fare
        sum_tip += tip
        sum_total += total
    else:
        if current_zone is not None:
            emit(current_zone, count, sum_distance, sum_fare, sum_tip, sum_total)
        current_zone = zone
        count = 1
        sum_distance = distance
        sum_fare = fare
        sum_tip = tip
        sum_total = total

if current_zone is not None:
    emit(current_zone, count, sum_distance, sum_fare, sum_tip, sum_total)