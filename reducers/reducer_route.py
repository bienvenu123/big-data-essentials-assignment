#!/usr/bin/env python
"""Reducer: Busiest Routes
Aggregates trip count and total revenue per route.
"""
import sys

current_route = None
count = 0
sum_total = 0.0

def emit(route, count, sum_total):
    print(f"{route}\t{count}\t{sum_total:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        route, total = line.rsplit("\t", 1)
        total = float(total)
    except ValueError:
        continue

    if current_route == route:
        count += 1
        sum_total += total
    else:
        if current_route is not None:
            emit(current_route, count, sum_total)
        current_route = route
        count = 1
        sum_total = total

if current_route is not None:
    emit(current_route, count, sum_total)