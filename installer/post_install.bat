@echo off
rem Runs at the end of the installation, with PREFIX set to the install folder.
rem Long single-line PowerShell calls on purpose: caret continuations inside quoted
rem strings are a reliable way to break a .bat file.

setlocal enableextensions
set "COURSE=%USERPROFILE%\Documents\Air Quality Tutorial"

rem 1. Unpack the notebooks and data into Documents. Guarded, so re-running the
rem    installer never overwrites work a student has already done.
if not exist "%COURSE%\notebooks" powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PREFIX%\course.zip' -DestinationPath '%COURSE%' -Force"

rem 2. Start-menu and desktop shortcuts pointing at the launcher.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; foreach ($dir in @([Environment]::GetFolderPath('Programs'), [Environment]::GetFolderPath('Desktop'))) { if (Test-Path $dir) { $lnk = $shell.CreateShortcut((Join-Path $dir 'Air Quality Tutorial.lnk')); $lnk.TargetPath = '%PREFIX%\start_tutorial.bat'; $lnk.WorkingDirectory = '%COURSE%'; $lnk.IconLocation = '%PREFIX%\python.exe,0'; $lnk.Description = 'Open the air quality course in JupyterLab'; $lnk.Save() } }"

exit /b 0
