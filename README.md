# 3D Clinostat Microgravity Simulator

Simulate and visualize the microgravity performance of a 3D clinostat — a device with two independently rotating frames that time-averages the gravity vector to near-zero. Evaluate RPM combinations using two quality metrics:

- **Magnitude** — L2 norm of the time-averaged acceleration vector (lower is better)
- **Distribution score** — number of Fibonacci hemisphere lattice points (out of 1000) hit by the acceleration vector over time (higher is better)

## Prerequisites

### Python

Python **3.9 or newer** is required (3.12+ recommended).

| Platform | Recommended install method |
|---|---|
| **macOS** | `brew install python@3.12` or install via [pyenv](https://github.com/pyenv/pyenv): `pyenv install 3.12` |
| **Ubuntu / Debian** | `sudo apt update && sudo apt install python3 python3-pip python3-venv` |
| **Fedora / RHEL** | `sudo dnf install python3 python3-pip` |
| **Arch Linux** | `sudo pacman -S python python-pip` |
| **Windows** | Download from [python.org](https://www.python.org/downloads/) or `winget install Python.Python.3.12`. Check "Add to PATH" during installation. |

Verify your install:

```bash
python3 --version   # macOS/Linux
python --version     # Windows
```

### Poetry (dependency manager)

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and virtual environments.

**macOS / Linux:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then add Poetry to your PATH (the installer will tell you the exact path):

```bash
# Add to ~/.zshrc (macOS) or ~/.bashrc (Linux):
export PATH="$HOME/.local/bin:$PATH"
```

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Poetry will be installed to `%APPDATA%\Python\Scripts` — add it to your PATH or use the full path.

Verify:

```bash
poetry --version
```

## Installation

```bash
git clone <repository-url>
cd clinostat-sim
poetry install
```

This creates a virtual environment and installs all dependencies (`numpy`, `matplotlib`, `click`, `openpyxl`).

**Windows note:** If you encounter issues with Poetry installation, you can use pip directly:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install numpy matplotlib click openpyxl
```

## Usage

All commands are run from the project root directory.

### Single simulation

Simulate one inner/outer RPM pair and visualize the results:

**Using Poetry:**
```bash
poetry run python -m app sim --inner 0.25 --outer 4.0
```

**Windows (direct venv):**
```bash
.venv\Scripts\python -m app sim --inner 0.25 --outer 4.0
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--inner` | *(required)* | Inner frame RPM |
| `--outer` | *(required)* | Outer frame RPM |
| `--duration` | 3000 | Simulation duration in seconds |
| `--dt` | 0.1 | Timestep in seconds |
| `--save DIR` | *(none)* | Save plots to directory instead of showing interactively |

**Example — save plots to disk:**

```bash
poetry run python -m app sim --inner 0.25 --outer 4.0 --duration 3000 --save ./output
```

**Windows:**
```bash
.venv\Scripts\python -m app sim --inner 0.25 --outer 4.0 --duration 3000 --save ./output
```

This generates three plots:
- `trajectory_3d.png` — 3D path of the acceleration vector
- `hemisphere_distribution.png` — which Fibonacci lattice points were hit
- `time_series.png` — X, Y, Z acceleration components over time

### RPM sweep (heatmaps)

Sweep a grid of inner/outer RPM combinations to find optimal settings:

**Using Poetry:**
```bash
poetry run python -m app sweep-cmd --rpm-min 0.5 --rpm-max 4.0 --rpm-step 0.25
```

**Windows (direct venv):**
```bash
.venv\Scripts\python -m app sweep-cmd --rpm-min 0.5 --rpm-max 4.0 --rpm-step 0.25
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--rpm-min` | 0.125 | Minimum RPM for both axes |
| `--rpm-max` | 4.0 | Maximum RPM for both axes |
| `--rpm-step` | 0.125 | RPM increment |
| `--duration` | 3000 | Duration per simulation in seconds |
| `--dt` | 0.1 | Timestep in seconds |
| `--save DIR` | *(none)* | Save heatmap to directory |

This generates `sweep_heatmaps.png` — side-by-side magnitude and distribution score heatmaps, and prints the best RPM combinations to the terminal.

> **Note:** A full sweep with default settings (32x32 = 1024 combinations) can take 15–20 minutes. Use a larger `--rpm-step` or smaller `--rpm-max` for quicker runs.

## Building a Windows executable

To create a standalone Windows executable (.exe) that can run without Python installed:

### 1. Install PyInstaller

First, activate your virtual environment and install PyInstaller:

**Using Poetry:**
```powershell
poetry add --group dev pyinstaller
```

**Using pip directly:**
```powershell
.venv\Scripts\python -m pip install pyinstaller
```

### 2. Build the executable

From the project root directory, run:

**Using Poetry:**
```powershell
poetry run pyinstaller --onefile --name clinostat-sim --console app\__main__.py
```

**Using venv directly:**
```powershell
.venv\Scripts\python -m PyInstaller --onefile --name clinostat-sim --console app\__main__.py
```

**Build options explained:**
- `--onefile` — packages everything into a single .exe file
- `--name clinostat-sim` — names the executable `clinostat-sim.exe`
- `--console` — keeps the console window (required for CLI apps)
- `app\__main__.py` — the entry point of the application

### 3. Find the executable

The built executable will be located at:
```
dist\clinostat-sim.exe
```

### 4. Run the executable

You can now run the program without Python or any dependencies installed:

```powershell
.\dist\clinostat-sim.exe sim --inner 0.25 --outer 4.0
.\dist\clinostat-sim.exe sweep-cmd --rpm-min 0.5 --rpm-max 4.0 --rpm-step 0.25
```

### 5. Distribution

The `clinostat-sim.exe` file in the `dist` folder is completely standalone and can be:
- Copied to any Windows machine (no Python required)
- Distributed to users who don't have Python installed
- Run from any directory

**File size note:** The executable will be 15–25 MB because it bundles Python and all dependencies.

### Advanced options

**Reduce executable size** by excluding unnecessary modules:
```powershell
poetry run pyinstaller --onefile --name clinostat-sim --console --exclude-module tkinter app\__main__.py
```

**Add an icon** to the executable:
```powershell
poetry run pyinstaller --onefile --name clinostat-sim --console --icon=icon.ico app\__main__.py
```

**Hide console window** (not recommended for CLI apps, but useful for GUI wrappers):
```powershell
poetry run pyinstaller --onefile --name clinostat-sim --noconsole app\__main__.py
```

### Troubleshooting the build

**Issue:** `ModuleNotFoundError` when running the .exe

**Solution:** PyInstaller may miss some dynamic imports. Create a `.spec` file for more control:

1. Generate a spec file:
   ```powershell
   poetry run pyi-makespec --onefile --name clinostat-sim app\__main__.py
   ```

2. Edit `clinostat-sim.spec` and add hidden imports:
   ```python
   hiddenimports=['numpy', 'matplotlib', 'click', 'openpyxl']
   ```

3. Build using the spec file:
   ```powershell
   poetry run pyinstaller clinostat-sim.spec
   ```

**Issue:** Antivirus flags the executable

**Solution:** This is a common false positive with PyInstaller executables. You can:
- Add an exception in your antivirus software
- Sign the executable with a code signing certificate (for distribution)
- Build with `--debug all` to help antivirus software analyze the file

## Platform notes

### macOS

If plots don't display interactively, you may need a matplotlib backend that supports GUI windows. The default (`macosx` backend) works out of the box on most setups. If you see errors, try:

```bash
pip install pyobjc-framework-Cocoa
```

### Linux (headless / SSH)

If running on a server without a display, always use `--save` to write plots to files. If you need interactive display over SSH, configure X11 forwarding:

```bash
ssh -X user@server
```

Or set the Agg backend for non-interactive use:

```bash
export MPLBACKEND=Agg
poetry run python -m app sim --inner 0.25 --outer 4.0 --save ./output
```

### Windows

Use PowerShell or Command Prompt. Replace `python3` with `python` in all commands.

**Recommended approach** — use the virtual environment directly:

```powershell
.venv\Scripts\python -m app sim --inner 0.25 --outer 4.0
```

If using Poetry and it's not recognized after installation, restart your terminal or add Poetry to PATH:

```powershell
$env:PATH += ";$env:APPDATA\Python\Scripts"
```

Or use the full path:

```powershell
& "$env:APPDATA\Python\Scripts\poetry" run python -m app sim --inner 0.25 --outer 4.0
```

## Troubleshooting

### Poetry installation fails or dependencies won't install

**Issue**: `poetry install` exits with an error code, or packages appear to install but aren't actually available.

**Solution**: Use pip directly to install dependencies:

```bash
# Windows
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install numpy matplotlib click openpyxl

# macOS/Linux
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install numpy matplotlib click openpyxl
```

### Poetry environment contains invalid distribution

**Issue**: Error message about "invalid distribution" or corrupted pip installation.

**Solution**: Remove the corrupted virtual environment and recreate:

```bash
# Windows
rm -rf .venv
python -m venv .venv

# macOS/Linux
rm -rf .venv
python3 -m venv .venv
```

Then install dependencies using pip as shown above.

### ModuleNotFoundError when running the app

**Issue**: `ModuleNotFoundError: No module named 'numpy'` (or other packages)

**Solution**: Ensure you're using the virtual environment's Python interpreter:

```bash
# Windows - use full path to venv Python
.venv\Scripts\python -m app sim --inner 0.25 --outer 4.0

# macOS/Linux
.venv/bin/python -m app sim --inner 0.25 --outer 4.0
```

### Poetry command not found

**Issue**: `poetry: command not found` or `'poetry' is not recognized`

**Solution**:

**Windows**: Add Poetry to your PATH or use the full path:
```powershell
& "$env:APPDATA\Python\Scripts\poetry" --version
```

**macOS/Linux**: Add Poetry to your shell configuration:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell or run `source ~/.bashrc` (or `~/.zshrc` on macOS).

## Extending with custom speed profiles

The simulation engine accepts any function that maps time values to angular velocities — not just constant RPMs. To create a custom speed profile, write a function matching the `SpeedFunction` signature:

```python
from app.engine import simulate, constant_rpm
import numpy as np

# Example: sinusoidal speed variation
def sinusoidal_speed(base_rpm, amplitude_rpm, period_s):
    base = base_rpm * 2 * np.pi / 60
    amp = amplitude_rpm * 2 * np.pi / 60
    def speed(t):
        return base + amp * np.sin(2 * np.pi * t / period_s)
    return speed

result = simulate(
    inner_speed=sinusoidal_speed(0.25, 0.1, 60.0),
    outer_speed=constant_rpm(4.0),
    duration=3000,
)
print(f"Magnitude: {result.magnitude:.6f} m/s²")
print(f"Distribution: {result.dist_score}/1000")
```

No changes to the engine are needed — just pass your callable.

## Project structure

```
app/
  __init__.py        # Package version
  __main__.py        # Entry point
  cli.py             # Click CLI (sim, sweep-cmd)
  engine.py          # Simulation core: rotation math, metrics, sweep
  lattice.py         # Fibonacci hemisphere lattice, distribution scoring
  visualize.py       # Matplotlib plots (trajectory, hemisphere, time series, heatmaps)
```
