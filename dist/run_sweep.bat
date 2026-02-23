@echo off
REM 3D Clinostat RPM Sweep Example
REM This script sweeps a grid of RPM combinations to find optimal settings

echo ========================================
echo 3D Clinostat RPM Sweep
echo ========================================
echo.
echo Enter sweep parameters (press Enter for defaults):
echo.

REM Prompt for inner frame parameters
set /p INNER_MIN="Inner frame minimum RPM [0.5]: "
if "%INNER_MIN%"=="" set INNER_MIN=0.5

set /p INNER_MAX="Inner frame maximum RPM [4.0]: "
if "%INNER_MAX%"=="" set INNER_MAX=4.0

set /p INNER_STEP="Inner frame RPM step size [0.25]: "
if "%INNER_STEP%"=="" set INNER_STEP=0.25

echo.
REM Prompt for outer frame parameters
set /p OUTER_MIN="Outer frame minimum RPM [0.5]: "
if "%OUTER_MIN%"=="" set OUTER_MIN=0.5

set /p OUTER_MAX="Outer frame maximum RPM [4.0]: "
if "%OUTER_MAX%"=="" set OUTER_MAX=4.0

set /p OUTER_STEP="Outer frame RPM step size [0.25]: "
if "%OUTER_STEP%"=="" set OUTER_STEP=0.25

echo.
REM Prompt for duration
set /p DURATION="Duration per simulation in seconds [3000]: "
if "%DURATION%"=="" set DURATION=3000

REM Prompt for output mode
echo Output options:
echo   1 - Save plots to files
echo   2 - Show interactive plots
echo.
set /p MODE="Choose output mode [1]: "
if "%MODE%"=="" set MODE=1

if "%MODE%"=="2" goto interactive

REM Save mode - prompt for output folder
set /p OUTPUT="Output folder [output]: "
if "%OUTPUT%"=="" set OUTPUT=output

echo.
echo ========================================
echo Running sweep with:
echo   Inner frame RPM: %INNER_MIN% to %INNER_MAX%, step %INNER_STEP%
echo   Outer frame RPM: %OUTER_MIN% to %OUTER_MAX%, step %OUTER_STEP%
echo   Duration: %DURATION% seconds per simulation
echo   Output folder: %OUTPUT%
echo ========================================
echo.
echo NOTE: This may take several minutes to complete.
echo.

clinostat-sim.exe sweep-cmd --inner-min %INNER_MIN% --inner-max %INNER_MAX% --inner-step %INNER_STEP% --outer-min %OUTER_MIN% --outer-max %OUTER_MAX% --outer-step %OUTER_STEP% --duration %DURATION% --save %OUTPUT%

echo.
echo ========================================
echo Sweep complete!
echo Check the "%OUTPUT%" folder for:
echo   - sweep_heatmaps.png (visualization)
echo   - sweep_results.xlsx (data table)
echo   - sweep_results.csv (data table)
echo ========================================
echo.
goto end

:interactive
echo.
echo ========================================
echo Running sweep with:
echo   Inner frame RPM: %INNER_MIN% to %INNER_MAX%, step %INNER_STEP%
echo   Outer frame RPM: %OUTER_MIN% to %OUTER_MAX%, step %OUTER_STEP%
echo   Duration: %DURATION% seconds per simulation
echo   Output: interactive plots
echo ========================================
echo.
echo NOTE: This may take several minutes to complete.
echo.

clinostat-sim.exe sweep-cmd --inner-min %INNER_MIN% --inner-max %INNER_MAX% --inner-step %INNER_STEP% --outer-min %OUTER_MIN% --outer-max %OUTER_MAX% --outer-step %OUTER_STEP% --duration %DURATION%

echo.
echo ========================================
echo Sweep complete!
echo ========================================
echo.

:end
pause
