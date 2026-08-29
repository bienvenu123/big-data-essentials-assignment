#!/usr/bin/env python
"""Reducer: Payment Method Analysis
Aggregates trip count, total revenue, average fare, average tip per payment method.
"""
import sys

current_label = None
count = 0
sum_fare = 0.0
sum_tip = 0.0
sum_total = 0.0

def emit(label, count, sum_fare, sum_tip, sum_total):
    avg_fare = sum_fare / count if count else 0
    avg_tip = sum_tip / count if count else 0
    print(f"{label}\t{count}\t{sum_total:.2f}\t{avg_fare:.2f}\t{avg_tip:.2f}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        label, values = line.rsplit("\t", 1)
        fare, tip, total = values.split(",")
        fare, tip, total = float(fare), float(tip), float(total)
    except ValueError:
        continue

    if current_label == label:
        count += 1
        sum_fare += fare
        sum_tip += tip
        sum_total += total
    else:
        if current_label is not None:
            emit(current_label, count, sum_fare, sum_tip, sum_total)
        current_label = label
        count = 1
        sum_fare = fare
        sum_tip = tip
        sum_total = total

if current_label is not None:
    emit(current_label, count, sum_fare, sum_tip, sum_total)