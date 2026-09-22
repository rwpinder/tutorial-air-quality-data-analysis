# Using this course without the internet

Google Colab needs a connection. **Everything else in this course does not.** All the
measurements ship inside this repository, and every notebook reads them from the
`data/` folder when it is there — nothing is downloaded while you work. The one
exception is notebook 6, which calls a live air-quality API.

So the plan is: install Python and seven packages **once, while you have a
connection**, then work through the course with the Wi-Fi off.

You will use **JupyterLab**, which shows notebooks in your browser much as Colab
does — same cells, same **Shift+Enter**, same charts.

---

## Windows: one file installs everything

Download **`AirQualityTutorial-…-Windows-x86_64.exe`** (about 340 MB) from the
[**Releases page**](https://github.com/rwpinder/tutorial-air-quality-data-analysis/releases)
and run it. Python, JupyterLab, every package and the course itself are inside it, so
there is nothing else to install and nothing to fetch later.

* Windows will say **“Windows protected your PC”**. Click **More info ▸ Run anyway** —
  the installer is simply not code-signed, which costs a yearly fee.
* It installs for you alone. No administrator password, no changes to your `PATH`, and
  no interference with any other Python on the machine.
* When it finishes you have an **Air Quality Tutorial** shortcut on your desktop and in
  the Start menu. Click it and JupyterLab opens in your browser, showing the notebooks,
  which live in `Documents\Air Quality Tutorial`.
* To remove it later: *Settings ▸ Apps*. Your notebooks in Documents are left alone.

Then skip ahead to [What is different from Colab](#what-is-different-from-colab).

Everything between here and there is for macOS and Linux — and for anyone on Windows
who would rather install the pieces themselves.

---

## What you need to download

Do this part while you are connected. About **150 MB** in total, once.

| What | Size | Where it comes from |
|------|------|---------------------|
| The Python installer | ~30 MB | <https://www.python.org/downloads/> |
| This course (*Code ▸ Download ZIP*) | ~5 MB | the repository's green **Code** button |
| Seven Python packages | ~110–145 MB | downloaded for you in Step 3 |

Once installed, the course takes roughly **600 MB** of disk space.

---

## Step 1 — Install Python

### Windows

1. Go to <https://www.python.org/downloads/> and download the installer for Windows.
2. Run it, and on the very first screen **tick “Add python.exe to PATH”**. This is the
   one step people miss, and skipping it causes most of the problems in the
   troubleshooting list below.
3. Click **Install Now**.
4. Check it worked: press **Start**, type `cmd`, press Enter, and in the black window
   type `python --version`. You should see a version number.

### macOS

1. Go to <https://www.python.org/downloads/> and download the macOS installer.
2. Run it and accept the defaults.
3. Check it worked: open **Terminal** (press ⌘+Space, type `Terminal`) and type
   `python3 --version`.

Use this Python rather than the one Apple includes with macOS.

### Linux

```bash
sudo apt install python3 python3-venv python3-pip     # Debian / Ubuntu
python3 --version
```

**Which version?** Anything from **Python 3.11** onwards. This course was last tested
on **3.14.3**. If you are preparing several machines for a group, make sure everyone
installs the *same* version — see the instructor section at the end.

---

## Step 2 — Get the course files

On the repository page, click the green **Code** button, then **Download ZIP**. Unzip
it somewhere you will find again — your Documents folder is fine.

You should end up with a folder containing `notebooks/`, `data/`, `README.md` and
`requirements.txt`.

**Keep the notebooks inside the `notebooks/` folder.** They find the measurements by
looking one folder up, so a notebook moved elsewhere will try to download the data
instead — and fail when you are offline.

---

## Step 3 — Install the seven packages

**Open a terminal in the course folder:**

* **Windows** — open the folder in File Explorer, click in the address bar at the top,
  type `cmd`, and press Enter.
* **macOS** — open Terminal, type `cd ` (with a space), then drag the course folder
  onto the Terminal window and press Enter.

**Then create a private workspace for the course and install into it.**

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas matplotlib plotly requests jupyterlab scipy PyWavelets
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pandas matplotlib plotly requests jupyterlab scipy PyWavelets
```

The download takes a few minutes. When it finishes, your prompt starts with `(.venv)` —
that is how you know the workspace is switched on.

> **What is a “virtual environment”?** The `.venv` folder is a private box holding this
> course's packages, so they cannot disturb anything else on your computer. If your
> setup ever gets tangled, delete the `.venv` folder and run these three lines again.

There is also a `requirements.txt` in the folder. It installs the same seven packages
plus two more (`boto3`, `contextily`) that are only needed for regenerating the course
data from scratch — a much bigger download that students do not need.

*No internet at all on this machine?* See **Preparing machines with no connection** at
the end.

---

## Step 4 — Start JupyterLab

In the same terminal, with `(.venv)` showing:

```bash
jupyter lab
```

Your browser opens with a file browser on the left. Open the `notebooks` folder and
double-click `01_welcome_python_basics.ipynb`. Run each cell with **Shift+Enter**,
exactly as the notebooks describe.

**To stop:** close the browser tab, then press **Ctrl+C** twice in the terminal.

**Every day after that**, three lines from the course folder:

```bash
cd path/to/tutorial-air-quality-data-analysis
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # macOS / Linux
jupyter lab
```

---

## What is different from Colab

The notebooks were written for Colab, so a few menu names differ. Everything else —
cells, Shift+Enter, the ✅/💡 self-checks — behaves the same.

| The notebook says | In JupyterLab |
|---|---|
| *Runtime ▸ Restart session* | **Kernel ▸ Restart Kernel** |
| *Runtime ▸ Run all* | **Run ▸ Run All Cells** |
| *File ▸ Save a copy in Drive* | **Ctrl+S** / **⌘S** — saves straight into the notebook file |
| the 📁 Files panel | the file browser on the left |
| “Run anyway” warning | does not appear |

**Your work is saved in the notebook file on your own computer.** There is no Drive
copy to make and nothing to lose when you close the tab. If you later want a fresh,
unfilled copy of a notebook, download the ZIP again.

---

## The one notebook that needs the internet

**Notebook 6 (Bonus: the OpenAQ API)** fetches live measurements from the internet and
needs a free [OpenAQ API key](https://explore.openaq.org/register). Do that one while
you are connected, or skip it — nothing later depends on it.

Notebooks **1–5, 7 and 8 run completely offline**, including all the maps and charts.
The Accra map in notebook 7 is a picture that ships with the course, so no map service
is contacted.

---

## If something goes wrong

**`'python' is not recognized…`** (Windows) — Python was installed without “Add
python.exe to PATH”. Either re-run the installer and tick that box, or type `py`
instead of `python`.

**`No module named pandas`** — the workspace is not switched on. Your prompt should
start with `(.venv)`; if it does not, run the `activate` line again from the course
folder.

**The browser did not open** — look in the terminal for a line starting with
`http://localhost:8888/lab?token=…` and paste that whole line into your browser.

**`Port 8888 is already in use`** — JupyterLab is already running in another window.
Close it, or let JupyterLab pick the next port when it offers.

**A notebook tries to download data, or says `FileNotFoundError: ../data/…`** — the
notebook has been moved out of the `notebooks/` folder. Put it back, or keep the
`data/` folder one level above it.

**Charts do not appear, or a cell complains about a name it does not know** — run the
cells in order from the top of the notebook. Each one builds on the last.
**Kernel ▸ Restart Kernel and Run All Cells** fixes almost everything.

**The interactive chart in notebook 5 is blank** — restart the kernel and run the
notebook again from the top. The other charts in that notebook are ordinary images and
are unaffected.

**`pip` fails behind a company firewall or antivirus** — use the offline route below,
prepared on a machine that is not restricted.

---

## For instructors: preparing machines with no connection

### If each machine can get online once

Walk the group through Steps 1–4 above. Budget about 15 minutes per machine, most of
it waiting for the download, and have the course ZIP on a USB stick so 30 people are
not pulling it over the same weak connection.

### If the machines never get online

**For a room of Windows machines, put the one-file installer on a USB stick and stop
there.** It is self-contained, so each machine needs nothing else: copy, run, click
through the unsigned-software warning, done in a few minutes per laptop. Rebuild it
from the Actions tab whenever the notebooks change (see
[`installer/README.md`](installer/README.md)).

For macOS or Linux machines, build a USB stick containing the Python installer, the
course ZIP, and a folder of pre-downloaded packages (a “wheelhouse”).

On a connected machine **of the same operating system and the same Python version** as
the target machines:

```bash
pip download pandas matplotlib plotly requests jupyterlab scipy PyWavelets -d wheels
```

Then on each offline machine — install Python, unzip the course, and run:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --no-index --find-links D:\wheels ^
    pandas matplotlib plotly requests jupyterlab scipy PyWavelets
```

(`--no-index` tells pip not to look for the internet at all. On macOS or Linux use
`python3`, `source .venv/bin/activate`, and the path to the folder on the stick.)

Measured on macOS: **109 MB** of packages, giving a 573 MB installed environment.

### Building the Windows stick from a Mac

This works, with one trap worth knowing. `pip download` will fetch the Windows
versions of the packages, but it still decides *which* packages are needed based on the
machine it is running on — so it silently leaves out three packages that only Windows
needs, and JupyterLab will not start without them. Ask for them explicitly:

```bash
pip download --only-binary=:all: --platform win_amd64 --python-version 3.13 \
    pandas matplotlib plotly requests jupyterlab scipy PyWavelets -d wheels-win

pip download --only-binary=:all: --platform win_amd64 --python-version 3.13 \
    pywin32 pywinpty colorama -d wheels-win
```

That produces **143 MB** across 107 files. The `--python-version` must match the Python
your students install (3.13 in the example), because these files are tied to a specific
version — so tell the room one version and stick to it.

**Caveat:** that bundle was assembled and checked on a Mac, not installed on Windows.
Do one trial install on any Windows laptop before the workshop.

---

## What was tested

On 2026-09-22, on macOS, in a newly created environment: Python 3.14.3 with pandas
3.0.6, matplotlib 3.11.2, plotly 7.1.0, scipy 1.18.1, PyWavelets 1.8.0 and JupyterLab
4.6.4. Notebooks 1–5, 7 and 8 each ran top to bottom reading the local `data/` folder,
and JupyterLab served the course folder without incident.

The Windows installer is tested the same way, on every build: the workflow installs it
silently on a Windows machine, checks the notebooks reached Documents and the shortcut
exists, then runs those same seven notebooks inside the installed environment. A
published installer is one that passed all of it.
