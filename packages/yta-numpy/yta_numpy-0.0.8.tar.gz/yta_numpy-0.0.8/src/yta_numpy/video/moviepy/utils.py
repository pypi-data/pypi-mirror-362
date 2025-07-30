"""
All these utils must be used with 
numpy arrays that are valid as moviepy
video frames.
"""
from typing import Union

import numpy as np


def _moviepy_normal_frame_has_all_colors(
    frame: 'np.ndarray',
    colors: list
) -> bool:
    """
    Check if the provided 'frame' has the
    also provided 'colors', that must be a
    list of RGB arrays. All the colors must
    be present in the frame.
    """
    frame_flat = frame.reshape(-1, 3)
    colors = np.array(colors)

    return all(
        np.any(
            np.all(frame_flat == color, axis = 1)
        )
        for color in colors
    )

def _moviepy_normal_frame_has_only_colors(
    frame: 'np.ndarray',
    colors: list
) -> bool:
    """
    Check if the provided 'frame' has only
    the also provided 'colors', that must
    be a list of RGB arrays. All the colors
    in the frame must be the ones provided
    as 'colors' parameter.
    """
    frame_flat = frame.reshape(-1, 3)
    colors = np.array(colors)

    return np.all(
        np.any(
            np.all(frame_flat[:, None] == colors, axis = 2),
            axis = 1
        )
    )


def _is_moviepy_normal_frame(
    frame: 'np.ndarray'
) -> bool:
    """
    Check if the provided 'frame' is a 
    valid moviepy normal video frame,
    which is:

    - `ndim == 3`
    - `shape[2] == 3`
    - `dtype == np.uint8`

    A valid frame would be like this:
    - `(720, 1080, 3)`
    """
    return (
        frame.ndim == 3 and
        frame.shape[2] == 3 and
        frame.dtype == np.uint8
    )

def _is_moviepy_mask_frame(
    frame: 'np.ndarray'
) -> bool:
    """
    Check if the provided 'frame' is a 
    valid moviepy mask video frame,
    which is:

    - `ndim == 2`
    - `dtype in [np.float32, np.float64]`
    - each value is in `[-1.0, 1.0]` range

    A valid frame would be like this:
    - `(720, 1080)`
    """
    return (
        frame.ndim == 2 and
        frame.dtype in [np.float32, np.float64] and
        #np.issubdtype(frame.dtype, np.floating) and
        (
            frame.min() >= 0.0 and
            frame.max() <= 1.0 
        )
    )


def _is_normalized(
    frame: 'np.ndarray'
):
    """
    Check if the provided frame is a a
    normalized one, which means that its
    type is .float64 or .float32 and that
    all values are between 0.0 and 1.0.
    """
    return (
        frame.dtype in (np.float64, np.float32) and
        np.all((frame >= 0.0) & (frame <= 1.0))
    )

def _is_not_normalized(
    frame: 'np.ndarray'
):
    """
    Check if the provided frame is not
    a normalized one, which means that
    its type is .uint8 and that all
    values are between 0 and 255.
    """
    return (
        # TODO: Maybe the type is not that one (?)
        frame.dtype == np.uint8 and
        np.all((frame >= 0) & (frame <= 255))
    )

def _invert(
    frame: np.ndarray
) -> Union['np.ndarray', None]:
    """
    Invert the provided array according
    to if it is a normalized or a not
    normalized one.
    """
    return (
        1.0 - frame
        if _is_normalized(frame) else
        255 - frame
        if _is_not_normalized(frame) else
        # TODO: Raise exception (?)
        None
    )