# Instructor Guide

How to run this course with a group. There is **nothing to set up**: the notebooks
are public, students open them in Google Colab straight from this repository, and
each keeps their own copy in Google Drive. No accounts to provision, no starter
repositories, no submission step.

## Running the course

1. **Send students the link** to this repository —
   `https://github.com/rwpinder/tutorial-air-quality-data-analysis` — and point them
   at the badge table in the [README](README.md#the-notebooks). Each badge opens
   that notebook in Colab.
2. **Tell them to save a copy to Drive** (*File ▸ Save a copy in Drive*) the first
   time they open each notebook, and to work in that copy — edits to the
   badge-opened copy are not saved anywhere. This is the one instruction worth
   repeating out loud.
3. **Suggested pace**: one notebook per session — 1–2 → 3 → 4 → 5 across four
   sessions, with notebook 6 (the live OpenAQ API) as homework for the keen.
   Notebook 6 needs a free [OpenAQ API key](https://explore.openaq.org/register);
   if you plan to cover it, have students register beforehand.
4. **The advanced pair**: notebooks 7 (mapping a sensor network) and 8 (regional
   background vs local sources) add two further sessions. They are genuinely
   harder — 7 introduces spatial interpolation, 8 introduces wavelets — and they
   assume notebook 5. Groups short on time can stop after 5 with a complete
   course; groups of analysts will get the most out of 7 and 8.

### The two support questions to expect

* *"Colab says this notebook wasn't authored by Google."* — **Run anyway**. It
  appears for every notebook opened from GitHub.
* *"I closed the tab and lost my work."* — they were editing the badge-opened copy.
  *Save a copy in Drive* first; the Drive copy lives under `Colab Notebooks/`.

## Checking progress in class

There is no submission or grading step — the feedback is built into the notebooks,
so students self-check as they go. To see where a group is:

* Ask for a show of hands on **✅ counts** — each ✏️ *Your turn* exercise is followed
  by a checker cell that prints ✅ or a 💡 hint, so "how many ✅ in notebook 3?" is a
  precise, low-friction progress question.
* Walk the room (or, remotely, ask students to share their screen) during exercises;
  the 💡 hints tell you exactly which concept a student is stuck on.
* If you do want to look at finished work, ask students to share their Drive copy
  (*Share ▸ Anyone with the link ▸ Viewer*) or to paste a chart into a shared doc.
* What to look for, per notebook: the ✏️ exercise cells filled in, their checker
  cells printing **✅**, and — from notebook 4 on — charts whose **titles state a
  finding** (that habit is the course's real deliverable).

## Course design notes

* **Audience**: air-quality professionals with zero programming background.
  Domain examples (WHO guidelines, Harmattan, rush hours) carry the motivation.
* **Self-checks**: every exercise is followed by a `check(...)` cell that prints
  ✅ or a 💡 hint and never raises — notebooks 1–5, 7 and 8 run top-to-bottom even
  with all exercises unfilled, so "Run all" never strands a student on a
  traceback. Notebook 6 requires a (free) OpenAQ API key and warns students
  accordingly.
* **Notebooks 7 and 8 teach scepticism, not just technique.** Both spend a
  section on whether the result could be an instrument artefact rather than a
  finding — the August 2025 AirQo sensors really did lose their hour-to-hour
  coherence, and the notebooks diagnose it with a colocated sensor pair and an
  autocorrelation check, then show that the seasonal conclusions survive it. If
  you cut for time, keep those sections: they are the most transferable thing in
  the course.
* **Notebook 8 reproduces a published method.** The four-component split is
  Zimmerman et al. (2020), *Aerosol and Air Quality Research* 20, 314–328, with
  the iterative non-negative baseline of Klems et al. (2010). It is the same
  method the AQ agent's wavelet module runs in production, on the same city, so
  students who go on to use the agent will recognise it.
* **Charts render in the browser**: this course uses matplotlib throughout, so
  plots appear inline in Colab (and in the notebook file itself if a student saves
  it with outputs). The optional Plotly cells at the end of notebook 5 are
  interactive in Colab but show as blank if the notebook is viewed on GitHub.
* **The data is real** and includes real problems on purpose: a low-cost sensor
  with 45 missing days, a reference monitor with a 203-day outage, a raw
  multi-parameter export that must be filtered and parsed, and a network month
  (August 2025) noisy enough that the completeness bar had to be lowered to 60%
  to keep enough sensors to map. See [`data/README.md`](data/README.md).
* **Solutions**: instructor solution notebooks (every exercise filled, all outputs
  rendered) exist but are deliberately not in this public repository — contact the
  course author.

## Making your own version

The notebooks are MIT licensed and this repository is a GitHub template, so you can
click **Use this template** (or fork) to make a copy you customise — swapping in
your own city's data, cutting notebooks, changing the pacing. If you do, note that
the Colab badge URLs in the README encode the repository path, so update them to
point at your copy before handing the link out.

## Maintaining the course

* **Refreshing the data** (e.g., a new 12-month window): `pip install pandas boto3`,
  edit the window/site constants at the top of
  [`scripts/prepare_data.py`](scripts/prepare_data.py), run it, and review the QC
  summary it prints (row counts, spans, completeness) before committing the new
  CSVs. It downloads from OpenAQ's public archive — no API key needed. Note that
  several notebook checks reference the current data's values (peak hour 08:00,
  worst month January, site means); if you regenerate with a different window,
  re-run the notebooks and adjust any check that turns 💡.
* **Refreshing the network data** (notebooks 7 and 8): these two months come from
  the AQ agent measurement database rather than the OpenAQ archive, because the
  Lagos network is mostly AirQo sensors and AirQo data is not in that archive.
  Regenerate with [`scripts/prepare_network_data.py`](scripts/prepare_network_data.py)
  — it needs database access (`DATABASE_URL`), or `--print-sql` to run the two
  queries yourself and `--from-dump` to shape the results offline. The window and
  completeness thresholds are constants at the top of the file. Both notebooks
  quote figures from this data in their prose (background shares, correlations,
  autocorrelations); re-run them and update any number that moves.
* **Editing notebooks**: edit the `.ipynb` files directly in Jupyter or Colab and
  commit. Keep the two invariants: exercise cells contain only assignments (so an
  unfilled notebook still runs top-to-bottom), and checker cells print rather than
  raise.
* After any change, click through one notebook in Colab as a student would before
  the next class.
