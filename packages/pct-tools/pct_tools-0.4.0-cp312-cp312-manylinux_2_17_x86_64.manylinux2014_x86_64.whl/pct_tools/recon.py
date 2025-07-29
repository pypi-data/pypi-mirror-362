from __future__ import annotations

from typing import TYPE_CHECKING

import pct_tools._ext

if TYPE_CHECKING:
    from typing import Any, Sequence

    import numpy as np


def gradient_descent(
    x: np.ndarray[Any, np.dtype[np.float32]],
    step_size: float,
    matrix_filenames: Sequence[str],
    vector_filenames: Sequence[str],
    *,
    verbosity_level: int = 0,
    n_threads: int = 1,
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute gradient descent step.

    Args:
        x: A vector.
        step_size: The step size to be used in the descent.
        matrix_filenames: The filenames of the matrices.
        vector_filenames: The filenames of the vectors.

    Returns:
        A tuple that contains the updated vector and the sum of squared residuals.
    """

    return pct_tools._ext.gradient_descent(
        x, step_size, matrix_filenames, vector_filenames, verbosity_level, n_threads
    )


def gradient_descent_fast(
    x: np.ndarray[Any, np.dtype[np.float32]],
    step_size: float,
    matrix_filenames: Sequence[str],
    vector_filenames: Sequence[str],
    *,
    verbosity_level: int = 0,
    n_threads: int = 1,
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute gradient descent step.

    Args:
        x: A vector.
        step_size: The step size to be used in the descent.
        matrix_filenames: The filenames of the matrices.
        vector_filenames: The filenames of the vectors.

    Returns:
        A tuple that contains the updated vector and the sum of squared residuals.
    """

    return pct_tools._ext.gradient_descent_fast(
        x, step_size, matrix_filenames, vector_filenames, verbosity_level, n_threads
    )


def squared_residuals(
    x: np.ndarray[Any, np.dtype[np.float32]],
    matrix_filenames: Sequence[str],
    vector_filenames: Sequence[str],
    *,
    verbosity_level: int = 0,
    n_threads: int = 1,
) -> float:
    """Compute the squared residual norm for a given vector.

    Args:
        x: A vector.
        matrix_filenames: The filenames of the matrices.
        vector_filenames: The filenames of the vectors.

    Returns:
        The squared residual norm.
    """

    return pct_tools._ext.squared_residuals(x, matrix_filenames, vector_filenames, verbosity_level, n_threads)


def squared_residuals_fast(
    x: np.ndarray[Any, np.dtype[np.float32]],
    matrix_filenames: Sequence[str],
    vector_filenames: Sequence[str],
    *,
    verbosity_level: int = 0,
    n_threads: int = 1,
) -> float:
    """Compute the squared residual norm for a given vector.

    Args:
        x: A vector.
        matrix_filenames: The filenames of the matrices.
        vector_filenames: The filenames of the vectors.

    Returns:
        The squared residual norm.
    """

    return pct_tools._ext.squared_residuals_fast(
        x, matrix_filenames, vector_filenames, verbosity_level, n_threads
    )
