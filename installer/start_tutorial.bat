@echo off
rem Launcher for the course. Sits in the install folder; the Start-menu and desktop
rem shortcuts point at it. Sets up the environment by hand rather than activating it,
rem so nothing about the student's machine is changed.

set "PREFIX=%~dp0"
set "COURSE=%USERPROFILE%\Documents\Air Quality Tutorial"
set "PATH=%PREFIX%;%PREFIX%Library\mingw-w64\bin;%PREFIX%Library\usr\bin;%PREFIX%Library\bin;%PREFIX%Scripts;%PREFIX%bin;%PATH%"

rem Unpack the course on first run if the install-time step did not manage it —
rem the launcher is what students actually click, so it is the reliable place to
rem make sure the notebooks exist.
if not exist "%COURSE%\notebooks" (
    if exist "%PREFIX%course.zip" (
        echo   Setting up your notebooks in %COURSE% ...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PREFIX%course.zip' -DestinationPath '%COURSE%' -Force"
    )
)

if not exist "%COURSE%" mkdir "%COURSE%"
cd /d "%COURSE%"

echo.
echo   Air Quality Data Analysis
echo   -------------------------
echo   JupyterLab is starting in your web browser.
echo   Your notebooks are in: %COURSE%
echo.
echo   Leave this window open while you work. To finish, close the browser tab
echo   and then press Ctrl+C twice in here.
echo.

"%PREFIX%Scripts\jupyter-lab.exe" --notebook-dir="%COURSE%"
