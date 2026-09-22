@echo off
rem Runs at the end of the installation, with PREFIX set to the install folder.
rem
rem Two hard-won rules here:
rem   * the installer runs with a minimal PATH, so `powershell` alone is not found
rem     (it fails with 9009). Call it by absolute path, and prefer the Python we
rem     have just installed for anything it can do.
rem   * `echo text %ERRORLEVEL%>> file` makes cmd read the trailing digit as a file
rem     handle and the line disappears. Always leave a space before the >>.
rem
rem Everything is logged to %PREFIX%\post_install.log — the installer window is gone
rem by the time anything goes wrong, so that file is the only way to find out why.

setlocal enableextensions enabledelayedexpansion
set "COURSE=%USERPROFILE%\Documents\Air Quality Tutorial"
set "LOG=%PREFIX%\post_install.log"
set "PS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
set "UNZIP=import zipfile, sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])"

echo [post_install] %DATE% %TIME%> "%LOG%"
echo PREFIX=%PREFIX% >> "%LOG%"
echo COURSE=%COURSE% >> "%LOG%"

rem 1. Unpack the notebooks and data into Documents, using the bundled Python so
rem    nothing depends on the PATH. Guarded, so re-running the installer never
rem    overwrites work a student has already done.
if exist "%COURSE%\notebooks" (
    echo [1] course folder already present, leaving it alone >> "%LOG%"
    goto shortcuts
)
echo [1] unpacking course.zip into the course folder >> "%LOG%"
"%PREFIX%\python.exe" -c "%UNZIP%" "%PREFIX%\course.zip" "%COURSE%" >> "%LOG%" 2>&1
echo [1] exit code !ERRORLEVEL! >> "%LOG%"

:shortcuts
rem 2. Start-menu and desktop shortcuts pointing at the launcher.
echo [2] creating shortcuts >> "%LOG%"
"%PS%" -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; foreach ($dir in @([Environment]::GetFolderPath('Programs'), [Environment]::GetFolderPath('Desktop'))) { if (Test-Path $dir) { $lnk = $shell.CreateShortcut((Join-Path $dir 'Air Quality Tutorial.lnk')); $lnk.TargetPath = '%PREFIX%\start_tutorial.bat'; $lnk.WorkingDirectory = '%COURSE%'; $lnk.IconLocation = '%PREFIX%\python.exe,0'; $lnk.Description = 'Open the air quality course in JupyterLab'; $lnk.Save(); Write-Output ('made a shortcut in ' + $dir) } }" >> "%LOG%" 2>&1
echo [2] exit code !ERRORLEVEL! >> "%LOG%"

echo [post_install] finished >> "%LOG%"
exit /b 0
