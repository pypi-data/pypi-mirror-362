from yta_numpy.video.moviepy.utils import _is_moviepy_normal_frame, _is_moviepy_mask_frame, _moviepy_normal_frame_has_all_colors, _moviepy_normal_frame_has_only_colors
from yta_validation.parameter import ParameterValidator
from yta_validation.number import NumberValidator
from yta_validation import PythonValidator

import numpy as np


MASK_FRAME_TOLERANCE  = 1e-6
# TODO: Move this to another file,
# it is not a utils
# TODO: Implement testing
class MoviepyVideoFrameHandler:
    """
    Class to wrap the functionality related
    to handle and manipulate numpy arrays
    that are moviepy normal or mask frame
    arrays.
    """

    @staticmethod
    def validate(
        frame: 'np.ndarray'
    ) -> None:
        """
        Check if the provided 'frame' is a
        numpy array valid as a moviepy mask
        or normal frame numpy array and
        raise an exception if not.
        """
        if not MoviepyVideoFrameHandler.is_normal_or_mask_frame(frame):
            raise Exception('The "frame" provided is not a valid moviepy normal or mask frame')
        
    @staticmethod
    def is_normal_or_mask_frame(
        frame: 'np.ndarray'
    ) -> bool:
        """
        Check if the provided 'frame' is a 
        valid moviepy normal or mask video
        frame.

        Normal:
        - `ndim == 3`
        - `shape[2] == 3`
        - `dtype == np.uint8`

        A valid frame would be like this:
        - `(720, 1080, 3)`

        Mask:
        - `ndim == 2`
        - `dtype in [np.float32, np.float64]`
        - each value is in `[-1.0, 1.0]` range

        A valid frame would be like this:
        - `(720, 1080)`
        """
        return (
            MoviepyVideoNormalFrameHandler.is_normal_frame(frame) or
            MoviepyVideoMaskFrameHandler.is_mask_frame(frame)
        )

    @staticmethod
    def is_normal_frame(
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
        return MoviepyVideoNormalFrameHandler.is_normal_frame(frame)
    
    def is_mask_frame(
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
        return MoviepyVideoMaskFrameHandler.is_mask_frame(frame)


class MoviepyVideoMaskFrameHandler:
    """
    Class to wrap the functionality related
    to handle and manipulate numpy arrays
    that are moviepy mask frame arrays.
    """

    @staticmethod
    def validate(
        frame: 'np.ndarray'
    ) -> None:
        """
        Check if the provided 'frame' is a
        numpy array valid as a moviepy mask
        frame numpy array and raise an
        exception if not.
        """
        if not MoviepyVideoMaskFrameHandler.is_mask_frame(frame):
            raise Exception('The "frame" provided is not a valid moviepy mask frame')
        
    @staticmethod
    def is_mask_frame(
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
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        return _is_moviepy_mask_frame(frame)

    @staticmethod
    def generate_random(
        width: int,
        height: int
    ) -> 'np.ndarray':
        """
        Generate a random numpy array that
        is valid as a moviepy video mask
        frame. The numpy array will have 
        the (width, height) shape, where
        each value is in the [0.0, 1.0]
        range.
        """
        ParameterValidator.validate_mandatory_positive_int('width', width, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('height', height, do_include_zero = False)

        return np.random.rand(height, width).astype(np.float32)
    
    @staticmethod
    def generate(
        width: int,
        height: int,
        opacity: float = 0.0
    ) -> 'np.ndarray':
        """
        Get a numpy array with the 'width'
        and 'height' provided that will
        have the also provided 'opacity'
        for each of the pixels. The
        'opacity' must be a value between
        0.0 (full transparent) and 1.0
        (full opaque).
        """
        ParameterValidator.validate_mandatory_positive_int('width', width, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('height', height, do_include_zero = False)
        ParameterValidator.validate_mandatory_number_between('opacity', opacity, 0.0, 1.0)

        return np.full((height, width), fill_value = opacity, dtype = np.float32)

    @staticmethod
    def is_full_opaque(
        frame: 'np.ndarray'
    ) -> bool:
        """
        Check if the provided 'frame' is a
        full opaque numpy array that works
        as a moviepy video mask frame.
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        MoviepyVideoMaskFrameHandler.validate(frame)

        return np.all(np.abs(frame - 1.0) < MASK_FRAME_TOLERANCE)

    @staticmethod
    def is_full_transparent(
        frame: 'np.ndarray'
    ) -> bool:
        """
        Check if the provided 'frame' is a
        full transparent numpy array that
        works as a moviepy video mask frame.
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        MoviepyVideoMaskFrameHandler.validate(frame)

        return np.all(frame < MASK_FRAME_TOLERANCE)
    
    @staticmethod
    def has_full_transparent_pixel(
        frame: 'np.ndarray'
    ) -> bool:
        """
        Check if the provided 'frame' is a
        numpy array that has, at least, one
        full transparent pixel and that 
        works as a moviepy video mask frame.
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        MoviepyVideoMaskFrameHandler.validate(frame)

        return np.any(frame < MASK_FRAME_TOLERANCE)
    
    @staticmethod
    def has_transparent_pixel(
        frame: 'np.ndarray'
    ) -> bool:
        """
        Check if the provided 'frame' is a
        numpy array that has, at least, one
        partially transparent pixel and that
        works as a moviepy video mask frame.
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        MoviepyVideoMaskFrameHandler.validate(frame)

        return np.any((frame > MASK_FRAME_TOLERANCE) & (frame < 1.0 - MASK_FRAME_TOLERANCE))

class MoviepyVideoNormalFrameHandler:
    """
    Class to wrap the functionality related
    to handle and manipulate numpy arrays
    that are moviepy rgb normal frame arrays.
    """

    @staticmethod
    def validate(
        frame: 'np.ndarray'
    ) -> None:
        """
        Check if the provided 'frame' is a
        numpy array valid as a moviepy RGB
        frame numpy array and raise an
        exception if not.
        """
        if not MoviepyVideoNormalFrameHandler.is_normal_frame(frame):
            raise Exception('The "frame" provided is not a valid moviepy normal RGB frame')
        
    @staticmethod
    def is_normal_frame(
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
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)

        return _is_moviepy_normal_frame(frame)
        
    @staticmethod
    def generate_random(
        width: int,
        height: int
    ) -> 'np.ndarray':
        """
        Generate a random numpy array that
        is valid as a moviepy video normal
        frame. The numpy array will have 
        the (width, height, 3) shape, where
        the 3 values will be a RGB array.
        """
        ParameterValidator.validate_mandatory_positive_int('width', width, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('height', height, do_include_zero = False)

        return np.random.randint(0, 256, size = (height, width, 3), dtype = np.uint8)
    
    @staticmethod
    def generate(
        width: int,
        height: int,
        color: list = [255, 255, 255]
    ) -> 'np.ndarray':
        """
        Generate a random numpy array that
        is valid as a moviepy video normal
        frame. The numpy array will have 
        the (width, height, 3) shape, where
        the 3 values will be a RGB array.
        """
        ParameterValidator.validate_mandatory_positive_int('width', width, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('height', height, do_include_zero = False)
        # TODO: Maybe use the 'yta_color' lib to
        # parse and validate
        if not (
            PythonValidator.is_instance(color, [list, np.ndarray]) and
            len(color) == 3 and
            all(
                NumberValidator.is_int(c) and
                0 <= c <= 255 for c in color
            )
        ):
            raise Exception('The "color" provided is not a valid color.')

        return np.full((height, width, 3), color, dtype = np.uint8)
    
    @staticmethod
    def has_all_colors(
        frame: 'np.ndarray',
        colors: list
    ) -> bool:
        """
        Check if the provided 'frame' has the
        also provided 'colors', that must be a
        list of RGB arrays. All the colors must
        be present in the frame.
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)
        # TODO: Validate 'colors' is a list but
        # I don't have the validation method
        
        return _moviepy_normal_frame_has_all_colors(frame, colors)
    
    @staticmethod
    def has_only_colors(
        frame: 'np.ndarray',
        colors: list
    ) -> bool:
        """
        Check if the provided 'frame' has only
        the also provided 'colors', that must
        be a list of RGB arrays. All the
        """
        ParameterValidator.validate_mandatory_numpy_array('frame', frame)
        # TODO: Validate 'colors' is a list but
        # I don't have the validation method

        return _moviepy_normal_frame_has_only_colors(frame, colors)


# TODO: This class below has been
# migrated as it was to refactor it
# here.
from yta_constants.video import MoviepyFrameMaskingMethod
#from yta_image.parser import ImageParser
from typing import Union

import numpy as np


class NumpyFrameHelper:
    """
    Class to encapsulate functionality related to numpy
    frames. Numpy frames are frames with width and height,
    and 1 or 3 values per pixel (per cell).
    """

    # TODO: Maybe use the ValueNormalizer (?)
    @staticmethod
    def normalize(
        frame: np.ndarray,
        do_check: bool = True
    ):
        """
        Normalize the frame if not normalized.
        """
        return (
            frame / 255.0
            if (
                do_check and
                NumpyFrameHelper.is_rgb_not_normalized(frame) or
                NumpyFrameHelper.is_alpha_not_normalized(frame) or
                NumpyFrameHelper.is_rgba_not_normalized(frame)
            ) else
            frame
        )

    @staticmethod
    def denormalize(
        frame: np.ndarray,
        do_check: bool = True
    ):
        """
        Denormalize the frame if normalized.
        """
        return (
            (frame * 255).astype(np.uint8)
            if (
                do_check and
                NumpyFrameHelper.is_rgb_normalized(frame) or
                NumpyFrameHelper.is_alpha_normalized(frame) or
                NumpyFrameHelper.is_rgba_normalized(frame)
            ) else
            frame
        )
    
    @staticmethod
    def is_normalized(
        frame: np.ndarray
    ):
        """
        Check if the provided frame is a a
        normalized one, which means that its
        type is .float64 or .float32 and that
        all values are between 0.0 and 1.0.
        """
        #frame = ImageParser.to_numpy(frame)

        return (
            frame.dtype in (np.float64, np.float32) and
            np.all((frame >= 0.0) & (frame <= 1.0))
        )

    @staticmethod
    def is_not_normalized(
        frame: np.ndarray
    ):
        """
        Check if the provided frame is not
        a normalized one, which means that
        its type is .uint8 and that all
        values are between 0 and 255.
        """
        #frame = ImageParser.to_numpy(frame)
        
        return (
            # TODO: Maybe the type is not that one (?)
            frame.dtype == np.uint8 and
            np.all((frame >= 0) & (frame <= 255))
        )

    @staticmethod
    def is_rgb(
        frame: np.ndarray,
        is_normalized: Union[None, bool] = None
    ):
        """
        Check if the provided 'frame' is an
        RGB frame, which means that its
        dimension is 3 and its shape is also
        3 per pixel.

        If 'is_normalized' is provided, it
        will check if the frame is normalized
        or not according to the boolean value
        passed as parameter.
        """
        # TODO: Validation, maybe (?)
        #frame = ImageParser.to_numpy(frame)

        is_rgb = (
            frame.ndim == 3 and
            frame.shape[2] == 3
        )

        return (
            is_rgb
            if is_normalized is None else
            (
                is_rgb and
                NumpyFrameHelper.is_normalized(frame)
            )
            if is_normalized else
            (
                is_rgb and
                NumpyFrameHelper.is_not_normalized(frame)
            )
        )

    @staticmethod
    def is_rgba(
        frame: np.ndarray,
        is_normalized: Union[None, bool] = None
    ):
        """
        Check if the provided 'frame' is an
        RGBA frame, which means that its
        dimension is 3 and its shape is 4 per
        pixel.

        If 'is_normalized' is provided, it
        will check if the frame is normalized
        or not according to the boolean value
        passed as parameter.

        TODO: This is not actually a frame we
        can use in moviepy videos, but it
        could be a frame we build to later
        decompose in clip and mask clip, so I
        keep the code. Maybe it is useless in
        the future and thats why this is a
        TODO.
        """
        # TODO: Validation, maybe (?)
        #frame = ImageParser.to_numpy(frame)

        is_rgba = (
            frame.ndim == 3 and
            frame.shape[2] == 4
        )

        return (
            is_rgba
            if is_normalized is None else
            (
                is_rgba and
                NumpyFrameHelper.is_normalized(frame)
            )
            if is_normalized else
            (
                is_rgba and
                NumpyFrameHelper.is_not_normalized(frame)
            )
        )
    
    @staticmethod
    def is_alpha(
        frame: np.ndarray,
        is_normalized: Union[None, bool] = None
    ):
        """
        Check if the provided 'frame' is an
        alpha frame, which means that its
        dimension is 2 because there is only
        one single value per pixel.

        
        If 'is_normalized' is provided, it
        will check if the frame is normalized
        or not according to the boolean value
        passed as parameter.
        """
        # TODO: Validation, maybe (?)
        #frame = ImageParser.to_numpy(frame)

        is_alpha = frame.ndim == 2

        return (
            is_alpha
            if is_normalized is None else
            (
                is_alpha and
                NumpyFrameHelper.is_normalized(frame)
            )
            if is_normalized else
            (
                is_alpha and
                NumpyFrameHelper.is_not_normalized(frame)
            )
        )

    @staticmethod
    def is_rgb_not_normalized(
        frame: np.ndarray
    ):
        """
        Check if the provided 'frame' is a
        numpy array of ndim = 3, dtype =
        np.uint8 and all the values (3) are
        between 0 and 255.
        """
        return NumpyFrameHelper.is_rgb(frame, is_normalized = False)
    
    @staticmethod
    def is_rgb_normalized(
        frame: np.ndarray
    ):
        """
        Check if the provided 'frame' is a
        numpy array of ndim = 3, dtype =
        np.float64|np.float32 and all the
        values (3) are between 0.0 and 1.0.
        """
        return NumpyFrameHelper.is_rgb(frame, is_normalized = True)

    @staticmethod
    def is_rgba_normalized(
        frame: np.ndarray
    ):
        """
        TODO: Explain
        """
        return NumpyFrameHelper.is_rgba(frame, is_normalized = True)
    
    @staticmethod
    def is_rgba_not_normalized(
        frame: np.ndarray
    ):
        """
        TODO: Explain
        """
        return NumpyFrameHelper.is_rgba(frame, is_normalized = False)

    @staticmethod
    def is_alpha_normalized(
        frame: np.ndarray
    ):
        """
        TODO: Explain
        """
        return NumpyFrameHelper.is_alpha(frame, is_normalized = True)

    @staticmethod
    def is_alpha_not_normalized(
        frame: np.ndarray
    ):
        """
        TODO: Explain
        """
        return NumpyFrameHelper.is_alpha(frame, is_normalized = False)

    @staticmethod
    def as_rgb(
        frame: np.ndarray,
        do_normalize: bool = False
    ):
        """
        Turn the provided 'frame' to a
        normal (rgb) frame, normalized or
        not according to the provided as
        'do_normalize' parameter.

        This method will return a numpy
        array containing 3 values for each
        pixel, and each one for them will
        be from 0.0 to 1.0 if normalized,
        or from 0 to 255 if not normalized.

        A default moviepy frame is a numpy
        array of 3 values per pixel from 0
        to 255.
        """
        if NumpyFrameHelper.is_alpha_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        # TODO: Why not 'elif' (?)
        if NumpyFrameHelper.is_alpha_not_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgb_normalized(frame):
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgb_not_normalized(frame):
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgba_normalized(frame):
            frame = frame[:, :, :3]
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgba_not_normalized(frame):
            frame = frame[:, :, :3]
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        else:
            raise Exception('The provided "frame" is not recognized as a valid frame (RGB, RGBA or alpha).')

        return frame
    
    @staticmethod
    def as_alpha(
        frame: np.ndarray,
        do_normalize: bool = True,
        masking_method: MoviepyFrameMaskingMethod = MoviepyFrameMaskingMethod.MEAN
    ):
        """
        Turn the provided 'frame' to an
        alpha frame, normalized or not
        according to the 'do_normalize'
        parameter provided.

        This method will return a numpy
        array containing one single
        value for each pixel, that will
        be from 0.0 to 1.0 if normalized,
        or from 0 to 255 if not
        normalized.

        A default moviepy mask frame is
        a numpy array of one single value
        per pixel from 0.0 to 1.0.

        The 'masking_method' will
        determine the method that is
        needed to be used to turn the
        normal frame into a mask frame.
        """
        masking_method = MoviepyFrameMaskingMethod.to_enum(masking_method)

        if NumpyFrameHelper.is_alpha_normalized(frame):
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        # TODO: Why not 'elif' (?)
        if NumpyFrameHelper.is_alpha_not_normalized(frame):
            frame = np.stack((frame, frame, frame), axis = -1)
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgb_normalized(frame):
            frame = _moviepy_normal_frame_to_mask_frame(frame, masking_method)
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgb_not_normalized(frame):
            frame = _moviepy_normal_frame_to_mask_frame(frame, masking_method)
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgba_normalized(frame):
            frame = frame[:, :, :3]
            frame = _moviepy_normal_frame_to_mask_frame(frame, masking_method)
            frame = (
                NumpyFrameHelper.denormalize(frame, do_check = False)
                if not do_normalize else
                frame
            )
        elif NumpyFrameHelper.is_rgba_not_normalized(frame):
            frame = frame[:, :, :3]
            frame = _moviepy_normal_frame_to_mask_frame(frame, masking_method)
            frame = (
                NumpyFrameHelper.normalize(frame, do_check = False)
                if do_normalize else
                frame
            )
        else:
            raise Exception('The provided "frame" is not recognized as a valid frame (RGB, RGBA or alpha).')

        return frame

    def invert(
        frame: np.ndarray
    ):
        """
        Invert the provided array
        according to if it is a
        normalized or a not normalized
        one.
        """
        if NumpyFrameHelper.is_normalized():
            frame = 1.0 - frame
        elif NumpyFrameHelper.is_not_normalized():
            frame = 255 - frame
        else:
            raise Exception('The provided "frame" is not a normalized array nor a not normalized one.')
        
        return frame
    
# TODO: I moved this NumpyFrameHelper
# class to here to remove from the
# 'yta_video_base' library but maybe
# has too many methods
def _moviepy_normal_frame_to_mask_frame(
    frame: 'np.ndarray',
    method: MoviepyFrameMaskingMethod
) -> 'np.ndarray':
    """
    Process the given 'frame', that has to
    be a moviepy normal video frame, and
    transform it into a moviepy mask video
    frame by using the method.
    """
    # TODO: The 'frame' has to be valid
    if not MoviepyVideoFrameHandler.is_normal_frame(frame):
        raise Exception('The provided "frame" is not actually a moviepy normal video frame.')

    return {
        MoviepyFrameMaskingMethod.MEAN: np.mean(frame, axis = -1) / 255.0,
        MoviepyFrameMaskingMethod.PURE_BLACK_AND_WHITE: _pure_black_and_white_image_to_moviepy_mask_numpy_array(_frame_to_pure_black_and_white_image(frame))
    }[method]

# Other utils
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

# TODO: Should I combine these 2 methods below in only 1 (?)
def _pure_black_and_white_image_to_moviepy_mask_numpy_array(
    image: 'np.ndarray'
):
    """
    Turn the received 'image' (that must
    be a pure black and white image) to a
    numpy array that can be used as a
    moviepy mask (by using ImageClip).

    This is useful for static processed
    images that we want to use as masks,
    such as frames to decorate our videos.
    """
    # TODO: Image must be a numpy
    #image = ImageParser.to_numpy(image)

    if not MoviepyVideoNormalFrameHandler.has_only_colors(image, [BLACK, WHITE]):
        raise Exception(f'The provided "image" parameter "{str(image)}" is not a black and white image.')

    # Image to a numpy parseable as moviepy mask
    mask = np.zeros(image.shape[:2], dtype = int)   # 3col to 1col
    mask[np.all(image == WHITE, axis = -1)] = 1     # white to 1 value

    return mask

def _frame_to_pure_black_and_white_image(
    frame: 'np.ndarray'
):
    """
    Process the provided moviepy clip mask
    frame (that must have values between
    0.0 and 1.0) or normal clip frame (that 
    have values between 0 and 255) and
    convert it into a pure black and white
    image (an image that contains those 2
    colors only).

    This method returns a not normalized
    numpy array of only 2 colors (pure white
    [255, 255, 255] and pure black [0, 0,
    0]), perfect to turn into a mask for
    moviepy clips.

    This is useful when handling an alpha
    transition video that can include (or
    not) an alpha layer but it is also
    clearly black and white so you
    transform it into a mask to be applied
    on a video clip.
    """
    # TODO: Frame must be a numpy
    #frame = ImageParser.to_numpy(frame)

    if not MoviepyVideoFrameHandler.is_normal_frame(frame):
        raise Exception('The provided "frame" parameter is not a moviepy mask clip frame nor a normal clip frame.')
    
    if MoviepyVideoFrameHandler.is_normal_frame(frame):
        # TODO: Process it with some threshold to turn it
        # into pure black and white image (only those 2
        # colors) to be able to transform them into a mask.
        threshold = 220
        white_pixels = np.all(frame >= threshold, axis = -1)

        # Image to completely and pure black
        new_frame = np.array(frame)
        
        # White pixels to pure white
        new_frame[white_pixels] = WHITE
        new_frame[~white_pixels] = BLACK
    elif MoviepyVideoFrameHandler.is_mask_frame(frame):
        transparent_pixels = frame == 1

        new_frame = np.array(frame)
        
        # Transparent pixels to pure white
        new_frame[transparent_pixels] = WHITE
        new_frame[~transparent_pixels] = BLACK

    return new_frame