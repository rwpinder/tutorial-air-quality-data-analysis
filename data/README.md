# Course data

Real hourly PM2.5 measurements from Nigeria, fetched from the
[OpenAQ](https://openaq.org) public data archive by
[`../scripts/prepare_data.py`](../scripts/prepare_data.py). Values are µg/m³;
timestamps are **UTC** (ISO 8601 with offset) — the notebooks teach converting to
local West Africa Time (`Africa/Lagos`, UTC+1, no daylight saving).

Some files are deliberately imperfect: the course teaches completeness checks and
cleaning on real problems, not manufactured ones.

## Files

### `lagos_pm25_recent.csv` — the primary teaching dataset
Hourly PM2.5 at **Oshodi Bus Terminal, Lagos** (AirGradient low-cost optical
sensor; OpenAQ location 5038498), 11 July 2025 – 30 June 2026.
Columns: `datetime`, `pm25_value`. 7,297 rows, ~86% complete (45 empty days —
left in on purpose). Mean ≈ 44 µg/m³; diurnal peak at 08:00 local; worst month
January (Harmattan).

### `abuja_pm25_2024.csv` — a reference-grade year
Hourly PM2.5 at the **US Embassy, Abuja** (US Department of State / AirNow BAM
reference monitor; OpenAQ location 220715), calendar 2024 (record ends 20 Dec).
Columns: `datetime`, `pm25_value`. 7,283 rows, ~86% complete. Shows an extreme
Harmattan: January mean ≈ 117 µg/m³ vs rainy-season months ≈ 20.

### `lagos_sites_recent.csv` — five contrasting Lagos-area sites
Long format: `datetime`, `site_name`, `pm25_value`; same 12-month window as the
primary file. Sites (all low-cost sensors via OpenAQ): Oshodi Bus Terminal
(transport hub), University of Lagos / Makoko (campus, lagoon-side),
Dolphin Estate Ikoyi (residential), M.K.O. Abiola Gardens (urban park),
Arepo Ogun State (peri-urban). Per-site completeness 58–93%; M.K.O. Abiola
Gardens starts 13 Aug 2025.

### `lagos_us_consulate_2023_2024.csv` — the gaps exercise
The **Lagos US Consulate** reference monitor (OpenAQ location 404479), 2023–2024,
**with its outages preserved** — including a 203-day gap in 2024. Used in
notebook 3 to teach "check completeness before trusting a record" (and it's why
the primary Lagos file is a low-cost sensor instead).

### `oshodi_raw_january.csv` — the cleaning exercise
One month (January 2026) from the Oshodi sensor **exactly as archived**: five
parameters interleaved (`pm25`, `pm1`, `relativehumidity`, `temperature`,
`um003`), text timestamps with a `+01:00` offset, text values. Columns:
`location`, `datetime`, `parameter`, `units`, `value` (3,490 rows).

### `stations.csv`
One row of metadata per site: `site_name`, `city`, `latitude`, `longitude`,
`provider`, `site_type`, `location_id` (OpenAQ), `data_file`.

## Provenance, licence, attribution

* All measurements were aggregated and republished by **OpenAQ**
  (https://openaq.org) and fetched from their public S3 archive
  (`s3://openaq-data-archive`, anonymous access). OpenAQ data carries the licence
  of its originating provider — see https://docs.openaq.org/about/licenses for the
  authoritative terms per source.
* Originating providers: **U.S. Department of State / AirNow** (Abuja embassy and
  Lagos consulate reference monitors) and the **AirGradient** open network
  (low-cost sites).
* Suggested citation line for student reports: *“PM2.5 data via OpenAQ
  (openaq.org), original measurements by the U.S. Department of State and the
  AirGradient network.”*
* Low-cost optical sensors can drift and differ from reference monitors;
  treat absolute values from those sites accordingly.

To regenerate everything from the archive: `pip install pandas boto3`, then
`python ../scripts/prepare_data.py` (it prints a QC summary for every file).
