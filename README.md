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

This creates a virtual environment and installs all dependencies (`numpy`, `matplotlib`, `click`).

## Usage

All commands are run from the project root directory.

### Single simulation

Simulate one inner/outer RPM pair and visualize the results:

```bash
poetry run python -m app sim --inner 0.25 --outer 4.0
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

This generates three plots:
- `trajectory_3d.png` — 3D path of the acceleration vector
- `hemisphere_distribution.png` — which Fibonacci lattice points were hit
- `time_series.png` — X, Y, Z acceleration components over time

### RPM sweep (heatmaps)

Sweep a grid of inner/outer RPM combinations to find optimal settings:

```bash
poetry run python -m app sweep-cmd --rpm-min 0.5 --rpm-max 4.0 --rpm-step 0.25
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

Use PowerShell or Command Prompt. Replace `python3` with `python` in all commands:

```powershell
poetry run python -m app sim --inner 0.25 --outer 4.0
```

If `poetry` is not recognized after installation, restart your terminal or use the full path:

```powershell
%APPDATA%\Python\Scripts\poetry run python -m app sim --inner 0.25 --outer 4.0
```

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
