from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

import pct_tools._ext

from .io import ShuffleMethod

if TYPE_CHECKING:
    from typing import Any


def compute_matrix_elements(
    x: np.ndarray[Any, np.dtype[np.float32]],
    y: np.ndarray[Any, np.dtype[np.float32]],
    z: np.ndarray[Any, np.dtype[np.float32]],
    x_boundaries: np.ndarray[Any, np.dtype[np.float32]],
    y_boundaries: np.ndarray[Any, np.dtype[np.float32]],
    z_boundaries: np.ndarray[Any, np.dtype[np.float32]],
    img_shape: tuple,
    coordinate_origin: tuple,
    pixel_width: float,
    slice_thickness: float,
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute the matrix elements for a given proton trajectory.

    Args:
        x: The x-coordinates of the proton trajectories.
        y: The y-coordinates of the proton trajectories.
        z: The z-coordinates of the proton trajectories.
        x_boundaries: The x-coordinates of the boundaries of the voxels.
        y_boundaries: The y-coordinates of the boundaries of the voxels.
        z_boundaries: The z-coordinates of the boundaries of the voxels.
        img_shape: The shape of the image.
        coordinate_origin: The origin of the image.
        pixel_width: The width of the pixels.
        slice_thickness: The thickness of the slices.

    Returns:
        The 3D array of matrix elements for the given proton trajectory.
    """
    return pct_tools._ext.compute_matrix_elements(
        x,
        y,
        z,
        x_boundaries,
        y_boundaries,
        z_boundaries,
        img_shape,
        coordinate_origin,
        pixel_width,
        slice_thickness,
    )


def compute_and_store_sparse_matrix(
    filename: str,
    x: np.ndarray[Any, np.dtype[np.float32]],
    y: np.ndarray[Any, np.dtype[np.float32]],
    z: np.ndarray[Any, np.dtype[np.float32]],
    img_shape: tuple,
    coordinate_origin: tuple,
    pixel_width: float,
    slice_thickness: float,
    verbosity_level: int = 0,
    n_threads: int = 8,
    compression_level: int = 9,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
) -> None:
    """Compute the matrix elements for a given block of proton trajectories.

    Args:
        filename: The filename of the output file.
        x: The x-coordinates of the proton trajectories.
        y: The y-coordinates of the proton trajectories.
        z: The z-coordinates of the proton trajectories.
        img_shape: The shape of the image.
        coordinate_origin: The origin of the image.
        pixel_width: The width of the pixels.
        slice_thickness: The thickness of the slices.
        verbosity_level: The verbosity level.
        n_threads: The number of threads to use.
        compression_level: The compression level.
        shuffle_method: The Blosc shuffle method. Default is byte shuffling.
    """
    return pct_tools._ext.compute_and_store_sparse_matrix(
        filename,
        x,
        y,
        z,
        img_shape,
        coordinate_origin,
        pixel_width,
        slice_thickness,
        verbosity_level,
        n_threads,
        compression_level,
        shuffle_method,
    )
