"""Regenerate the tutorial's data files from the OpenAQ public S3 archive.

Instructors only — students never need to run this; the CSVs it produces are
committed in ``data/``. Requires ``pip install pandas boto3``. No API key and
no database: the archive bucket is public and anonymous::

    s3://openaq-data-archive/records/csv.gz/locationid={id}/year={Y}/month={M}/
        location-{id}-{YYYYMMDD}.csv.gz

Adapted from the AQ agent project's side-project/src/openaq_s3_fetch.py.

Outputs (written to ``--data-dir``, default ../data):

* lagos_pm25_recent.csv — the primary teaching file: hourly PM2.5 at Oshodi Bus
  Terminal, Lagos (AirGradient low-cost sensor), 12 months Jul 2025 – Jun 2026
* abuja_pm25_2024.csv — hourly PM2.5, Abuja US embassy (AirNow reference
  monitor), calendar 2024
* lagos_sites_recent.csv — hourly PM2.5 for five contrasting Lagos-area sites
  over the same 12-month window, long format (datetime, site_name, pm25_value)
* lagos_us_consulate_2023_2024.csv — the Lagos reference monitor, kept AS IS
  including its large outages, for the "real monitoring has gaps" exercise
  (this is why the primary Lagos file is a low-cost sensor: the reference
  monitor was down for most of 2023–2024)
* oshodi_raw_january.csv — one month exactly as archived: every parameter the
  sensor reports, raw timestamp strings, zeros and all, for the data-cleaning
  exercise
* stations.csv — one row of metadata per site

Each file ends with a QC summary printed to stdout: row count, date span,
completeness against the expected hourly grid, and counts of the rows removed.
"""

from __future__ import annotations

import argparse
import gzip
import io
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from pathlib import Path

import boto3
import pandas as pd
from botocore import UNSIGNED
from botocore.config import Config as BotoConfig

BUCKET = "openaq-data-archive"
PREFIX = "records/csv.gz"
KEY_DATE_RE = re.compile(r"location-\d+-(\d{8})\.csv\.gz$")

# A full 12-month window shared by the low-cost Lagos sites (Harmattan included).
WINDOW_START = date(2025, 7, 1)
WINDOW_END = date(2026, 6, 30)

PRIMARY = dict(location_id=5038498, site_name="Oshodi Bus Terminal", site_type="transport hub",
               out="lagos_pm25_recent.csv")

# Contrasting surroundings around Lagos (site_type is our own label, not OpenAQ's).
RECENT_SITES = [
    dict(location_id=5038498, site_name="Oshodi Bus Terminal", site_type="transport hub"),
    dict(location_id=3400895, site_name="University of Lagos / Makoko", site_type="university"),
    dict(location_id=4903422, site_name="Dolphin Estate (Ikoyi)", site_type="residential"),
    dict(location_id=4605121, site_name="M.K.O. Abiola Gardens", site_type="urban park"),
    dict(location_id=4986946, site_name="Arepo (Ogun State)", site_type="peri-urban"),
]

ABUJA = dict(location_id=220715, site_name="Abuja (US Embassy)", site_type="reference",
             year=2024, out="abuja_pm25_2024.csv")

# The Lagos reference monitor, preserved with its outages (teaching material).
LAGOS_REF = dict(location_id=404479, site_name="Lagos (US Consulate)", site_type="reference",
                 start=date(2023, 1, 1), end=date(2024, 12, 31),
                 out="lagos_us_consulate_2023_2024.csv")

RAW_SAMPLE = dict(location_id=5038498, year=2026, month=1, out="oshodi_raw_january.csv")


def s3_client():
    return boto3.client(
        "s3",
        region_name="us-east-1",
        config=BotoConfig(
            signature_version=UNSIGNED,
            connect_timeout=20,
            read_timeout=40,
            retries={"max_attempts": 3},
            max_pool_connections=32,
        ),
    )


def month_range(start: date, end: date) -> list[tuple[int, int]]:
    out, (y, m) = [], (start.year, start.month)
    while (y, m) <= (end.year, end.month):
        out.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


