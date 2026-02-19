"""Fibonacci hemisphere lattice and distribution score computation."""

import numpy as np


def fibonacci_hemisphere(n: int = 1000) -> np.ndarray:
    """Generate n evenly-spaced points on the upper hemisphere using Fibonacci spiral.

    Returns array of shape (n, 3) with unit vectors where z >= 0.
    """
    golden_ratio = (1 + np.sqrt(5)) / 2
    i = np.arange(n)
    # Polar angle from pole (z=1) to equator (z=0)
    theta = np.arccos(1 - i / n)
    # Azimuthal angle using golden angle spacing
    phi = 2 * np.pi * i / golden_ratio

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    return np.column_stack([x, y, z])


def distribution_score(
    accel: np.ndarray,
    lattice: np.ndarray | None = None,
    n_points: int = 1000,
) -> tuple[int, np.ndarray]:
    """Count how many Fibonacci lattice points are closest to at least one
    acceleration vector.

    Args:
        accel: Acceleration vectors, shape (N, 3).
        lattice: Precomputed lattice points, shape (n_points, 3). Generated if None.
        n_points: Number of lattice points (used only if lattice is None).

    Returns:
        Tuple of (score, hit_counts) where score is the number of unique lattice
        points hit (0 to n_points) and hit_counts is shape (n_points,) with the
        count of hits per lattice point.
    """
    if lattice is None:
        lattice = fibonacci_hemisphere(n_points)

    # Normalize acceleration vectors to unit vectors
    norms = np.linalg.norm(accel, axis=1, keepdims=True)
    # Avoid division by zero for near-zero vectors
    norms = np.maximum(norms, 1e-12)
    normalized = accel / norms

    # Flip vectors pointing to -Z hemisphere (symmetry: direction and opposite are equivalent)
    mask = normalized[:, 2] < 0
    normalized[mask] *= -1

    # Process in chunks to bound memory usage
    chunk_size = 10000
    hit_counts = np.zeros(len(lattice), dtype=np.int64)

    for start in range(0, len(normalized), chunk_size):
        chunk = normalized[start : start + chunk_size]
        # Dot product with all lattice points: (chunk_size, n_points)
        dots = chunk @ lattice.T
        # Closest lattice point for each vector
        closest = np.argmax(dots, axis=1)
        # Increment hit counts
        np.add.at(hit_counts, closest, 1)

    score = int(np.count_nonzero(hit_counts))
    return score, hit_counts
