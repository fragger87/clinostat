"""Core simulation engine for 3D clinostat microgravity simulation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from app.lattice import distribution_score, fibonacci_hemisphere

# A speed function maps an array of time values (seconds) to angular velocities (rad/s).
SpeedFunction = Callable[[np.ndarray], np.ndarray]


def constant_rpm(rpm: float) -> SpeedFunction:
    """Return a speed function that yields constant angular velocity."""
    omega = rpm * 2.0 * np.pi / 60.0

    def _speed(t: np.ndarray) -> np.ndarray:
        return np.full_like(t, omega, dtype=np.float64)

    return _speed


def integrate_angles(speed_fn: SpeedFunction, t: np.ndarray) -> np.ndarray:
    """Compute cumulative angle by integrating a speed function over time.

    Uses cumulative trapezoidal integration. For constant speed this reduces
    to omega * t (exact).
    """
    omega = speed_fn(t)
    dt = np.diff(t)
    avg_omega = 0.5 * (omega[:-1] + omega[1:])
    return np.concatenate([[0.0], np.cumsum(avg_omega * dt)])


def _rotation_matrices_x(angles: np.ndarray) -> np.ndarray:
    """Build (N, 3, 3) rotation matrices about the X axis."""
    c, s = np.cos(angles), np.sin(angles)
    N = len(angles)
    R = np.zeros((N, 3, 3))
    R[:, 0, 0] = 1.0
    R[:, 1, 1] = c
    R[:, 1, 2] = -s
    R[:, 2, 1] = s
    R[:, 2, 2] = c
    return R


def _rotation_matrices_z(angles: np.ndarray) -> np.ndarray:
    """Build (N, 3, 3) rotation matrices about the Z axis."""
    c, s = np.cos(angles), np.sin(angles)
    N = len(angles)
    R = np.zeros((N, 3, 3))
    R[:, 0, 0] = c
    R[:, 0, 1] = -s
    R[:, 1, 0] = s
    R[:, 1, 1] = c
    R[:, 2, 2] = 1.0
    return R


@dataclass
class SimResult:
    """Result of a single clinostat simulation."""

    t: np.ndarray  # (N,) time values in seconds
    accel: np.ndarray  # (N, 3) acceleration vectors
    magnitude: float  # L2 norm of the time-averaged acceleration
    dist_score: int  # number of Fibonacci lattice points hit
    hit_counts: np.ndarray  # (n_points,) hits per lattice point


@dataclass
class SweepResult:
    """Result of an RPM sweep across a grid."""

    inner_rpms: np.ndarray  # (M,)
    outer_rpms: np.ndarray  # (K,)
    magnitudes: np.ndarray  # (M, K)
    distributions: np.ndarray  # (M, K)


def simulate(
    inner_speed: SpeedFunction,
    outer_speed: SpeedFunction,
    duration: float,
    dt: float = 0.1,
    g0: np.ndarray | None = None,
) -> SimResult:
    """Run a 3D clinostat simulation.

    The clinostat has an inner frame rotating about X and an outer frame
    rotating about Z. The effective acceleration at each timestep is:
        a(t) = R_z(outer_angle(t)) @ R_x(inner_angle(t)) @ g0

    Args:
        inner_speed: Speed function for the inner frame.
        outer_speed: Speed function for the outer frame.
        duration: Simulation duration in seconds.
        dt: Timestep in seconds.
        g0: Gravity vector. Defaults to [0, 0, 9.81].

    Returns:
        SimResult with time series, acceleration vectors, and quality metrics.
    """
    if g0 is None:
        g0 = np.array([0.0, 0.0, 9.81])

    t = np.arange(0, duration, dt)

    # Integrate speed functions to get cumulative angles
    inner_angles = integrate_angles(inner_speed, t)
    outer_angles = integrate_angles(outer_speed, t)

    # Build rotation matrices: (N, 3, 3)
    R_inner = _rotation_matrices_x(inner_angles)
    R_outer = _rotation_matrices_z(outer_angles)

    # Apply combined rotation to gravity vector for all timesteps:
    # a[i] = R_outer[i] @ R_inner[i] @ g0
    accel = np.einsum("nij,njk,k->ni", R_outer, R_inner, g0)

    # Compute magnitude of time-averaged acceleration
    a_avg = np.mean(accel, axis=0)
    magnitude = float(np.linalg.norm(a_avg))

    # Compute distribution score
    lattice = fibonacci_hemisphere(1000)
    score, hit_counts = distribution_score(accel, lattice)

    return SimResult(
        t=t,
        accel=accel,
        magnitude=magnitude,
        dist_score=score,
        hit_counts=hit_counts,
    )


def sweep(
    inner_rpms: np.ndarray,
    outer_rpms: np.ndarray,
    duration: float,
    dt: float = 0.1,
    progress_callback: Callable[[int, int], None] | None = None,
) -> SweepResult:
    """Sweep a grid of RPM combinations and compute metrics for each.

    Args:
        inner_rpms: Array of inner frame RPM values.
        outer_rpms: Array of outer frame RPM values.
        duration: Simulation duration in seconds for each combination.
        dt: Timestep in seconds.
        progress_callback: Optional callback(current, total) for progress reporting.

    Returns:
        SweepResult with magnitude and distribution matrices.
    """
    M, K = len(inner_rpms), len(outer_rpms)
    magnitudes = np.zeros((M, K))
    distributions = np.zeros((M, K), dtype=np.int64)
    total = M * K

    for i, inner_rpm in enumerate(inner_rpms):
        for j, outer_rpm in enumerate(outer_rpms):
            result = simulate(
                constant_rpm(inner_rpm),
                constant_rpm(outer_rpm),
                duration,
                dt,
            )
            magnitudes[i, j] = result.magnitude
            distributions[i, j] = result.dist_score

            if progress_callback is not None:
                progress_callback(i * K + j + 1, total)

    return SweepResult(
        inner_rpms=inner_rpms,
        outer_rpms=outer_rpms,
        magnitudes=magnitudes,
        distributions=distributions,
    )
