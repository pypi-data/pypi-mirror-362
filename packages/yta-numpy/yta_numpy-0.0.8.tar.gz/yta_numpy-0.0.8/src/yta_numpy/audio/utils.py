"""
Utils to transform numpy arrays to the
desired format.

Some libraries need the audio to have the
data intercalated if stereo, which means
that the information is: LRLRLRLR... (or
RLRLRLRL...) for the different channels 
(R = right, L = left).
"""
from typing import Union

import numpy as np


def _to_dtype(
    audio: np.ndarray,
    dtype: np.dtype = np.float32,
    is_mono: Union[bool, None] = None
):
    """
    Transform the given 'audio' numpy array to
    one with the given 'dtype' with the shape
    (n_samples, n_channels). It will be mono
    if the 'is_mono' attribute is true or
    stereo if false.

    When we want a float dtype as the output
    type, the range of values will be always
    [-1.0, 1.0], which is the value used by all
    the libraries we are interacting with when
    handling audio numpy arrays.

    The 'dtype' we handle, by now, are these:
    - `np.int16`
    - `np.int32`
    - `np.float32`
    - `np.float64`

    And these are the conversions we handle:
    - `np.int32` to `np.int16`
    - `np.int32` to `np.float32`
    - `np.int16` to `np.float32`
    - `np.float32` to `np.int16`
    - `np.float64` to `np.int16`
    - `np.float64` to `np.float32`

    The maximum values are:
    - 2147483647 for `np.int32` 
    - 32767 for `np.int16`
    - 3.4^38 for `np.float32`
    """
    ACCEPTED_DTYPE_COMBINATIONS = {
        frozenset([np.int32, np.int16]),
        frozenset([np.int32, np.float32]),
        frozenset([np.int16, np.float32]),
        frozenset([np.float32, np.int16]),
        frozenset([np.float64, np.int16]),
        frozenset([np.float64, np.float32]),
        # These ones below are just to force
        # the 2 dimensions array and the
        # _normalized values if float, but no
        # transformation actually
        frozenset([np.int16, np.int16]),
        frozenset([np.int32, np.int32]),
        frozenset([np.float32, np.float32]),
        frozenset([np.float64, np.float64])
    }

    if frozenset([audio.dtype.type, dtype]) not in ACCEPTED_DTYPE_COMBINATIONS:
        raise Exception(f'We cannot transform a "{audio.dtype.type}" numpy array to a "{dtype}" numpy array.')

    # Audio to (ns, nc) format, mono or stereo
    audio = _force_2_dimensions_audio(audio, is_mono)

    # To [-1.0, 1.0] if 'np.float32' or 'np.float64'
    audio = _normalize(audio)

    """
    We use the max value of the int type because
    the minimum is one unit bigger, and when
    multiplied by 1.0 would be higher the max,
    being out of the valid range.

    In the range [-32768, 32767], when compared
    with the [-1.0, 1.0] range, if we multiply
    1.0 by the absolute minimum, the result,
    1.0 * 32768 = 32768, would be greater than
    the maximum (32767). Thats why we will use
    the maximum for the calculations, even
    though we will never be able to obtain the
    -32768 value back (-1.0 * 32767 = -32767).
    The same happens with the other int ranges.
    """

    return (
        # from 'np.int32' to 'np.int16'
        int32_to_int16(audio)
        if (
            audio.dtype == np.int32 and
            dtype == np.int16
        ) else
        # from 'np.int32' to 'np.float32' [-1.0, 1.0]
        int32_to_float32(audio)
        if (
            audio.dtype == np.int32 and
            dtype == np.float32
        ) else
        # from 'np.int16' to 'np.float32' [-1.0, 1.0]
        int16_to_float32(audio)
        if (
            audio.dtype == np.int16 and
            dtype == np.float32
        ) else
        # from 'np.float32' [-1.0, 1.0] to 'np.int16'
        float32_to_int16(audio)
        if (
            audio.dtype == np.float32 and
            dtype == np.int16
        ) else
        # from 'np.float64' [-1.0, 1.0] to 'np.float32' [-1.0, 1.0]
        float64_to_float32(audio)
        if (
            audio.dtype == np.float64 and
            dtype == np.float32
        ) else
        # from 'np.float64' [-1.0, 1.0] to 'np.int16'
        float64_to_int16(audio)
        if (
            audio.dtype == np.float64 and
            dtype == np.int16
        ) else
        # no conversion needed (first return actually)
        audio
    )

