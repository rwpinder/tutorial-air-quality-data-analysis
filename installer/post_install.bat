@echo off
rem Runs at the end of the installation, with PREFIX set to the install folder.
rem Long single-line PowerShell calls on purpose: caret continuations inside quoted
rem strings are a reliable way to break a .bat file.
rem
rem Everything is logged to %PREFIX%\post_install.log — the installer window is gone
rem by the time anything goes wrong, so that file is the only way to find out why.

setlocal enableextensions
set "COURSE=%USERPROFILE%\Documents\Air Quality Tutorial"
set "LOG=%PREFIX%\post_install.log"

echo [post_install] %DATE% %TIME%> "%LOG%"
echo PREFIX=%PREFIX%>> "%LOG%"
echo USERPROFILE=%USERPROFILE%>> "%LOG%"
echo COURSE=%COURSE%>> "%LOG%"
echo --- contents of the install folder --->> "%LOG%"
dir /b "%PREFIX%">> "%LOG%" 2>&1

rem 1. Unpack the notebooks and data into Documents. Guarded, so re-running the
rem    installer never overwrites work a student has already done.
if exist "%COURSE%\notebooks" (
    echo [1] course folder already present, leaving it alone>> "%LOG%"
) else (
    echo [1] expanding "%PREFIX%\course.zip" into "%COURSE%">> "%LOG%"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PREFIX%\course.zip' -DestinationPath '%COURSE%' -Force">> "%LOG%" 2>&1
    echo [1] exit code %ERRORLEVEL%>> "%LOG%"
)

rem 2. Start-menu and desktop shortcuts pointing at the launcher.
echo [2] creating shortcuts>> "%LOG%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; foreach ($dir in @([Environment]::GetFolderPath('Programs'), [Environment]::GetFolderPath('Desktop'))) { if (Test-Path $dir) { $lnk = $shell.CreateShortcut((Join-Path $dir 'Air Quality Tutorial.lnk')); $lnk.TargetPath = '%PREFIX%\start_tutorial.bat'; $lnk.WorkingDirectory = '%COURSE%'; $lnk.IconLocation = '%PREFIX%\python.exe,0'; $lnk.Description = 'Open the air quality course in JupyterLab'; $lnk.Save(); Write-Output ('made ' + $dir) } }">> "%LOG%" 2>&1
echo [2] exit code %ERRORLEVEL%>> "%LOG%"

echo [post_install] finished>> "%LOG%"
exit /b 0
