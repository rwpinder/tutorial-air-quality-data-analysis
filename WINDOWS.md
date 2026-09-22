# Installing the course on Windows

Everything you need — Python, JupyterLab, the packages and the course itself — comes in
one download. You need a connection for that download only; afterwards the course runs
with no internet at all.

**Windows will warn you twice along the way, and both warnings are expected.** They are
about a missing signature, not about anything wrong with the file. What to click is
spelled out below.

Total time: about ten minutes, most of it downloading.

---

## Step 1 — Download the file

Open the Releases page:

```
https://github.com/rwpinder/tutorial-air-quality-data-analysis/releases
```

Under **Windows installer ▸ Assets**, click:

```
AirQualityTutorial-1.0.0-Windows-x86_64.zip
```

Or paste this straight into your browser's address bar:

```
https://github.com/rwpinder/tutorial-air-quality-data-analysis/releases/download/windows-installer/AirQualityTutorial-1.0.0-Windows-x86_64.zip
```

It is about **340 MB**. On a slow connection this can take a while — it is one file, so
you can leave it running.

> **Download it once, use it many times.** The same file installs the course on any
> number of computers. For a class, put it on a USB stick and pass it round rather than
> having thirty people download it over the same connection.

### If the download will not finish

Browsers distrust installer files. In **Edge** or **Chrome** you may end up with a file
called *“Unconfirmed 123456.crdownload”*, which will not open, or a download that sits
there refusing to complete.

1. Press **Ctrl+J** to open your downloads.
2. Find the entry for this file, hover over it, and click **⋯** (More actions) at the
   right-hand side.
3. Choose **Keep**.
4. If you are then asked again — *“This app isn't commonly downloaded and might harm
   your device”* — click **Show more**, then **Keep anyway**.
5. Delete the leftover `Unconfirmed … .crdownload` file. The real file will appear with
   its proper name.

Still stuck? Two ways round it:

* **Use a different browser.** Firefox downloads it without argument.
* **Download from the command line.** Press **Start**, type `powershell`, press Enter,
  and paste this single line:

  ```powershell
  curl.exe -L -o "$env:USERPROFILE\Downloads\AirQualityTutorial.zip" https://github.com/rwpinder/tutorial-air-quality-data-analysis/releases/download/windows-installer/AirQualityTutorial-1.0.0-Windows-x86_64.zip
  ```

  It prints a progress bar and leaves the file in your Downloads folder.

---

## Step 2 — Unblock and unzip it

Windows quietly marks every downloaded file as "from the internet", and that mark
spreads to whatever you extract from it. Clearing it now saves trouble later.

1. In File Explorer, find the `.zip` in your **Downloads** folder.
2. **Right-click it ▸ Properties.**
3. At the bottom of the *General* tab, if you see a checkbox or button marked
   **Unblock**, tick it, then click **OK**. (If there is no Unblock option, nothing is
   wrong — carry on.)
4. **Right-click the zip again ▸ Extract All… ▸ Extract.**

You now have a folder containing **`AirQualityTutorial-1.0.0-Windows-x86_64.exe`**.

---

## Step 3 — Run the installer, and tell Windows it is safe

Double-click the `.exe`. A blue window appears:

> **Windows protected your PC**
> Microsoft Defender SmartScreen prevented an unrecognised app from starting.

This is the warning to expect. To continue:

1. Click **More info** (small link, easy to miss — the *Don't run* button is the only
   obvious option until you click it).
2. Click **Run anyway**.

Then click through the installer: **Next ▸ I Agree ▸ Next ▸ Install**. Leave the
suggested location alone. It takes a couple of minutes.

**Why the warning appears:** the installer is not *code-signed*. A signature is a paid
yearly subscription from a certificate vendor, and this is a free course, so there
isn't one. Windows cannot tell "unknown author" from "dangerous", so it warns about
both the same way. If you would rather satisfy yourself the file is genuine, see
[Checking the file is the real one](#checking-the-file-is-the-real-one) below.

**What it does to your computer** — deliberately very little:

* installs into your own account only (`%LOCALAPPDATA%\AirQualityTutorial`), so it
  never asks for an administrator password;
* does **not** change your `PATH` and does **not** register itself as "the" Python, so
  any Python you already have is untouched;
* puts the notebooks in `Documents\Air Quality Tutorial`;
* adds an **Air Quality Tutorial** shortcut to your desktop and Start menu.

---

## Step 4 — Start the course

Double-click the **Air Quality Tutorial** shortcut on your desktop.

* A black command window opens and stays open. **Leave it there** — that is the program
  itself running. Closing it stops the course.
* Your browser opens showing a list of files. Open the **notebooks** folder and
  double-click **`01_welcome_python_basics.ipynb`**.
* Run each cell with **Shift+Enter** and work down the page.

When you have finished for the day: save with **Ctrl+S**, close the browser tab, then
click the black window and press **Ctrl+C** twice.

Your work is saved straight into the notebook files in `Documents\Air Quality
Tutorial`. There is nothing to upload and nothing to lose.

---

## Checking the file is the real one

Unsigned software is worth a moment's care, and this is how to satisfy yourself — or
your IT department — that the download is exactly what was published.

Download **`SHA256SUMS.txt`** from the same Releases page. Then in PowerShell:

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\AirQualityTutorial-1.0.0-Windows-x86_64.zip" -Algorithm SHA256
```

Compare the long string it prints with the line for that filename in `SHA256SUMS.txt`
(upper- and lower-case do not matter). If they match, your copy is byte-for-byte the
file the build published. If they differ, the download was corrupted or tampered with:
delete it and download again.

Every installer is built in public by
[a GitHub Actions workflow](.github/workflows/build-windows-installer.yml) from the
files in this repository. The build also installs it and runs the course notebooks
inside it before publishing, so nothing is released untested.

---

## If your workplace blocks it

Some organisations refuse all unsigned installers, and no amount of clicking will get
past that. In that case:

* Send your IT team this page and the checksum. The installer contains only open-source
  software from [conda-forge](https://conda-forge.org) plus the course notebooks.
* Or install the pieces yourself instead — [OFFLINE.md](OFFLINE.md) has the manual
  route: install Python, then install seven packages. It ends up in the same place.

---

## If something goes wrong

**The desktop shortcut is missing.** Look in the Start menu for *Air Quality Tutorial*.
If it is not there either, open `%LOCALAPPDATA%\AirQualityTutorial` in File Explorer and
double-click `start_tutorial.bat`; it does exactly what the shortcut does.

**The black window opens and closes immediately.** The install did not finish. Run the
installer again — it is safe to install over itself, and it will not touch notebooks you
have already worked on.

**The browser does not open.** Look in the black window for a line beginning
`http://localhost:8888/lab?token=…` and paste that whole line into your browser.

**Your antivirus deleted the download.** Check its quarantine and restore the file, or
verify the checksum above and add an exception. Antivirus products flag unsigned
installers on reputation alone.

**"This app can't run on your PC".** You have the 64-bit installer on a 32-bit or ARM
machine. Use the manual route in [OFFLINE.md](OFFLINE.md) instead.

**You want to remove it.** *Settings ▸ Apps ▸ Installed apps ▸ AirQualityTutorial ▸
Uninstall.* Your notebooks in Documents are deliberately left behind; delete that folder
by hand if you want them gone too.
