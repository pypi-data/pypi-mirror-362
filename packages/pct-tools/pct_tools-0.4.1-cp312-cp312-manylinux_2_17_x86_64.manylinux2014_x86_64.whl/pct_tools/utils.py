from __future__ import annotations

import pct_tools._ext
from pct_tools.io import ShuffleMethod


def subsample_matrix_vector_pair(
    input_path: str,
    projection: str,
    output_path: str,
    subsampling_ratio: float,
    pixel_width: float,
    *,
    seed: int = 0,
    compression_level: int = 9,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
    verbosity_level: int = 0,
) -> None:
    """Subsample matrix and b-vector for a given projection.

    Args:
        input_path: The path to the input matrices.
        projection: The projection to subsample.
        output_path: The path to the output matrices.
        subsampling_ratio: The subsampling ratio.
    """
    if seed < 0:
        raise ValueError("Seed must be a non-negative integer.")

    return pct_tools._ext.subsample_matrix_vector_pair(
        input_path,
        projection,
        output_path,
        subsampling_ratio,
        f"{pixel_width}mm",
        seed,
        compression_level,
        shuffle_method,
        verbosity_level,
    )


def recompress_matrix(
    filename: str,
    output: str,
    compression_level: int = 9,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
    verbosity_level: int = 0,
) -> None:
    """Recompress a matrix with a given compression level.

    Args:
        filename: The name of the file containing the matrix.
        output: The name of the output file.
        compression_level: The compression level to use when storing it.
    """
    return pct_tools._ext.recompress_matrix(
        filename, output, compression_level, shuffle_method, verbosity_level
    )


def recompress_matrix_lz4hc(
    filename: str,
    output: str,
    compression_level: int = 9,
    shuffle_method: ShuffleMethod = ShuffleMethod.BLOSC_SHUFFLE,
    verbosity_level: int = 0,
) -> None:
    """Recompress a matrix with a given compression level using delta storage.

    Args:
        filename: The name of the file containing the matrix.
        output: The name of the output file.
        compression_level: The compression level to use when storing it.
    """
    return pct_tools._ext.recompress_matrix_lz4hc(
        filename, output, compression_level, shuffle_method, verbosity_level
    )
