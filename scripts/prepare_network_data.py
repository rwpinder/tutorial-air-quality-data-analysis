"""Regenerate the Lagos sensor-network datasets used by notebooks 06 and 07.

Instructors only — students never run this; the CSVs it produces are committed
in ``data/``. Unlike ``prepare_data.py`` (which pulls single sites from the
anonymous OpenAQ S3 archive), this script needs the **AQ agent measurement
database**, because the Lagos network in early 2025 is almost entirely AirQo
sensors and AirQo data does not reach the OpenAQ S3 archive.

Two windows, screened independently:

* ``lagos_network_feb2025.csv`` — February 2025 (Harmattan), sensors reporting
  at least **75%** of the month's 672 hours;
* ``lagos_network_aug2025.csv`` — August 2025 (wet season), sensors reporting at
  least **60%** of the month's 744 hours. The bar is lower here on purpose:
  August 2025 was a gappy month for the Lagos network and a 75% screen leaves
  only 5 sensors — too few for a spatial map. This is a real limitation of the
  data, and notebook 06 says so out loud rather than hiding it.

Completeness is measured on QA-passing hours only (``valid`` +
``minor_concern`` — the same four-tier QA/QC the agent applies elsewhere), so a
sensor that reported constantly but was flagged as suspect does not qualify.

Outputs (written to ``--data-dir``, default ../data):

* ``lagos_network_feb2025.csv`` — datetime (UTC), site_name, pm25_value
* ``lagos_network_aug2025.csv`` — same columns
* ``lagos_network_sites.csv``   — one row per site: coordinates, source,
  completeness in each window, and which windows it qualified for
* ``lagos_basemap.png``         — pre-rendered Esri WorldGrayCanvas backdrop
* ``lagos_basemap.csv``         — that image's extent (west, east, south, north)

The basemap is rendered here, once, so the notebooks need no mapping library
and no network access at run time: they just ``imshow`` the committed PNG.

Usage
-----
Straight from the database (needs ``pip install psycopg2-binary``)::

    DATABASE_URL=postgresql://... python scripts/prepare_network_data.py

From a CSV dump of the query below (no database driver needed) — this is the
path to use when the database is only reachable over SSH::

    python scripts/prepare_network_data.py --from-dump hourly.csv --sites-dump sites.csv

Print the two SQL statements and exit, to run them yourself::

    python scripts/prepare_network_data.py --print-sql

Re-rendering the basemap needs ``pip install contextily``; pass
``--skip-basemap`` to leave the committed PNG alone.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

# Lagos metropolitan bounding box (west, south, east, north).
BBOX = (3.05, 6.30, 3.70, 6.80)

WINDOWS = {
    "feb2025": dict(start="2025-02-01", end="2025-03-01", hours=672, min_pct=75,
                    out="lagos_network_feb2025.csv", label="February 2025"),
    "aug2025": dict(start="2025-08-01", end="2025-09-01", hours=744, min_pct=60,
                    out="lagos_network_aug2025.csv", label="August 2025"),
}

# Hourly QA-passing PM2.5 for every Lagos-area sensor across both windows.
SQL_HOURLY = """
COPY (
  SELECT m.sensor_id, date_trunc('hour', m.datetime) AS dt,
         round(avg(m.pm25_value)::numeric, 2) AS pm25
  FROM measurements m JOIN sensors s ON s.id = m.sensor_id
  WHERE s.geom && ST_MakeEnvelope(3.05, 6.30, 3.70, 6.80, 4326)
    AND m.pm25_value IS NOT NULL
    AND m.qa_flag IN ('valid','minor_concern')
    AND ( (m.datetime >= '2025-02-01' AND m.datetime < '2025-03-01')
       OR (m.datetime >= '2025-08-01' AND m.datetime < '2025-09-01') )
  GROUP BY 1,2
) TO STDOUT WITH CSV HEADER;
"""

SQL_SITES = """
COPY (
  SELECT s.id AS sensor_id, s.source, s.name,
         ST_Y(s.geom) AS latitude, ST_X(s.geom) AS longitude
  FROM sensors s
  WHERE s.geom && ST_MakeEnvelope(3.05, 6.30, 3.70, 6.80, 4326)
) TO STDOUT WITH CSV HEADER;
"""

# Database sensor names carry device serials and repeated ", Lagos, Nigeria"
# suffixes. Students should see the neighbourhood, so each qualifying sensor is
# given a short, unique, human name here. The two UNILAG rows are a genuine
# colocation pair ~110 m apart — deliberately kept distinct, because notebook 06
# uses them to show what a near-perfect nearest-neighbour correlation looks like.
SITE_NAMES = {
    216: "Oshodi Bus Terminal",
    7403: "Lekki (LASEPA)",
    7473: "NIMET Oshodi",
    7474: "Eti-Osa",
    7476: "Apapa Port",
    7477: "Agege",
    7479: "Araromi",
    7480: "Ikeja Hospital Road",
    7483: "Mushin",
    7484: "UNILAG Colocation B",
    7485: "Ikotun",
    7487: "UNILAG Colocation A",
    7489: "Banana Island",
    7491: "Oshodi",
    7493: "Egbeda",
    7500: "Ifako-Ijaiye",
}


def load_from_db(url: str) -> "tuple[pd.DataFrame, pd.DataFrame]":
    """Run both queries against the AQ agent database."""
    try:
        import psycopg2  # noqa: F401
    except ImportError:
        sys.exit("psycopg2 not installed. `pip install psycopg2-binary`, or use "
                 "--from-dump with a CSV produced by --print-sql.")
    import psycopg2

    def copy_to_frame(conn, sql: str) -> pd.DataFrame:
        import io
        buf = io.StringIO()
        with conn.cursor() as cur:
            cur.copy_expert(sql.strip(), buf)
        buf.seek(0)
        return pd.read_csv(buf)

    with psycopg2.connect(url) as conn:
        return copy_to_frame(conn, SQL_HOURLY), copy_to_frame(conn, SQL_SITES)


def screen(hourly: pd.DataFrame, key: str) -> "tuple[list[int], pd.Series]":
    """Sensor ids meeting the window's completeness bar, plus every sensor's %."""
    w = WINDOWS[key]
    win = hourly[(hourly["dt"] >= w["start"]) & (hourly["dt"] < w["end"])]
    pct = win.groupby("sensor_id").size() / w["hours"] * 100
    passing = sorted(pct[pct >= w["min_pct"]].index)
    unnamed = [s for s in passing if s not in SITE_NAMES]
    if unnamed:
        raise SystemExit(
            f"{w['label']}: sensors {unnamed} passed screening but have no entry "
            f"in SITE_NAMES. Add short names for them and re-run."
        )
    return passing, pct


def write_window(hourly: pd.DataFrame, key: str, passing: "list[int]",
                 data_dir: Path) -> pd.DataFrame:
    w = WINDOWS[key]
    win = hourly[(hourly["dt"] >= w["start"]) & (hourly["dt"] < w["end"])
                 & (hourly["sensor_id"].isin(passing))].copy()
    win["site_name"] = win["sensor_id"].map(SITE_NAMES)
    out = (win.rename(columns={"dt": "datetime", "pm25": "pm25_value"})
              [["datetime", "site_name", "pm25_value"]]
              .sort_values(["site_name", "datetime"]))
    out.to_csv(data_dir / w["out"], index=False)

    span = (out["datetime"].min(), out["datetime"].max())
    print(f"\n=== {w['out']} ===")
    print(f"  window: {w['label']}  (screen: >= {w['min_pct']}% of {w['hours']} h, QA-passing)")
    print(f"  sites: {out['site_name'].nunique()}   rows: {len(out)}")
    print(f"  span: {span[0]} -> {span[1]}")
    print(f"  pm25: min={out['pm25_value'].min():.1f} "
          f"mean={out['pm25_value'].mean():.1f} max={out['pm25_value'].max():.1f}")
    per_site = out.groupby("site_name").size().sort_values()
    print(f"  hours per site: {per_site.min()} (fewest, {per_site.idxmin()}) .. "
          f"{per_site.max()} (most, {per_site.idxmax()})")
    return out


def write_sites(sites: pd.DataFrame, passing: "dict[str, list[int]]",
                pcts: "dict[str, pd.Series]", data_dir: Path) -> pd.DataFrame:
    keep = sorted(set(passing["feb2025"]) | set(passing["aug2025"]))
    rows = []
    for sid in keep:
        meta = sites[sites["sensor_id"] == sid]
        if meta.empty:
            raise SystemExit(f"sensor {sid} passed screening but is missing from the sites dump")
        meta = meta.iloc[0]
        rows.append(dict(
            site_name=SITE_NAMES[sid],
            latitude=round(float(meta["latitude"]), 6),
            longitude=round(float(meta["longitude"]), 6),
            source=meta["source"],
            completeness_feb2025=round(float(pcts["feb2025"].get(sid, 0.0)), 1),
            completeness_aug2025=round(float(pcts["aug2025"].get(sid, 0.0)), 1),
            in_feb2025=sid in passing["feb2025"],
            in_aug2025=sid in passing["aug2025"],
        ))
    out = pd.DataFrame(rows).sort_values("site_name").reset_index(drop=True)
    out.to_csv(data_dir / "lagos_network_sites.csv", index=False)
    print(f"\n=== lagos_network_sites.csv ===")
    print(f"  {len(out)} sites  ({out['in_feb2025'].sum()} in Feb, "
          f"{out['in_aug2025'].sum()} in Aug, "
          f"{(out['in_feb2025'] & out['in_aug2025']).sum()} in both)")
    print(f"  lat {out['latitude'].min():.4f}..{out['latitude'].max():.4f}   "
          f"lon {out['longitude'].min():.4f}..{out['longitude'].max():.4f}")
    return out


def render_basemap(sites: pd.DataFrame, data_dir: Path, pad: float = 0.035) -> None:
    """Fetch an OpenStreetMap backdrop once and commit it as a PNG + extent.

    Rendering here rather than in the notebooks keeps the student experience
    dependency-free and offline-safe: no contextily, no tile fetch, and the
    same picture for everyone, every run.
    """
    try:
        import contextily as cx
    except ImportError:
        sys.exit("contextily not installed. `pip install contextily`, or pass --skip-basemap.")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    west = sites["longitude"].min() - pad
    east = sites["longitude"].max() + pad
    south = sites["latitude"].min() - pad
    north = sites["latitude"].max() + pad

    # Esri's WorldGrayCanvas, deliberately. The two obvious alternatives both
    # fail *silently*, returning a perfectly valid PNG of an error message:
    # OSM's volunteer servers refuse scripted clients ("403 Access blocked")
    # and CartoDB now watermarks unkeyed tiles ("API KEY REQUIRED"). Always
    # eyeball a re-rendered basemap. WorldGrayCanvas is also the right
    # cartography here — a pale, near-monochrome backdrop that leaves the
    # colour axis entirely to the data drawn on top of it.
    img, ext = cx.bounds2img(west, south, east, north, ll=True,
                             source=cx.providers.Esri.WorldGrayCanvas, zoom=12)
    # bounds2img returns Web-Mercator extent; warp to plain lon/lat so the
    # notebooks can plot sensor coordinates directly with no projection code.
    img, ext = cx.warp_tiles(img, ext, t_crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img, extent=ext)
    ax.set_xlim(west, east)
    ax.set_ylim(south, north)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(data_dir / "lagos_basemap.png", dpi=140, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    pd.DataFrame([dict(west=west, east=east, south=south, north=north)]).round(6).to_csv(
        data_dir / "lagos_basemap.csv", index=False)
    print(f"\n=== lagos_basemap.png ===")
    print(f"  extent: lon {west:.4f}..{east:.4f}  lat {south:.4f}..{north:.4f}")
    print("  attribution: Tiles (C) Esri — Esri, DeLorme, NAVTEQ")


def main() -> None:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", type=Path, default=here.parent / "data")
    ap.add_argument("--from-dump", type=Path, help="CSV dump of SQL_HOURLY")
    ap.add_argument("--sites-dump", type=Path, help="CSV dump of SQL_SITES")
    ap.add_argument("--print-sql", action="store_true")
    ap.add_argument("--skip-basemap", action="store_true")
    args = ap.parse_args()

    if args.print_sql:
        print("-- hourly measurements --")
        print(SQL_HOURLY.strip())
        print("\n-- site metadata --")
        print(SQL_SITES.strip())
        return

    if args.from_dump:
        if not args.sites_dump:
            sys.exit("--from-dump also needs --sites-dump")
        hourly = pd.read_csv(args.from_dump)
        sites = pd.read_csv(args.sites_dump)
    else:
        url = os.environ.get("DATABASE_URL")
        if not url:
            sys.exit("Set DATABASE_URL, or use --from-dump/--sites-dump. "
                     "See --print-sql for the queries.")
        hourly, sites = load_from_db(url)

    hourly["dt"] = pd.to_datetime(hourly["dt"], utc=True)
    args.data_dir.mkdir(parents=True, exist_ok=True)

    passing, pcts = {}, {}
    for key in WINDOWS:
        passing[key], pcts[key] = screen(hourly, key)
    for key in WINDOWS:
        write_window(hourly, key, passing[key], args.data_dir)
    site_table = write_sites(sites, passing, pcts, args.data_dir)

    if not args.skip_basemap:
        render_basemap(site_table, args.data_dir)
    print("\nDone.")


if __name__ == "__main__":
    main()
