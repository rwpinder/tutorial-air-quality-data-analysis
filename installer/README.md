# The Windows installer

`AirQualityTutorial-<version>-Windows-x86_64.exe` gives a student everything in one
file: Python, JupyterLab, the seven packages the notebooks need, and the notebooks and
data themselves. They download it once while connected, run it, and the course works
from then on with no connection at all.

What it does on the student's machine:

* installs into `%LOCALAPPDATA%\AirQualityTutorial` — **no administrator rights**, no
  changes to `PATH`, and no interference with any other Python already installed;
* unpacks the notebooks and data into `Documents\Air Quality Tutorial` — and leaves
  them alone if that folder already has work in it;
* adds a **Start-menu and desktop shortcut** that opens JupyterLab on that folder.

To uninstall, use *Settings ▸ Apps*, or run `Uninstall-AirQualityTutorial.exe` in the
install folder. Student notebooks in Documents are deliberately left behind.

## Building it

Nobody needs a Windows machine: the build runs on a GitHub-hosted Windows runner.

1. Actions tab ▸ **Windows installer** ▸ *Run workflow*.
2. Tick **Attach the installer to the windows-installer release** to publish it;
   leave it unticked for a trial build, which only uploads an artifact.

The workflow does not just build — it installs the result silently and then executes
notebooks 1–5, 7 and 8 inside the installed environment, so a green run means the
installer really works, not merely that it compiled. Pushing to a branch named
`installer/**` runs the same build, which is how to iterate on this folder.

## The pieces

| File | What it is |
|------|-----------|
| `construct.yaml` | the package list and installer options, read by [constructor](https://conda.github.io/constructor/) |
| `post_install.bat` | runs at the end of the install: unpacks the course, makes the shortcuts |
| `start_tutorial.bat` | what the shortcuts point at; sets up the environment and starts JupyterLab |
| `course.zip` | built by the workflow from `notebooks/` and `data/` — not stored in the repository |

## Two things to know

**It is not code-signed.** Windows shows *“Windows protected your PC”* on first run;
students click **More info ▸ Run anyway**. Removing that warning needs a paid
code-signing certificate. Worth telling a group up front, because it looks alarming.

**The installer is a fixed snapshot.** It pins Python 3.13 and whatever package
versions conda-forge served on build day. Rebuild it after changing the notebooks or
the data, otherwise students get the old course inside a new installer.
