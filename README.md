# Air Quality Data Analysis with Python

An interactive, beginner-friendly course for **air-quality professionals who are new
to programming**. Across five hands-on notebooks (plus a bonus), you'll go from your
first line of Python to building the two signature charts of air-quality analysis —
the **diurnal profile** and the **monthly average** — using a real year of PM2.5
measurements from Lagos and Abuja, Nigeria.

No installation needed: everything runs in your browser with **Google Colab**.

## The notebooks

| # | Notebook | You'll learn | ⏱️ | Open |
|---|----------|--------------|----|------|
| 1 | Welcome & Python Basics | Colab, variables, f-strings, if/else, WHO guidelines | 45 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/01_welcome_python_basics.ipynb) |
| 2 | Data Structures | Lists, indexing, loops, dicts — one real day of Lagos data | 50 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/02_data_structures.ipynb) |
| 3 | pandas & Real Data | DataFrames, datetimes & time zones, resampling, cleaning raw sensor files | 60 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/03_pandas_real_data.ipynb) |
| 4 | First Plots | Time-series charts, house style, titles that carry the finding | 50 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/04_first_plots.ipynb) |
| 5 | Diurnal & Monthly Patterns | `groupby`, the two signature charts, Harmattan, five-site comparison | 75 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/05_diurnal_and_monthly.ipynb) |
| 6 | Bonus: the OpenAQ API | Live data, JSON, API keys kept secret | 40 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rwpinder/tutorial-air-quality-data-analysis/blob/main/notebooks/06_bonus_live_openaq_api.ipynb) |

Work through them **in order** — each builds on the last. Every notebook contains
✏️ *Your turn* exercises with instant ✅/💡 feedback built in.

## How to take the course

1. **Open a notebook** — click its Colab badge in the table above. The notebook
   opens in [Google Colab](https://colab.research.google.com); nothing to install.
2. **Click "Run anyway"** on Colab's *"Warning: this notebook was not authored by
   Google"* dialog. It appears for any notebook opened from GitHub.
3. **Work through it top to bottom**, running each cell with **Shift+Enter** and
   filling in the ✏️ *Your turn* exercises until the checker cells print ✅.
   (Nothing can break — if things get confused, *Runtime ▸ Restart session* and run
   again from the top.)
4. **Keep your work**: **File ▸ Save a copy in Drive**. Colab puts it in your Google
   Drive under `Colab Notebooks/`, and that copy is where you should keep working —
   edits to the badge-opened copy are not saved anywhere.

Do this once per notebook. If you'd rather keep your progress on GitHub than in
Drive, fork this repository first and use *File ▸ Save a copy in GitHub* to save
into your fork.

## What you need

* A web browser and a **Google account** (for Colab). A GitHub account only if you
  want to keep your work in a fork instead of Drive.
* Nothing to install — Colab already has Python, pandas, and matplotlib.
* Notebook 6 only: a free [OpenAQ API key](https://explore.openaq.org/register).

<details>
<summary><b>Prefer to run locally instead of Colab?</b></summary>

```bash
git clone https://github.com/rwpinder/tutorial-air-quality-data-analysis.git
cd tutorial-air-quality-data-analysis
pip install -r requirements.txt
jupyter lab notebooks/
```
</details>

## The data

Real measurements, deliberately including real-world quirks (gaps, a raw
multi-parameter sensor export, a reference monitor with a 203-day outage):

* **Oshodi Bus Terminal, Lagos** — 12 months of hourly PM2.5 (the primary dataset),
* **Abuja US Embassy** — a reference-grade calendar year with a dramatic Harmattan,
* **five contrasting Lagos-area sites** — bus terminal, university, residential,
  urban park, peri-urban,
* plus the raw and gappy files used in the cleaning lessons.

See [`data/README.md`](data/README.md) for the full data dictionary and provenance.
All measurements are aggregated by [OpenAQ](https://openaq.org) from the original
providers (U.S. Department of State AirNow; AirGradient).

## For instructors

[`INSTRUCTOR.md`](INSTRUCTOR.md) covers running the course with a group, suggested
pacing, the support questions to expect, the course's design rationale, and
regenerating the datasets.

## Credits

Created as a companion to the **AQ agent**, an LLM-assisted air-quality analysis
platform — these notebooks teach, by hand, the same analyses (and the same
chart-design doctrine) its Data Explorer performs conversationally. Code is MIT
licensed; data attribution in [`data/README.md`](data/README.md).
