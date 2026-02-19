"""Matplotlib visualization functions for clinostat simulation results."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from app.engine import SweepResult
from app.lattice import fibonacci_hemisphere


def plot_trajectory_3d(accel: np.ndarray) -> Figure:
    """3D plot of the acceleration vector trajectory.

    Args:
        accel: Acceleration vectors, shape (N, 3).

    Returns:
        Matplotlib Figure.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Subsample if too many points for legible plotting
    step = max(1, len(accel) // 5000)
    a = accel[::step]

    ax.plot(a[:, 0], a[:, 1], a[:, 2], linewidth=0.3, alpha=0.6)
    ax.set_xlabel("X (m/s²)")
    ax.set_ylabel("Y (m/s²)")
    ax.set_zlabel("Z (m/s²)")
    ax.set_title("Acceleration Vector Trajectory")

    # Draw reference sphere at radius g
    g = np.linalg.norm(accel[0])
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    xs = g * np.outer(np.cos(u), np.sin(v))
    ys = g * np.outer(np.sin(u), np.sin(v))
    zs = g * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(xs, ys, zs, color="gray", alpha=0.1, linewidth=0.3)

    return fig


def plot_hemisphere_distribution(
    accel: np.ndarray,
    hit_counts: np.ndarray,
    lattice: np.ndarray | None = None,
    n_points: int = 1000,
) -> Figure:
    """3D scatter plot of Fibonacci lattice points colored by hit count.

    Args:
        accel: Acceleration vectors, shape (N, 3). (unused, kept for interface consistency)
        hit_counts: Hit counts per lattice point, shape (n_points,).
        lattice: Precomputed lattice. Generated if None.
        n_points: Number of lattice points (used only if lattice is None).

    Returns:
        Matplotlib Figure.
    """
    if lattice is None:
        lattice = fibonacci_hemisphere(n_points)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Color: gray for unhit, colormap for hit points
    colors = np.where(hit_counts > 0, hit_counts, np.nan)

    sc = ax.scatter(
        lattice[:, 0],
        lattice[:, 1],
        lattice[:, 2],
        c=colors,
        cmap="hot_r",
        s=10,
        alpha=0.8,
        edgecolors="none",
    )

    # Plot unhit points in gray
    unhit = hit_counts == 0
    if np.any(unhit):
        ax.scatter(
            lattice[unhit, 0],
            lattice[unhit, 1],
            lattice[unhit, 2],
            c="lightgray",
            s=5,
            alpha=0.3,
            edgecolors="none",
        )

    fig.colorbar(sc, ax=ax, label="Hit count", shrink=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Distribution on Hemisphere")

    return fig


def plot_time_series(t: np.ndarray, accel: np.ndarray) -> Figure:
    """Stacked subplots of X, Y, Z acceleration components over time.

    Args:
        t: Time values, shape (N,).
        accel: Acceleration vectors, shape (N, 3).

    Returns:
        Matplotlib Figure.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
    labels = ["X", "Y", "Z"]

    # Subsample for plotting performance
    step = max(1, len(t) // 10000)
    ts = t[::step]
    a = accel[::step]

    for i, (ax, label) in enumerate(zip(axes, labels)):
        ax.plot(ts, a[:, i], linewidth=0.4)
        ax.set_ylabel(f"{label} (m/s²)")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Time (s)")
    axes[0].set_title("Acceleration Components Over Time")
    fig.tight_layout()

    return fig


def plot_sweep_heatmaps(result: SweepResult) -> Figure:
    """Side-by-side heatmaps of magnitude and distribution score.

    Args:
        result: SweepResult from an RPM sweep.

    Returns:
        Matplotlib Figure.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Magnitude heatmap
    im1 = ax1.imshow(
        result.magnitudes,
        origin="lower",
        aspect="auto",
        cmap="RdYlBu_r",
        extent=[
            result.outer_rpms[0],
            result.outer_rpms[-1],
            result.inner_rpms[0],
            result.inner_rpms[-1],
        ],
    )
    fig.colorbar(im1, ax=ax1, label="Magnitude (m/s²)")
    ax1.set_xlabel("Outer RPM")
    ax1.set_ylabel("Inner RPM")
    ax1.set_title("Time-Averaged Acceleration Magnitude\n(lower = better)")

    # Distribution score heatmap
    im2 = ax2.imshow(
        result.distributions,
        origin="lower",
        aspect="auto",
        cmap="RdYlBu",
        extent=[
            result.outer_rpms[0],
            result.outer_rpms[-1],
            result.inner_rpms[0],
            result.inner_rpms[-1],
        ],
    )
    fig.colorbar(im2, ax=ax2, label="Distribution Score")
    ax2.set_xlabel("Outer RPM")
    ax2.set_ylabel("Inner RPM")
    ax2.set_title("Distribution Score\n(higher = better)")

    fig.tight_layout()

    return fig
