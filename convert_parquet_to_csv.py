"""
Convert NYC TLC Yellow Taxi Parquet trip files to CSV for HDFS/Hadoop Streaming.

Usage:
    python convert_parquet_to_csv.py

Reads all .parquet files in the input folder and writes matching .csv files
to the output folder, printing row counts as it goes.
"""

import pandas as pd
import os

INPUT_DIR = r"C:\taxi_data"
OUTPUT_DIR = r"C:\taxi_data\csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

parquet_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".parquet")]

if not parquet_files:
    print(f"No .parquet files found in {INPUT_DIR}")
else:
    total_rows = 0
    for fname in sorted(parquet_files):
        in_path = os.path.join(INPUT_DIR, fname)
        out_name = fname.replace(".parquet", ".csv")
        out_path = os.path.join(OUTPUT_DIR, out_name)

        print(f"Reading {fname} ...")
        df = pd.read_parquet(in_path)
        row_count = len(df)
        total_rows += row_count

        print(f"  -> {row_count:,} rows, {len(df.columns)} columns")
        print(f"  Writing {out_name} ...")
        df.to_csv(out_path, index=False)
        print(f"  Done: {out_path}")
        print()

    print(f"TOTAL ROWS ACROSS ALL FILES: {total_rows:,}")