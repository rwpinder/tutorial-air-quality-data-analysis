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

### `accra_network_feb2025.csv` and `accra_network_aug2025.csv` — the sensor network
Two contrasting months across the **Accra metropolitan network**, Ghana, used by
notebooks 7 and 8. Long format: `datetime`, `site_name`, `pm25_value`.

| | February 2025 (Harmattan) | August 2025 (wet season) |
|---|---|---|
| Sites | 17 | 20 |
| Rows | 9,241 | 12,703 |
| Completeness screen | ≥ 70% of 672 hours | ≥ 70% of 744 hours |
| Mean PM2.5 | 32.6 µg/m³ | 22.4 µg/m³ |
| Range | 7.3 – 140.8 | 1.9 – 134.5 |

The same 70% bar applies to both months. Fifteen sites appear in both, which is
the set notebook 8 uses for its like-for-like seasonal comparison. Accra is on
**UTC+0** (`Africa/Accra`, no daylight saving), so UTC and local time coincide —
unlike the Lagos files above, which are UTC+1.

**Why Accra and not Lagos for these two notebooks.** Lagos was tried first and
abandoned. Its network has a much lower sensor density, and in August 2025 its
AirQo sensors lost most of their hour-to-hour coherence (median lag-1
autocorrelation 0.24, against 0.66 in February), which made a seasonal comparison
of spatial correlation unreliable. Accra's equivalent figures are 0.79 and 0.77 —
healthy in both months — so a seasonal difference there can be read as
atmosphere rather than instrument drift.

**Two deliberate quirks, both used for teaching.**

* *A colocation pair.* `Afri-SET CC1` and `Afri-SET F1` are two PurpleAir units
  **5 m apart** at the Afri-SET sensor-evaluation facility. They correlate at
  r = 0.99 (February) and 1.00 (August) — the reference for what healthy
  instruments in identical air look like. Notebook 7 uses them as a yardstick.
* *One broken sensor, left in on purpose.* `Osu Presby School` passed the
  completeness screen and has an unremarkable mean and range, but its August
  series has a lag-1 autocorrelation of 0.06 and correlates with its 1.1 km
  neighbour at r = 0.01. It is a real fault that only the *time ordering*
  exposes, and notebook 7 walks students through finding it. Removing it moves
  the August regional background by under 3%.

### `accra_network_sites.csv`
One row per network site: `site_name`, `latitude`, `longitude`, `source`,
`completeness_feb2025`, `completeness_aug2025`, `in_feb2025`, `in_aug2025`.
22 sites total — 16 via OpenAQ (the Clarity network), 5 PurpleAir, 1 AirQo.

### `accra_basemap.png` and `accra_basemap.csv`
A pre-rendered map of metropolitan Accra and the longitude/latitude rectangle it
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
* **The two `accra_network_*` files come from a different pipeline.** They were
  assembled from the AQ agent measurement database by
  [`../scripts/prepare_network_data.py`](../scripts/prepare_network_data.py),
  not from the OpenAQ S3 archive, so that PurpleAir and AirQo sites could sit
  alongside the OpenAQ ones. Values are the database's QA-passing hours (`valid`
  and `minor_concern` under its four-tier screen), averaged to the hour.
  Originating providers for these two files: the **Clarity** network and Ghana
  EPA sites via OpenAQ, **PurpleAir** (including the Afri-SET evaluation
  facility), and **AirQo**. Suggested attribution: *“PM2.5 data via OpenAQ
  (openaq.org), PurpleAir and AirQo.”* Confirm each provider's current terms
  before reusing these two files outside this course.
* Suggested citation line for student reports: *“PM2.5 data via OpenAQ
  (openaq.org), original measurements by the U.S. Department of State and the
  AirGradient network.”*
* Low-cost optical sensors can drift and differ from reference monitors;
  treat absolute values from those sites accordingly.

To regenerate the archive-sourced files: `pip install pandas boto3`, then
`python ../scripts/prepare_data.py` (it prints a QC summary for every file).

To regenerate the two Accra network files and the basemap you additionally need
access to the AQ agent database: `python ../scripts/prepare_network_data.py` (see
its `--help`; `--print-sql` shows the two queries if you'd rather run them
yourself).