def int32_to_int16(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is an
    int32 numpy array, into an int16 numpy
    array with the same shape and dimensions.
    """
    # TODO: What about this code below
    # extracted from here:
    # https://stackoverflow.com/a/55475799
    # = (audio >> 16).astype(np.int16)   
    return np.round(
        (audio.astype(np.float64) / np.iinfo(np.int32).max) * np.iinfo(np.int16).max
    ).astype(np.int16)

def int32_to_float32(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is an
    int32 numpy array, into a float32 numpy
    array with the same shape and dimensions.
    """
    return audio.astype(np.float32) / abs(np.iinfo(np.int32).min)

def int16_to_float32(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is an
    int16 numpy array, into a float32 numpy
    array with the same shape and dimensions.
    """
    return audio.astype(np.float32) / abs(np.iinfo(np.int16).min)

def float32_to_int16(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is a
    float32 numpy array, into an int16 numpy
    array with the same shape and dimensions.

    The array will be _normalized if needed
    before the conversion.
    """
    return (_normalize(audio) * np.iinfo(np.int16).max).round().astype(np.int16)

def float64_to_float32(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is a
    float64 numpy array, into a float32 numpy
    array with the same shape and dimensions.

    The array will be _normalized if needed
    before the conversion.
    """
    return _normalize(audio).astype(np.float32)

def float64_to_int16(
    audio: np.ndarray
) -> np.ndarray:
    """
    Transform the 'audio' given, that is a
    float64 numpy array, into an int16 numpy
    array with the same shape and dimensions.

    The array will be _normalized if needed
    before the conversion.
    """
    return (_normalize(audio) * np.iinfo(np.int16).max).round().astype(np.int16)

def _normalize(
    audio: np.ndarray
) -> np.ndarray:
    """
    _normalize the 'audio' provided if it is
    a non-_normalized float numpy array. This
    means that the values will be in the
    [-1.0, 1.0] range.
    """
    return (
        (audio / np.max(np.abs(audio))).astype(audio.dtype)
        if audio.dtype in [np.float32, np.float64] else
        audio
    )

def _force_2_dimensions_audio(
    audio: np.ndarray,
    is_mono: Union[bool, None] = None
) -> np.ndarray:
    """
    Force the 'audio' provided to be a numpy
    array with two dimensions (ns, nc) and
    mono or stereo according to the 'is_mono'
    attribute value provided.
    
    If 'is_mono' is None, the array type will
    not be modified, only the shape (if
    needed).
    """
    # from (ns) to (ns, nc) if needed
    audio = _force_2_dimensions(audio)

    return (
        # from stereo to mono (mean strategy)
        np.mean(audio, axis = 1, keepdims = True)
        if (
            is_mono is not None and
            is_mono and
            audio.shape[1] == 2
        ) else
        # from mono to stereo
        np.concatenate([audio, audio], axis = 1)
        if (
            is_mono is not None and
            not is_mono and
            audio.shape[1] == 1
        ) else
        audio
    )

def _force_2_dimensions(
    audio: np.ndarray
) -> np.ndarray:
    """
    Force the 'audio' provided to be a numpy
    array with two dimensions (ns, nc)
    """
    return (
        # same as audio.reshape(-1, 1)
        audio[:, np.newaxis]    
        if audio.ndim == 1 else
        audio
    )

def _remove_2nd_dimension(
    audio: np.ndarray
) -> np.ndarray:
    """
    Force the 'audio' provided to be a numpy
    array with only one dimension, removing
    the second one if needed.

    (!) Careful. This method doesn't consider
    mono or stereo sounds, just removes the
    second dimension without touching the 
    first one.
    """
    return (
        audio[:, 0]
        # We ignore if stereo or mono
        if audio.ndim == 2 else
        audio
    )