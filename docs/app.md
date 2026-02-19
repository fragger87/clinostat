# 3D Clinostat Microgravity Simulator — Implementation Plan

## Context

The research group uses a 3D clinostat (two independently rotating frames) to simulate microgravity. Quality is measured by two metrics: **magnitude** (time-averaged acceleration, lower = better) and **distribution score** (how uniformly the gravity vector covers a hemisphere, higher = better). This app will let researchers simulate any RPM combination, visualize results, and sweep RPM grids to find optimal settings — replacing manual computation with an interactive tool.

## Project Structure

```
clinostat-sim/
  pyproject.toml                # Poetry config, deps: numpy, matplotlib, click
  app/
    __init__.py                 # __version__ = "0.1.0"
    __main__.py                 # Entry point: from app.cli import main; main()
    cli.py                      # Click CLI: `simulate` and `sweep` commands
    engine.py                   # Core simulation: rotation math, metrics, sweep
    lattice.py                  # Fibonacci hemisphere lattice + distribution scoring
    visualize.py                # All matplotlib plotting (4 plot types)
```

## Implementation Steps

### Step 1: Project scaffold + Poetry setup
- Create `pyproject.toml` with deps: `numpy`, `matplotlib`, `click`, Python `>=3.9`
- Create `app/__init__.py`, `app/__main__.py`
- Run `poetry install`

### Step 2: `app/lattice.py` — Fibonacci lattice + distribution score
- `fibonacci_hemisphere(n=1000) -> np.ndarray` — generates n unit vectors on the +Z hemisphere using Fibonacci spiral
- `distribution_score(accel, lattice=None, n_points=1000) -> int` — normalizes acceleration vectors, finds closest lattice point for each via chunked matrix multiply (keeps memory bounded), returns count of unique lattice points hit

### Step 3: `app/engine.py` — Simulation core
- **Speed function pattern**: `SpeedFunction = Callable[[np.ndarray], np.ndarray]` — takes time array, returns angular velocity array (rad/s). This enables future variable-speed profiles with zero engine changes.
- `constant_rpm(rpm) -> SpeedFunction` — factory for constant speed
- `integrate_angles(speed_fn, t) -> np.ndarray` — cumulative trapezoidal integration of speed over time (works for both constant and variable speeds)
- `rotation_matrices_x(angles)` / `rotation_matrices_z(angles)` — vectorized (N,3,3) rotation matrix builders
- `simulate(inner_speed, outer_speed, duration, dt=0.1) -> SimResult` — returns dataclass with `t`, `accel` (N,3), `magnitude`, `distribution_score`
- `sweep(inner_rpms, outer_rpms, duration, dt=0.1) -> SweepResult` — iterates RPM grid, returns dataclass with `magnitudes` (M,K) and `distributions` (M,K) matrices

### Step 4: `app/visualize.py` — Matplotlib plots
- `plot_trajectory_3d(accel) -> Figure` — 3D line/scatter of acceleration vector path
- `plot_hemisphere_distribution(accel, lattice) -> Figure` — hemisphere scatter colored by hit count
- `plot_time_series(t, accel) -> Figure` — stacked x(t), y(t), z(t) subplots
- `plot_sweep_heatmaps(sweep_result) -> Figure` — side-by-side magnitude + distribution heatmaps

All functions return `Figure` without calling `plt.show()` — the CLI controls display.

### Step 5: `app/cli.py` — CLI with Click
- `simulate` command: `--inner`, `--outer`, `--duration`, `--dt`, `--save`
- `sweep` command: `--rpm-min`, `--rpm-max`, `--rpm-step`, `--duration`, `--dt`, `--save`
- Prints metrics to terminal, shows/saves plots

**Usage:**
```
python -m app simulate --inner 0.25 --outer 4.0 --duration 3000
python -m app sweep --rpm-min 0.125 --rpm-max 4.0 --rpm-step 0.25 --duration 3000
```

## Key Design Decisions

1. **Speed functions over RPM values**: The engine accepts `Callable[[np.ndarray], np.ndarray]` — any function mapping time to angular velocity. `constant_rpm()` is the factory for now. Future variable profiles (sinusoidal, ramp, etc.) require zero engine changes.

2. **Fully vectorized numpy**: Rotation matrices built as (N,3,3) arrays, combined via `np.einsum`. Single simulation (30k timesteps) runs in under 1 second.

3. **Chunked distribution scoring**: Process 10k timesteps at a time to keep memory under ~80MB regardless of simulation length.

4. **Sweep is a simple loop**: 32x32 grid = ~1024 simulations, each <1s. Total ~15-20 min for full sweep. Parallelization deferred until needed.

## Verification

- Simulate inner=0.25, outer=4.0, duration=3000 — magnitude should be ~0.00132 (matches Data Sheet 1)
- Simulate equal RPMs (e.g., 2.0:2.0) — magnitude should be ~0.5 (worst case, diagonal of heatmap)
- Small sweep (4x4 grid) — verify heatmap pattern matches reference: off-diagonal corners good, diagonal bad
- All plots render without errors
