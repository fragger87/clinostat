========================================
3D Clinostat Microgravity Simulator
Windows Executable Distribution
========================================

This folder contains a standalone Windows executable for the 3D Clinostat
Microgravity Simulator. No Python installation required!

CONTENTS:
---------
  clinostat-sim.exe       Standalone executable (39 MB)
  run_simulation.bat      Interactive script for single simulations
  run_sweep.bat           Interactive script for RPM sweeps
  README.txt              This file

QUICK START:
------------
1. Double-click run_simulation.bat OR run_sweep.bat
2. Enter parameters when prompted (or press Enter to use defaults)
3. Results will be saved in the "output" folder

OPTION 1: Single Simulation (run_simulation.bat)
-------------------------------------------------
Runs a single simulation with two rotating frames.

Parameters:
  - Inner frame RPM (default: 0.25)
  - Outer frame RPM (default: 4.0)
  - Duration in seconds (default: 3000)
  - Output folder (default: output)

Output files:
  - trajectory_3d.png           3D path of acceleration vector
  - hemisphere_distribution.png Fibonacci lattice coverage
  - time_series.png             X, Y, Z acceleration over time

OPTION 2: RPM Sweep (run_sweep.bat)
------------------------------------
Sweeps a grid of RPM combinations to find optimal settings.

Parameters:
  - Inner frame minimum RPM (default: 0.5)
  - Inner frame maximum RPM (default: 4.0)
  - Inner frame RPM step size (default: 0.25)
  - Outer frame minimum RPM (default: 0.5)
  - Outer frame maximum RPM (default: 4.0)
  - Outer frame RPM step size (default: 0.25)
  - Duration per simulation (default: 3000)
  - Output folder (default: output)

Output files:
  - sweep_heatmaps.png  Side-by-side magnitude & distribution heatmaps
  - sweep_results.xlsx  Complete data table with all combinations

COMMAND LINE USAGE:
-------------------
You can also run the executable directly from Command Prompt or PowerShell:

  Single simulation:
    clinostat-sim.exe sim --inner 0.25 --outer 4.0

  RPM sweep:
    clinostat-sim.exe sweep-cmd --inner-min 0.5 --inner-max 4.0 --inner-step 0.25 --outer-min 0.5 --outer-max 4.0 --outer-step 0.25

  Get help:
    clinostat-sim.exe --help
    clinostat-sim.exe sim --help
    clinostat-sim.exe sweep-cmd --help

SYSTEM REQUIREMENTS:
--------------------
  - Windows 7 or newer
  - No additional software required

NOTES:
------
  - The sweep operation can take several minutes depending on grid size
  - Default settings (0.5 to 4.0, step 0.25) = 225 combinations
  - For faster results, use larger step sizes (e.g., 0.5)
  - All output is saved to the specified folder (created if needed)

========================================
