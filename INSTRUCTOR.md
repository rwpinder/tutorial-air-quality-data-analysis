# Instructor Guide

How to run this course with **GitHub Classroom + Google Colab**: each student gets a
private copy of these notebooks, works on them in Colab (nothing to install), and
submits by saving back to their repository — where you review their filled-in
exercises and rendered charts. (This video shows the same student workflow in
another course: ["Instruction to use Github classroom and Google Colab"](https://www.youtube.com/watch?v=UziJMx4yjcc).)

## One-time setup (about 20 minutes)

1. **Create a GitHub organization** for your class (free): github.com → “+” →
   *New organization* → Free plan. Example name: `aq-python-2026`.
2. **Create a classroom**: go to [classroom.github.com](https://classroom.github.com),
   sign in, *New classroom*, and connect it to that organization.
3. **Create the assignment**: in the classroom, *New assignment* →
   * **Individual** assignment; repository visibility **Private** (the default —
     each student sees only their own work).
   * Under *Starter code*, choose **`rwpinder/tutorial-air-quality-data-analysis`**
     (this repository — it's public and marked as a template, so any classroom can
     use it directly; fork it first if you want to customise).
   * **Skip the autograding section** — grading feedback is built into the
     notebooks as self-check cells, and you review the pushed notebooks by eye.
4. **Copy the invitation link** and send it to your students. Optionally add a
   roster (student identifiers) so Classroom maps GitHub accounts to names.

## What students do

The exact steps (with screenshots-level detail) are in this repo's
[README](README.md#if-youre-in-a-class-github-classroom); in short:

1. Open your invitation link → accept → Classroom creates their private repo.
2. In Colab: *File ▸ Open notebook ▸ GitHub* → tick **Include private repos**
   (a one-time GitHub authorization; if the popup shows your organization with a
   **Grant** button, they must click it — this is the #1 support question).
   On first run, Colab warns *"this notebook was not authored by Google"* —
   **Run anyway** is the expected answer (#2 support question).
3. Work through the notebook; ✏️ exercises give instant ✅/💡 feedback.
4. *File ▸ Save a copy in GitHub* → their repo, path under `notebooks/`, **“omit
   code cell output” unchecked** → every save is a submission.

## Reviewing submissions

* The classroom dashboard lists every student repo; open a repo → `notebooks/` →
  GitHub renders the notebook **with the student's outputs and charts inline**
  (this course uses matplotlib precisely because GitHub displays its output;
  the optional Plotly cells at the end of notebook 5 will show as blank on GitHub —
  that's expected).
* What to look for, per notebook: the ✏️ exercise cells filled in, their checker
  cells printing **✅**, and — from notebook 4 on — charts whose **titles state a
  finding** (that habit is the course's real deliverable).
* Suggested pace: one notebook per session; 1–2 → 3 → 4 → 5 across four sessions,
  notebook 6 as homework for the keen.

## Course design notes

* **Audience**: air-quality professionals with zero programming background.
  Domain examples (WHO guidelines, Harmattan, rush hours) carry the motivation.
* **Self-checks**: every exercise is followed by a `check(...)` cell that prints
  ✅ or a 💡 hint and never raises — notebooks 1–5 run top-to-bottom even with all
  exercises unfilled, so "Run all" never strands a student on a traceback.
  Notebook 6 requires a (free) OpenAQ API key and warns students accordingly.
* **The data is real** and includes real problems on purpose: a low-cost sensor
  with 45 missing days, a reference monitor with a 203-day outage, and a raw
  multi-parameter export that must be filtered and parsed. See
  [`data/README.md`](data/README.md).
* **Solutions**: instructor solution notebooks (every exercise filled, all outputs
  rendered) exist but are deliberately not in this public repository — contact the
  course author.

## Maintaining the course

* **Refreshing the data** (e.g., a new 12-month window): `pip install pandas boto3`,
  edit the window/site constants at the top of
  [`scripts/prepare_data.py`](scripts/prepare_data.py), run it, and review the QC
  summary it prints (row counts, spans, completeness) before committing the new
  CSVs. It downloads from OpenAQ's public archive — no API key needed. Note that
  several notebook checks reference the current data's values (peak hour 08:00,
  worst month January, site means); if you regenerate with a different window,
  re-run the notebooks and adjust any check that turns 💡.
* **Editing notebooks**: edit the `.ipynb` files directly in Jupyter or Colab and
  commit. Keep the two invariants: exercise cells contain only assignments (so an
  unfilled notebook still runs top-to-bottom), and checker cells print rather than
  raise.
* After any change, click through one notebook in Colab as a student would before
  the next class.