def list_keys(client, location_id: int, start: date, end: date) -> list[str]:
    keys = []
    paginator = client.get_paginator("list_objects_v2")
    for year, month in month_range(start, end):
        prefix = f"{PREFIX}/locationid={location_id}/year={year}/month={month:02d}/"
        for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                m = KEY_DATE_RE.search(obj["Key"])
                if not m:
                    continue
                d = datetime.strptime(m.group(1), "%Y%m%d").date()
                if start <= d <= end:
                    keys.append(obj["Key"])
    return keys


def download_key(client, key: str, cache_dir: Path) -> bytes:
    dest = cache_dir / key
    if dest.exists():
        return dest.read_bytes()
    raw = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    return raw


def fetch_raw_frames(client, location_id: int, start: date, end: date,
                     cache_dir: Path) -> pd.DataFrame:
    """All archived rows for one location, columns as stored (strings intact)."""
    keys = list_keys(client, location_id, start, end)
    frames = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(download_key, client, k, cache_dir): k for k in keys}
        for fut in as_completed(futures):
            text = gzip.decompress(fut.result()).decode("utf-8", "replace")
            df = pd.read_csv(io.StringIO(text), dtype=str)
            if not df.empty:
                frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def tidy_pm25(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Archive rows -> clean hourly PM2.5 (datetime UTC, pm25_value).

    Returns (clean_df, qc_counts). Cleaning: keep parameter == pm25, coerce
    types, drop unparseable/missing, drop negative values (missing-data codes),
    average duplicate timestamps, floor to the hour.
    """
    qc = dict(rows_archived=len(raw))
    df = raw[raw["parameter"].str.lower() == "pm25"].copy()
    qc["rows_pm25"] = len(df)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce", format="ISO8601")
    df["pm25_value"] = pd.to_numeric(df["value"], errors="coerce")
    n = len(df)
    df = df.dropna(subset=["datetime", "pm25_value"])
    qc["dropped_unparseable"] = n - len(df)
    n = len(df)
    df = df[df["pm25_value"] >= 0]
    qc["dropped_negative"] = n - len(df)
    df["datetime"] = df["datetime"].dt.floor("h")
    n = len(df)
    df = df.groupby("datetime", as_index=False)["pm25_value"].mean()
    qc["collapsed_duplicates"] = n - len(df)
    df["pm25_value"] = df["pm25_value"].round(2)
    return df.sort_values("datetime").reset_index(drop=True), qc


def qc_report(name: str, df: pd.DataFrame, qc: dict) -> None:
    span = (df["datetime"].min(), df["datetime"].max())
    expected = int((span[1] - span[0]).total_seconds() // 3600) + 1 if len(df) else 0
    completeness = 100.0 * len(df) / expected if expected else 0.0
    print(f"\n=== {name} ===")
    for k, v in qc.items():
        print(f"  {k}: {v}")
    print(f"  clean rows: {len(df)}")
    if len(df):
        print(f"  span: {span[0]} -> {span[1]}")
        print(f"  completeness vs hourly grid: {completeness:.1f}%")
        print(f"  value stats: min={df['pm25_value'].min():.1f} "
              f"mean={df['pm25_value'].mean():.1f} max={df['pm25_value'].max():.1f}")


def site_coords(raw: pd.DataFrame) -> tuple[float, float, str]:
    """lat, lon, provider taken from the archive rows themselves."""
    first = raw.iloc[0]
    lat = float(first.get("lat", "nan"))
    lon = float(first.get("lon", "nan"))
    provider = str(first.get("provider", "")) if "provider" in raw.columns else ""
    return lat, lon, provider


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=here.parent / "data")
    ap.add_argument("--cache-dir", type=Path, default=here / ".s3_cache")
    args = ap.parse_args()
    args.data_dir.mkdir(parents=True, exist_ok=True)
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    client = s3_client()
    stations = []

    # --- Low-cost Lagos sites over the shared window (includes the primary) ---
    frames, raw_by_site = [], {}
    for site in RECENT_SITES:
        raw = fetch_raw_frames(client, site["location_id"], WINDOW_START, WINDOW_END,
                               args.cache_dir)
        if raw.empty:
            print(f"!! no archive data for {site['site_name']}")
            continue
        raw_by_site[site["site_name"]] = raw
        clean, qc = tidy_pm25(raw)
        clean.insert(1, "site_name", site["site_name"])
        frames.append(clean)
        qc_report(f"lagos_sites_recent.csv :: {site['site_name']}", clean, qc)
        lat, lon, provider = site_coords(raw)
        stations.append(dict(site_name=site["site_name"], city="Lagos",
                             latitude=lat, longitude=lon,
                             provider=provider or "AirGradient",
                             site_type=site["site_type"],
                             location_id=site["location_id"],
                             data_file="lagos_sites_recent.csv"))
    if frames:
        recent = pd.concat(frames, ignore_index=True).sort_values(["site_name", "datetime"])
        recent.to_csv(args.data_dir / "lagos_sites_recent.csv", index=False)

    # --- Primary teaching file: Oshodi alone, two columns ---
    primary_rows = recent[recent["site_name"] == PRIMARY["site_name"]]
    primary_rows[["datetime", "pm25_value"]].to_csv(args.data_dir / PRIMARY["out"], index=False)
    print(f"\n=== {PRIMARY['out']} === (Oshodi columns datetime,pm25_value; QC as above)")

    # --- Abuja reference year ---
    raw = fetch_raw_frames(client, ABUJA["location_id"],
                           date(ABUJA["year"], 1, 1), date(ABUJA["year"], 12, 31),
                           args.cache_dir)
    clean, qc = tidy_pm25(raw)
    clean.to_csv(args.data_dir / ABUJA["out"], index=False)
    qc_report(ABUJA["out"], clean, qc)
    lat, lon, _ = site_coords(raw)
    stations.append(dict(site_name=ABUJA["site_name"], city="Abuja",
                         latitude=lat, longitude=lon,
                         provider="AirNow (US Dept. of State)",
                         site_type=ABUJA["site_type"], location_id=ABUJA["location_id"],
                         data_file=ABUJA["out"]))

    # --- Lagos reference monitor, gaps preserved ---
    raw = fetch_raw_frames(client, LAGOS_REF["location_id"], LAGOS_REF["start"],
                           LAGOS_REF["end"], args.cache_dir)
    clean, qc = tidy_pm25(raw)
    clean.to_csv(args.data_dir / LAGOS_REF["out"], index=False)
    qc_report(LAGOS_REF["out"] + " (gaps preserved on purpose)", clean, qc)
    lat, lon, _ = site_coords(raw)
    stations.append(dict(site_name=LAGOS_REF["site_name"], city="Lagos",
                         latitude=lat, longitude=lon,
                         provider="AirNow (US Dept. of State)",
                         site_type=LAGOS_REF["site_type"], location_id=LAGOS_REF["location_id"],
                         data_file=LAGOS_REF["out"]))

    # --- Raw month, exactly as archived (column subset + stable ordering only) ---
    raw = fetch_raw_frames(client, RAW_SAMPLE["location_id"],
                           date(RAW_SAMPLE["year"], RAW_SAMPLE["month"], 1),
                           date(RAW_SAMPLE["year"], RAW_SAMPLE["month"], 31),
                           args.cache_dir)
    keep = [c for c in ["location", "datetime", "parameter", "units", "value"] if c in raw.columns]
    raw_out = raw[keep].sort_values(["datetime", "parameter"])
    raw_out.to_csv(args.data_dir / RAW_SAMPLE["out"], index=False)
    values = pd.to_numeric(raw_out["value"], errors="coerce")
    print(f"\n=== {RAW_SAMPLE['out']} (as archived) ===")
    print(f"  rows: {len(raw_out)}  parameters: {sorted(raw_out['parameter'].unique().tolist())}")
    print(f"  negatives: {(values < 0).sum()}  blank/non-numeric: {values.isna().sum()}  "
          f"zeros: {(values == 0).sum()}  "
          f"duplicate (datetime,parameter): {raw_out.duplicated(['datetime', 'parameter']).sum()}")

    pd.DataFrame(stations).to_csv(args.data_dir / "stations.csv", index=False)
    print(f"\nWrote {len(stations)} rows to stations.csv")
    print("Done.")


if __name__ == "__main__":
    main()
