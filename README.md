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

### If you're in a class (GitHub Classroom)

Your instructor gave you an **assignment link**. The badges above open the public
course copy — fine for reading, but **your graded work must happen in your own
repository**:

1. **Accept the assignment** by opening your instructor's link and signing in to
   GitHub. Classroom creates a private repository just for you (named like
   `assignment-yourusername`).
2. **Open your copy in Colab**: go to
   [colab.research.google.com](https://colab.research.google.com), choose
   **File ▸ Open notebook ▸ GitHub**, tick **“Include private repos”**, and
   authorize Colab when GitHub asks (if your class organization appears with a
   *Grant* button, click it). Then select **your** assignment repository and the
   notebook you're working on.
3. **Work through the notebook** top to bottom, filling in the ✏️ exercises until
   the checkers print ✅. (The first time you run, Colab shows a *"Warning: this
   notebook was not authored by Google"* dialog — click **Run anyway**; it appears
   for any notebook opened from GitHub.)
4. **Submit by saving back to GitHub**: **File ▸ Save a copy in GitHub**, make sure
   the repository shown is **your assignment repo** (not the course copy), keep the
   file path under `notebooks/`, and leave **“omit code cell output” unchecked** —
   your instructor needs to see your results and plots. Add a short commit message
   and click OK.
5. **Check your submission**: open your repository on github.com — the saved
   notebook should display with your outputs and charts.

Save back to GitHub whenever you make progress; every save is a submission.

### If you're learning on your own

Just click a badge, and click **Run anyway** on Colab's "not authored by Google"
warning. To keep your progress, use **File ▸ Save a copy in Drive** (or fork this
repository and save copies back to your fork).

## What you need

* A web browser, a **Google account** (for Colab), and a **GitHub account**.
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

[`INSTRUCTOR.md`](INSTRUCTOR.md) covers creating the GitHub Classroom, making the
assignment from this template, the student workflow, reviewing submissions, and
regenerating the datasets.

## Credits

Created as a companion to the **AQ agent**, an LLM-assisted air-quality analysis
platform — these notebooks teach, by hand, the same analyses (and the same
chart-design doctrine) its Data Explorer performs conversationally. Code is MIT
licensed; data attribution in [`data/README.md`](data/README.md).
