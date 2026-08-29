"""
Performance comparison: Hourly Taxi Demand via Pandas (section 12).
Times reading, computing, and reports memory usage for comparison against
the equivalent Hadoop Streaming MapReduce job.
"""
import pandas as pd
import time
import os

CLEANED_DIR = r"C:\taxi_data\cleaned"
files = [
    os.path.join(CLEANED_DIR, "yellow_tripdata_2024-01.csv"),
    os.path.join(CLEANED_DIR, "yellow_tripdata_2024-02.csv"),
]

start_time = time.time()

dfs = []
for f in files:
    dfs.append(pd.read_csv(f, low_memory=False))
df = pd.concat(dfs, ignore_index=True)

read_time = time.time()

df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["hour"] = df["tpep_pickup_datetime"].dt.hour

hourly_counts = df.groupby("hour").size().sort_index()

compute_time = time.time()

print("=== Pandas Hourly Demand — Performance Report ===")
print(f"Total records: {len(df):,}")
print(f"Read time: {read_time - start_time:.2f} sec")
print(f"Compute time: {compute_time - read_time:.2f} sec")
print(f"Total time: {compute_time - start_time:.2f} sec")
print(f"Memory usage (approx): {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
print()
print("Hourly counts:")
print(hourly_counts.to_string())