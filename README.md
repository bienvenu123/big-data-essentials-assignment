# NYC TLC Taxi Big Data Analytics — Hadoop MapReduce Project

## Overview

This project implements a Hadoop-based analytics pipeline for NYC TLC Yellow
Taxi trip data, using HDFS for distributed storage and Python-based Hadoop
Streaming for distributed MapReduce processing.

**Dataset:** NYC TLC Yellow Taxi Trip Records — January and February 2024
(5,972,150 raw records; 5,439,872 records after cleaning).

## Environment

- **OS:** Windows 10/11
- **Hadoop version:** 3.2.4 (native Windows install, `HADOOP_HOME=C:\hadoop\hadoop-3.2.4`)
- **Java:** 1.8.0_202
- **Python:** 3.14.4, with `pandas` and `pyarrow`
- **Cluster topology:** single-node (1 NameNode, 1 DataNode, 1 ResourceManager,
  1 NodeManager), Capacity Scheduler

### Known environment fixes applied

1. **`yarn-site.xml` typo:** the ShuffleHandler class name was mis-cased
   (`shuffleHandler` instead of `ShuffleHandler`), silently preventing
   NodeManager from starting. Fixed to:
   `org.apache.hadoop.mapred.ShuffleHandler`
2. **`winutils.exe` / `hadoop.dll` incompatibility:** the bundled Windows
   native binaries were incompatible with this system
   (`CreateProcess error=216`). Replaced with the Hadoop 3.2.2 build from
   the `cdarlint/winutils` GitHub repository (binary-compatible with 3.2.x),
   placed in `%HADOOP_HOME%\bin\` and `hadoop.dll` additionally copied to
   `C:\Windows\System32\`.
3. **Hadoop Streaming `-files` on Windows:** the comma-separated file list
   must be double-quoted (e.g. `-files "a.py,b.py"`), otherwise `cmd.exe`
   splits on the unquoted comma and Hadoop Streaming rejects the extra
   argument.

## Directory Structure

```
C:\taxi_data\                  Local raw/cleaned data and scripts
  yellow_tripdata_2024-01.parquet
  yellow_tripdata_2024-02.parquet
  csv\                         Converted raw CSVs
  cleaned\                     Cleaned CSVs (uploaded to HDFS)
  cleaning_report.txt
  convert_parquet_to_csv.py
  clean_taxi_data.py

C:\taxi_project\                Mapper/reducer scripts + local project root
  mappers\  reducers\           Organized copies (per assignment structure)
  mapper_*.py  reducer_*.py     Working copies used with Hadoop Streaming -files
  taxi_zone_lookup.csv          Copied here for map-side joins
  perf_compare_pandas.py

HDFS (/taxi_project/):
  input/raw/                    Uncleaned CSVs + zone lookup table
  input/cleaned/                Cleaned CSVs (source for all analytical jobs)
  output/hourly/                Job 1 results
  output/daily/                 Job 2 results
  output/locations/             Job 3 results
  output/revenue/               Job 4 results (Multi-Stage: Stage 1)
  output/payment/               Job 5 results
  output/distance/              Job 6 results
  output/routes/                Job 7 results
  output/duration/              Job 8 results
  output/anomalies/             Job 9 results (run on raw data)
  output/top_revenue_zones/     Job 10 results (Multi-Stage: Stage 2)
  archive/                      Cleaning report
```

## How to Reproduce

1. **Start the cluster:**
   ```
   start-dfs.cmd
   start-yarn.cmd
   jps    # confirm NameNode, DataNode, ResourceManager, NodeManager all running
   ```

2. **Prepare the dataset** (download, convert, clean) — see `commands.txt`
   section 3.

3. **Create the HDFS directory structure and upload data** — see
   `commands.txt` sections 2 and 4.

4. **Run the MapReduce jobs in order** — see `commands.txt` section 5.
   Jobs are run from `C:\taxi_project\`, where all mapper/reducer scripts
   and `taxi_zone_lookup.csv` are located. Note: Job 10 (Stage 2 of the
   multi-stage requirement) must run after Job 4, since it reads Job 4's
   HDFS output directory as its input.

5. **View results** and **run the performance comparison** — see
   `commands.txt` sections 6-7.

## Data Cleaning Summary

7 categories of invalid records were identified and quantified (not
silently dropped) before removal:

| Issue | Jan 2024 | Feb 2024 |
|---|---|---|
| Missing key fields | 4.73% | 6.17% |
| Invalid passenger count | 5.79% | 7.31% |
| Zero/negative distance | 2.04% | 2.27% |
| Invalid fares | 1.29% | 1.38% |
| Invalid timestamps | 0.03% | 0.03% |
| Duplicates | 0.00% | 0.00% |
| Impossible durations | 0.09% | 0.08% |
| **Total removed** | **8.19%** | **9.63%** |

Overall: 532,278 of 5,972,150 records removed (8.91%), leaving 5,439,872
clean records used for all analytical MapReduce jobs.

## Author / Submission Notes

See the accompanying report for full analytical findings, YARN evidence
screenshots, visualizations, and the Pandas-vs-MapReduce performance
comparison discussion.
