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

### `lagos_network_feb2025.csv` and `lagos_network_aug2025.csv` — the sensor network
Two contrasting months across the **Lagos metropolitan network**, used by
notebooks 7 and 8. Long format: `datetime`, `site_name`, `pm25_value`.

| | February 2025 (Harmattan) | August 2025 (wet season) |
|---|---|---|
| Sites | 12 | 11 |
| Rows | 6,972 | 5,513 |
| Completeness screen | ≥ 75% of 672 hours | ≥ 60% of 744 hours |
| Mean PM2.5 | 30.7 µg/m³ | 28.0 µg/m³ |
| Range | 10.2 – 149.6 | 4.5 – 126.0 |

Seven sites appear in both months, which is the set notebook 8 uses for its
like-for-like seasonal comparison.

**Why August's screen is lower.** August 2025 was a poor month for this network:
at a 75% bar only five sensors qualify — too few to interpolate or to define a
regional background. Dropping to 60% yields eleven. The threshold is stated in
the notebooks rather than buried, because choosing it *is* part of the analysis.

**A known data-quality problem, kept on purpose.** In August the AirQo sensors
show hour-to-hour autocorrelation near 0.24, against ~0.66 in February, while the
one non-AirQo sensor in the August set holds 0.71. The two colocated UNILAG
sensors (110 m apart) agree on daily means (r ≈ 0.78) but not hourly (r ≈ 0.31).
That is instrument noise, not weather, and notebook 7 walks students through
diagnosing it. The seasonal findings in notebooks 7 and 8 were checked against it
and survive: they live in the daily and >8 h signals, which the noise does not
reach.

### `lagos_network_sites.csv`
One row per network site: `site_name`, `latitude`, `longitude`, `source`,
`completeness_feb2025`, `completeness_aug2025`, `in_feb2025`, `in_aug2025`.
16 sites total — 14 AirQo, 1 PurpleAir (Lekki/LASEPA, February only) and
1 OpenAQ/AirGradient (Oshodi Bus Terminal, August only).

### `lagos_basemap.png` and `lagos_basemap.csv`
A pre-rendered map of metropolitan Lagos and the longitude/latitude rectangle it
covers (`west`, `east`, `south`, `north`). Rendered once by
[`../scripts/prepare_network_data.py`](../scripts/prepare_network_data.py) so the
notebooks need no mapping library and no network access at run time — they draw
it with `plt.imshow(image, extent=[...])` and scatter sensor coordinates on top.
Basemap tiles © [Esri](https://www.esri.com) (WorldGrayCanvas; Esri, DeLorme,
NAVTEQ).

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
* **The two `lagos_network_*` files come from a different pipeline.** They were
  assembled from the AQ agent measurement database by
  [`../scripts/prepare_network_data.py`](../scripts/prepare_network_data.py), not
  from the OpenAQ S3 archive, because the Lagos network in early 2025 is
  overwhelmingly **AirQo** sensors and AirQo measurements are not carried in that
  archive. They were collected from the AirQo Analytics API
  (https://analytics.airqo.net), with one PurpleAir site and one
  OpenAQ/AirGradient site alongside. Values are the database's QA-passing hours
  (`valid` and `minor_concern` under its four-tier screen), averaged to the hour.
  Suggested attribution: *“PM2.5 data from the AirQo network (airqo.net), with
  PurpleAir and AirGradient sites via OpenAQ.”* Confirm AirQo's current terms for
  redistribution before reusing these two files outside this course.
* Suggested citation line for student reports: *“PM2.5 data via OpenAQ
  (openaq.org), original measurements by the U.S. Department of State and the
  AirGradient network.”*
* Low-cost optical sensors can drift and differ from reference monitors;
  treat absolute values from those sites accordingly.

To regenerate the archive-sourced files: `pip install pandas boto3`, then
`python ../scripts/prepare_data.py` (it prints a QC summary for every file).

To regenerate the two network files and the basemap you additionally need access
to the AQ agent database: `python ../scripts/prepare_network_data.py` (see its
`--help`; `--print-sql` shows the two queries if you'd rather run them yourself).
