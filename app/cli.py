"""CLI interface for the 3D clinostat simulator."""

from __future__ import annotations

import os
import sys

import click
import matplotlib.pyplot as plt
import numpy as np

from app.engine import SimResult, SweepResult, constant_rpm, simulate, sweep
from app.export import export_sweep_xlsx
from app.lattice import fibonacci_hemisphere
from app.visualize import (
    plot_hemisphere_distribution,
    plot_sweep_heatmaps,
    plot_time_averaged_acceleration,
    plot_time_series,
    plot_trajectory_3d,
)


def _save_or_show(fig, save_dir: str | None, filename: str) -> None:
    """Save figure to directory or show interactively."""
    if save_dir is not None:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, filename)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        click.echo(f"  Saved: {path}")
        plt.close(fig)


@click.group()
def main():
    """3D Clinostat Microgravity Simulator."""
    pass


@main.command()
@click.option("--inner", type=float, required=True, help="Inner frame RPM.")
@click.option("--outer", type=float, required=True, help="Outer frame RPM.")
@click.option("--duration", type=float, default=3000, show_default=True, help="Duration in seconds.")
@click.option("--dt", type=float, default=0.1, show_default=True, help="Timestep in seconds.")
@click.option("--save", type=str, default=None, help="Directory to save figures (shows interactively if omitted).")
def sim(inner, outer, duration, dt, save):
    """Run a single clinostat simulation for one RPM pair."""
    click.echo(f"Simulating: inner={inner} RPM, outer={outer} RPM, duration={duration}s, dt={dt}s")

    result = simulate(constant_rpm(inner), constant_rpm(outer), duration, dt)

    click.echo(f"\nResults:")
    click.echo(f"  Magnitude (time-avg accel): {result.magnitude:.6f} m/s^2")
    click.echo(f"  Distribution score:         {result.dist_score} / 1000")

    click.echo("\nGenerating plots...")
    lattice = fibonacci_hemisphere(1000)

    fig1 = plot_trajectory_3d(result.accel)
    fig2 = plot_hemisphere_distribution(result.accel, result.hit_counts, lattice)
    fig3 = plot_time_series(result.t, result.accel)
    fig4 = plot_time_averaged_acceleration(result.t, result.accel)

    _save_or_show(fig1, save, "trajectory_3d.png")
    _save_or_show(fig2, save, "hemisphere_distribution.png")
    _save_or_show(fig3, save, "time_series.png")
    _save_or_show(fig4, save, "time_averaged_acceleration.png")

    if save is None:
        plt.show()
    else:
        click.echo("Done.")


@main.command()
@click.option("--inner-min", type=float, default=0.125, show_default=True, help="Minimum inner frame RPM.")
@click.option("--inner-max", type=float, default=4.0, show_default=True, help="Maximum inner frame RPM.")
@click.option("--inner-step", type=float, default=0.125, show_default=True, help="Inner frame RPM step size.")
@click.option("--outer-min", type=float, default=0.125, show_default=True, help="Minimum outer frame RPM.")
@click.option("--outer-max", type=float, default=4.0, show_default=True, help="Maximum outer frame RPM.")
@click.option("--outer-step", type=float, default=0.125, show_default=True, help="Outer frame RPM step size.")
@click.option("--duration", type=float, default=3000, show_default=True, help="Duration in seconds per simulation.")
@click.option("--dt", type=float, default=0.1, show_default=True, help="Timestep in seconds.")
@click.option("--save", type=str, default=None, help="Directory to save figures and XLSX (shows interactively if omitted).")
@click.option("--xlsx", "xlsx_path", type=str, default=None, help="Path to save results as .xlsx (default: <save>/sweep_results.xlsx when --save is set).")
def sweep_cmd(inner_min, inner_max, inner_step, outer_min, outer_max, outer_step, duration, dt, save, xlsx_path):
    """Sweep a grid of RPM combinations and generate heatmaps."""
    inner_rpms = np.arange(inner_min, inner_max + inner_step / 2, inner_step)
    outer_rpms = np.arange(outer_min, outer_max + outer_step / 2, outer_step)
    total = len(inner_rpms) * len(outer_rpms)

    click.echo(f"Sweeping {len(inner_rpms)}x{len(outer_rpms)} = {total} combinations")
    click.echo(f"  Inner RPM range: {inner_min} to {inner_max}, step {inner_step}")
    click.echo(f"  Outer RPM range: {outer_min} to {outer_max}, step {outer_step}")
    click.echo(f"  Duration: {duration}s, dt: {dt}s")

    def progress(current, total):
        pct = current / total * 100
        sys.stdout.write(f"\r  Progress: {current}/{total} ({pct:.0f}%)")
        sys.stdout.flush()
        if current == total:
            sys.stdout.write("\n")

    result = sweep(inner_rpms, outer_rpms, duration, dt, progress_callback=progress)

    # Find best combinations
    min_mag_idx = np.unravel_index(np.argmin(result.magnitudes), result.magnitudes.shape)
    max_dist_idx = np.unravel_index(np.argmax(result.distributions), result.distributions.shape)

    click.echo(f"\nBest by magnitude (lowest):")
    click.echo(
        f"  Inner={result.inner_rpms[min_mag_idx[0]]:.3f} RPM, "
        f"Outer={result.outer_rpms[min_mag_idx[1]]:.3f} RPM, "
        f"Magnitude={result.magnitudes[min_mag_idx]:.6f} m/s^2"
    )
    click.echo(f"\nBest by distribution (highest):")
    click.echo(
        f"  Inner={result.inner_rpms[max_dist_idx[0]]:.3f} RPM, "
        f"Outer={result.outer_rpms[max_dist_idx[1]]:.3f} RPM, "
        f"Score={result.distributions[max_dist_idx]}"
    )

    # Export XLSX
    if xlsx_path is None and save is not None:
        xlsx_path = os.path.join(save, "sweep_results.xlsx")
    if xlsx_path is not None:
        saved = export_sweep_xlsx(result, xlsx_path)
        click.echo(f"\n  Saved XLSX: {saved}")

    click.echo("\nGenerating heatmaps...")
    fig = plot_sweep_heatmaps(result)
    _save_or_show(fig, save, "sweep_heatmaps.png")

    if save is None:
        plt.show()
    else:
        click.echo("Done.")
