@echo off
REM 3D Clinostat Single Simulation Example
REM This script runs a single simulation with user-defined parameters

echo ========================================
echo 3D Clinostat Single Simulation
echo ========================================
echo.
echo Enter simulation parameters (press Enter for defaults):
echo.

REM Prompt for inner RPM
set /p INNER="Inner frame RPM [0.25]: "
if "%INNER%"=="" set INNER=0.25

REM Prompt for outer RPM
set /p OUTER="Outer frame RPM [4.0]: "
if "%OUTER%"=="" set OUTER=4.0

REM Prompt for duration
set /p DURATION="Duration in seconds [3000]: "
if "%DURATION%"=="" set DURATION=3000

REM Prompt for output folder
set /p OUTPUT="Output folder [output]: "
if "%OUTPUT%"=="" set OUTPUT=output

echo.
echo ========================================
echo Running simulation with:
echo   Inner frame: %INNER% RPM
echo   Outer frame: %OUTER% RPM
echo   Duration: %DURATION% seconds
echo   Output folder: %OUTPUT%
echo ========================================
echo.

clinostat-sim.exe sim --inner %INNER% --outer %OUTER% --duration %DURATION% --save %OUTPUT%

echo.
echo ========================================
echo Simulation complete!
echo Check the "%OUTPUT%" folder for results:
echo   - trajectory_3d.png
echo   - hemisphere_distribution.png
echo   - time_series.png
echo ========================================
echo.
pause
