#!/usr/bin/env python
"""Reducer: Trip Duration Analysis
Aggregates trip count, avg duration, avg fare, avg distance, avg tip per duration bucket.
"""
import sys

current_cat = None
count = 0
sum_duration = 0.0
sum_fare = 0.0
sum_distance = 0.0
sum_tip = 0.0

def emit(cat, count, sum_duration, sum_fare, sum_distance, sum_tip):
    avg_duration = sum_duration / count if count else 0
    avg_fare = sum_fare / count if count else 0
    avg_distance = sum_distance / count if count else 0
    avg_tip = sum_tip / count if count else 0
    print(f"{cat}\t{count}\t{avg_duration:.2f}\t{avg_fare:.2f}\t{avg_distance:.2f}\t{avg_tip:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        cat, values = line.rsplit("\t", 1)
        duration, fare, distance, tip = values.split(",")
        duration, fare, distance, tip = float(duration), float(fare), float(distance), float(tip)
    except ValueError:
        continue

    if current_cat == cat:
        count += 1
        sum_duration += duration
        sum_fare += fare
        sum_distance += distance
        sum_tip += tip
    else:
        if current_cat is not None:
            emit(current_cat, count, sum_duration, sum_fare, sum_distance, sum_tip)
        current_cat = cat
        count = 1
        sum_duration = duration
        sum_fare = fare
        sum_distance = distance
        sum_tip = tip

if current_cat is not None:
    emit(current_cat, count, sum_duration, sum_fare, sum_distance, sum_tip)