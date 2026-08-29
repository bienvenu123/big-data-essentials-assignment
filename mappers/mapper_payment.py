#!/usr/bin/env python
"""Mapper: Payment Method Analysis
Maps payment_type code to a label, emits (label, "fare,tip,total") per trip.
"""
import sys

PAYMENT_LABELS = {
    "1": "Credit card",
    "2": "Cash",
    "3": "No charge",
    "4": "Dispute",
    "5": "Unknown",
    "6": "Voided trip",
}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")

    if fields[0] == "VendorID":
        continue

    if len(fields) < 17:
        continue

    payment_type = fields[9]
    fare_amount = fields[10]
    tip_amount = fields[13]
    total_amount = fields[16]

    try:
        float(fare_amount)
        float(tip_amount)
        float(total_amount)
    except ValueError:
        continue

    label = PAYMENT_LABELS.get(payment_type, f"Other ({payment_type})")

    print(f"{label}\t{fare_amount},{tip_amount},{total_amount}")