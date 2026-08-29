"""
Clean NYC TLC Yellow Taxi trip data per assignment requirements (section 7).

Identifies and reports (not silently drops) records with:
  - missing/null values in key fields
  - invalid passenger counts (0 or > 6)
  - zero/negative trip distances
  - invalid fares (fare_amount <= 0, or total_amount <= 0)
  - invalid timestamps (dropoff before/equal pickup, or outside expected month)
  - duplicate records
  - impossible trip durations (0 seconds, or > 6 hours)

Writes a cleaning report (counts + percentages) and cleaned CSVs.

Usage:
    python clean_taxi_data.py
"""

import pandas as pd
import os

INPUT_DIR = r"C:\taxi_data\csv"
OUTPUT_DIR = r"C:\taxi_data\cleaned"
REPORT_PATH = r"C:\taxi_data\cleaning_report.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# expected (year, month) per file, used to flag timestamps outside the reporting period
FILE_PERIODS = {
    "yellow_tripdata_2024-01.csv": (2024, 1),
    "yellow_tripdata_2024-02.csv": (2024, 2),
}

report_lines = []

def log(line=""):
    print(line)
    report_lines.append(line)


def clean_file(fname):
    year, month = FILE_PERIODS[fname]
    in_path = os.path.join(INPUT_DIR, fname)

    log(f"\n{'='*70}")
    log(f"Cleaning {fname}  (expected period: {year}-{month:02d})")
    log(f"{'='*70}")

    df = pd.read_csv(in_path, low_memory=False)
    total = len(df)
    log(f"Total records read: {total:,}")

    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors="coerce")
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors="coerce")

    # --- 1. Missing values in key fields ---
    key_fields = [
        "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",
        "trip_distance", "PULocationID", "DOLocationID", "fare_amount", "total_amount"
    ]
    missing_mask = df[key_fields].isnull().any(axis=1)
    missing_count = missing_mask.sum()
    log(f"\n1. Missing values in key fields: {missing_count:,} ({missing_count/total*100:.2f}%)")

    # --- 2. Invalid passenger counts (0 or > 6) ---
    invalid_passengers_mask = (df["passenger_count"].fillna(-1) <= 0) | (df["passenger_count"].fillna(-1) > 6)
    invalid_passengers_count = invalid_passengers_mask.sum()
    log(f"2. Invalid passenger counts (<=0 or >6): {invalid_passengers_count:,} ({invalid_passengers_count/total*100:.2f}%)")

    # --- 3. Zero/negative trip distance ---
    invalid_distance_mask = df["trip_distance"].fillna(-1) <= 0
    invalid_distance_count = invalid_distance_mask.sum()
    log(f"3. Zero/negative trip distance: {invalid_distance_count:,} ({invalid_distance_count/total*100:.2f}%)")

    # --- 4. Invalid fares ---
    invalid_fare_mask = (df["fare_amount"].fillna(-1) <= 0) | (df["total_amount"].fillna(-1) <= 0)
    invalid_fare_count = invalid_fare_mask.sum()
    log(f"4. Invalid fares (fare_amount or total_amount <= 0): {invalid_fare_count:,} ({invalid_fare_count/total*100:.2f}%)")

    # --- 5. Invalid timestamps ---
    bad_order_mask = df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"]
    period_start = pd.Timestamp(year=year, month=month, day=1)
    period_end = period_start + pd.offsets.MonthEnd(1) + pd.Timedelta(days=1)  # small buffer
    outside_period_mask = (df["tpep_pickup_datetime"] < period_start) | (df["tpep_pickup_datetime"] >= period_end)
    invalid_timestamp_mask = bad_order_mask | outside_period_mask | df["tpep_pickup_datetime"].isnull() | df["tpep_dropoff_datetime"].isnull()
    invalid_timestamp_count = invalid_timestamp_mask.sum()
    log(f"5. Invalid timestamps (dropoff<=pickup or outside reporting month): {invalid_timestamp_count:,} ({invalid_timestamp_count/total*100:.2f}%)")

    # --- 6. Duplicate records ---
    duplicate_mask = df.duplicated(keep="first")
    duplicate_count = duplicate_mask.sum()
    log(f"6. Duplicate records: {duplicate_count:,} ({duplicate_count/total*100:.2f}%)")

    # --- 7. Impossible trip durations ---
    duration_sec = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds()
    invalid_duration_mask = (duration_sec <= 0) | (duration_sec > 6 * 3600)  # 0 or >6 hours
    invalid_duration_count = invalid_duration_mask.sum()
    log(f"7. Impossible trip durations (<=0s or >6hrs): {invalid_duration_count:,} ({invalid_duration_count/total*100:.2f}%)")

    # --- Combine all issues ---
    all_bad_mask = (
        missing_mask | invalid_passengers_mask | invalid_distance_mask |
        invalid_fare_mask | invalid_timestamp_mask | duplicate_mask | invalid_duration_mask
    )
    total_bad = all_bad_mask.sum()
    log(f"\nTOTAL affected records (any issue, union): {total_bad:,} ({total_bad/total*100:.2f}%)")

    df_clean = df[~all_bad_mask].copy()
    clean_count = len(df_clean)
    log(f"Remaining clean records: {clean_count:,} ({clean_count/total*100:.2f}%)")

    out_path = os.path.join(OUTPUT_DIR, fname)
    df_clean.to_csv(out_path, index=False)
    log(f"Cleaned file written to: {out_path}")

    return total, total_bad, clean_count


def main():
    log("NYC TLC Yellow Taxi Data Cleaning Report")
    log(f"Generated by clean_taxi_data.py\n")

    grand_total = 0
    grand_bad = 0
    grand_clean = 0

    for fname in sorted(FILE_PERIODS.keys()):
        total, bad, clean = clean_file(fname)
        grand_total += total
        grand_bad += bad
        grand_clean += clean

    log(f"\n{'='*70}")
    log("GRAND TOTAL ACROSS ALL FILES")
    log(f"{'='*70}")
    log(f"Total records processed: {grand_total:,}")
    log(f"Total affected/removed:  {grand_bad:,} ({grand_bad/grand_total*100:.2f}%)")
    log(f"Total clean records:     {grand_clean:,} ({grand_clean/grand_total*100:.2f}%)")

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(report_lines))
    print(f"\nFull report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()