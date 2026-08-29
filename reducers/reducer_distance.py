#!/usr/bin/env python
"""Reducer: Distance-Based Fare Analysis
Aggregates trip count, avg fare, avg distance, avg fare-per-mile per distance category.
"""
import sys

current_cat = None
count = 0
sum_distance = 0.0
sum_fare = 0.0
sum_total = 0.0

def emit(cat, count, sum_distance, sum_fare, sum_total):
    avg_fare = sum_fare / count if count else 0
    avg_distance = sum_distance / count if count else 0
    avg_total = sum_total / count if count else 0
    fare_per_mile = sum_fare / sum_distance if sum_distance else 0
    print(f"{cat}\t{count}\t{avg_distance:.2f}\t{avg_fare:.2f}\t{avg_total:.2f}\t{fare_per_mile:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        cat, values = line.rsplit("\t", 1)
        distance, fare, total = values.split(",")
        distance, fare, total = float(distance), float(fare), float(total)
    except ValueError:
        continue

    if current_cat == cat:
        count += 1
        sum_distance += distance
        sum_fare += fare
        sum_total += total
    else:
        if current_cat is not None:
            emit(current_cat, count, sum_distance, sum_fare, sum_total)
        current_cat = cat
        count = 1
        sum_distance = distance
        sum_fare = fare
        sum_total = total

if current_cat is not None:
    emit(current_cat, count, sum_distance, sum_fare, sum_total)