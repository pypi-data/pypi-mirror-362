from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pct_tools._ext

if TYPE_CHECKING:
    from typing import Any, Sequence


def compute_ATAx(
    x: np.ndarray[Any, np.dtype[np.float32]], filenames: Sequence[str]
) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Compute the multiplication A.T * A * x.

    This is used in the computation of the largest eigenvalue of the matrix A via the power method.

    Args:
        x: A column vector of shape (m, 1).
        filenames: Names of the files the compressed matrices are stored in.

    Returns:
        The resulting vector of shape (m, 1).
    """
    return pct_tools._ext.compute_ATAx(x, filenames)
