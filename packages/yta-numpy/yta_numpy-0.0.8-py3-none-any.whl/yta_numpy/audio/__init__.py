"""
Module to handle the numpy arrays
related to audio files, maybe with
libraries like:

- `pydub`
- `librosa`
- `soundfile`
- `moviepy`
- ...
"""
from yta_numpy.audio.utils import _to_dtype, _remove_2nd_dimension
from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_constants.audio import StereoAudioFormatMode
from typing import Union

import numpy as np


class AudioNumpyHandler:
    """
    Class to wrap functionality related
    to audio numpy arrays.
    """

    @staticmethod
    def to_dtype(
        audio: np.ndarray,
        dtype: np.dtype = np.float32,
        is_mono: Union[bool, None] = None
    ) -> np.ndarray:
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
        ParameterValidator.validate_mandatory_numpy_array('audio', audio)
        ParameterValidator.validate_mandatory_numpy_dtype('dtype', dtype)
        ParameterValidator.validate_bool('is_mono', is_mono)

        return _to_dtype(
            audio,
            dtype,
            is_mono
        )

    @staticmethod
    def to_mono(
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Transform the provided 'audio' to a mono
        audio if needed.
        """
        return AudioNumpyHandler.to_dtype(audio, audio.dtype, True)
    
    @staticmethod
    def to_stereo(
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Transform the provided 'audio' to a 
        stereo audio if needed.
        """
        return AudioNumpyHandler.to_dtype(audio, audio.dtype, False)
    
    def remove_2nd_dimension(
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
        ParameterValidator.validate_mandatory_numpy_array('audio', audio)

        return _remove_2nd_dimension(audio)
    
    # TODO: Is this the same as we have in
    # the 'channels' module (?)
    def format_audio(
        audio: np.ndarray,
        mode: StereoAudioFormatMode = StereoAudioFormatMode.MIX_FIRST_LEFT
    ) -> np.ndarray:
        """
        Format the "audio" to the "mode" given
        or raise an Exception if not a valid
        "audio" provided.

        This method will return a numpy array
        of only one dimension, corresponding to
        the expected format.
        """
        ParameterValidator.validate_mandatory_numpy_array('audio', audio)
        mode = StereoAudioFormatMode.to_enum(mode)

        return mode.format_audio(audio)

    @staticmethod
    def generate_audio(
        # Frecuencia de muestreo en Hz
        sample_rate: int = 44_100,
        duration: float = 1.0,
        # Frecuencia del tono (Hz) - La4
        frequency: int = 440,
        dtype: np.dtype = np.float32,
        is_mono: bool = False
    ) -> np.ndarray:
        """
        Generate a random numpy audio array
        of the given 'dtype' and 2 dimensions
        with the shape (n_samples, n_channels).
        """
        ParameterValidator.validate_mandatory_positive_int('sample_rate', sample_rate, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_float('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('frequency', frequency, do_include_zero = False)
        ParameterValidator.validate_mandatory_numpy_dtype('dtype', dtype)
        #ParameterValidator.validate_mandatory_subclass_of('dtype', dtype, np.generic)
        ParameterValidator.validate_mandatory_bool('is_mono', is_mono)

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint = False)
        amplitude = 0.5
        audio = amplitude * np.sin(2 * np.pi * frequency * t)

        return AudioNumpyHandler.to_dtype(audio, dtype, is_mono)

    @staticmethod
    def is_valid(
        audio: np.ndarray
    ) -> bool:
        """
        Check if the 'audio' given is a 
        valid audio numpy array, which
        means that is a np.float32 array
        with the (n_samples, n_channels)
        shape and with values in the range
        [-1.0, 1.0].

        This is an audio that is processable
        by our libraries without any change.
        """
        return (
            PythonValidator.is_numpy_array(audio) and
            audio.ndim == 2 and
            audio.shape[1] in [1, 2] and
            audio.dtype == np.float32 and
            np.any(np.abs(audio) <= 1.0)
        )
    
    @staticmethod
    def can_be_valid(
        audio: np.ndarray
    ) -> bool:
        """
        Check if the provided 'audio' is
        an audio that is valid or can be
        transformed into a valid one by
        using the
        'to_valid_numpy_array_audio'
        method.
        """
        return (
            PythonValidator.is_numpy_array(audio) and
            (
                audio.ndim == 1 or
                (
                    audio.ndim == 2 and
                    audio.shape[1] in [1, 2]
                )
            ) and
            audio.dtype in [np.int16, np.float32]
        )
    
    @staticmethod
    def to_valid_numpy_array_audio(
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Transform, if needed, the 'audio'
        provided to a valid audio numpy
        array, which is a np.float32 array
        with the (n_samples, n_channels)
        shape and with values in the range
        [-1.0, 1.0].
        """
        ParameterValidator.validate_mandatory_numpy_array('audio', audio)
        if not AudioNumpyHandler.can_be_valid(audio):
            raise Exception('The "audio" provided cannot be converted to a valid numpy audio array.')

        return AudioNumpyHandler.to_dtype(audio, np.float32, None)

    @staticmethod
    def parse(
        audio: np.ndarray
    ) -> np.ndarray:
        """
        Parse the 'audio' numpy array 
        provided, check if is valid and
        transform it if needed to be able
        to use it in the libraries.
        """
        if not AudioNumpyHandler.can_be_valid:
            raise Exception('The "audio" parameter provided cannot be processed as a valid audio numpy array.')
        
        return AudioNumpyHandler.to_valid_numpy_array_audio(audio)