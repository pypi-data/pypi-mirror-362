from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

import pct_tools._ext

if TYPE_CHECKING:
    from typing import Any


def compute_mlp(
    phantom: str,
    z: np.ndarray[Any, np.dtype[np.float32]],
    h_in: float,
    theta_in: float,
    h_out: float,
    theta_out: float,
    *,
    n_threads: int = 8,
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute the most likley proton trajectory for a set of parameters.

    Args:
        phantom: The phantom to use.
        z: The z-coordinates of the proton trajectories.
        h_in: The transverse position at the entry detector.
        theta_in: The proton direction at the entry detector.
        h_out: The transverse position at the exit detector.
        theta_out: The proton direction at the exit detector.

    Returns:
        Array of most likely transverse positions along trajectory.
    """

    return pct_tools._ext.compute_mlp(phantom, z, h_in, theta_in, h_out, theta_out, n_threads)


def mlp(
    z: np.ndarray[Any, np.dtype[np.float32]],
    h_in: float,
    theta_in: float,
    h_out: float,
    theta_out: float,
    coefficients: list[float],
    *,
    n_threads: int = 8,
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute the most likley proton trajectory for a set of parameters.

    Args:
        z: The z-coordinates of the proton trajectories.
        h_in: The transverse position at the entry detector.
        theta_in: The proton direction at the entry detector.
        h_out: The transverse position at the exit detector.
        theta_out: The proton direction at the exit detector.
        coefficients: List of length 6. Fit parameters used in the 6th order fit to
            the inverse energy intergral.

    Returns:
        Array of most likely transverse positions along trajectory.
    """

    if len(coefficients) != 6:
        raise ValueError("The list of coefficients must be of length 6")

    return pct_tools._ext.mlp(z, h_in, theta_in, h_out, theta_out, coefficients, n_threads)
