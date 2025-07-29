"""
Module to manage and handle moviepy
video frames.

Each moviepy video is a sequence of
frames. Each frame can be normal or
can have a second related frame that
is a mask frame.

The normal frame is a 'np.uint8' and
has a (height, width, 3) shape. The
range of values is [0, 255] for each
color channel (R, G, B), where 0 
means no color and 255 full color.
For example, a frame of a 720p video
would have a (720, 1280, 3) shape.

The mask frame is a 'np.float32' or
'np.float64' and has a (height,
width) shape. The range of values is
[0.0, 1.0] for each value, where 0.0
means completely transparent and 1.0
means completely opaque. For example,
a frame of a 720p video would have 
(720, 1280) shape.

A mask frame can be attached to a 
normal frame but not viceversa. So,
a normal frame can (or cannot) have
a mask frame attached.
"""
from yta_numpy.video.moviepy.frame_handler import NumpyFrameHelper
from yta_constants.video import MoviepyFrameMaskingMethod
from dataclasses import dataclass

import numpy as np


@dataclass
class VideoFrame:
    """
    Class to represent a video frame, to simplify the way
    we turn it into a mask and work with it. A mask frame
    is a numpy array with single values per pixel and 
    values between 0.0 and 1.0 (where 0.0 is full 
    full transparent and 1.0 is full opaque). A normal
    frame is a numpy array with 3 values per pixel
    (representing R, G, B) between 0 and 255 (where 0 is
    the absence of color and 255 the full presence of that
    color).

    This class has been created to work easily with frames
    and to verify them when creating a new instance.
    """
    
    @property
    def is_mask(
        self
    ):
        """
        Indicate if the 'frame' stored is a mask,
        which means that is a numpy array of single
        values between 0.0 and 1.0 (representing 
        the opacity: 0.0 is full transparent, 1.0 
        is full opaque).
        """
        return self._is_mask == True
    
    @property
    def is_normal(
        self
    ):
        """
        Indicate if the 'frame' stored is normal,
        which means that is a numpy array of 3 
        values (R, G, B) between 0 and 255 
        (representing the color presence: 0 is no
        color, 255 is full color).
        """
        return self._is_mask == False
    
    @property
    def inverted(
        self
    ):
        """
        Get the frame but inverted (each pixel
        will be transformed by substracting its
        value from the maximum value). This
        property does not modify the object
        itself.
        """
        return NumpyFrameHelper.invert(self.frame)
    
    @property
    def normalized(
        self
    ):
        """
        Get the frame but normalized (with values
        between 0.0 and 1.0). This property does
        not modify the object itself.
        """
        return NumpyFrameHelper.normalize(self.frame)
    
    @property
    def denormalized(
        self
    ):
        """
        Get the frame denormalized (with values
        between 0 and 255). This property does not
        modify the object itself.
        """
        return NumpyFrameHelper.denormalize(self.frame)

    def __init__(
        self,
        frame: np.ndarray
    ):
        if (
            not NumpyFrameHelper.is_rgb_not_normalized(frame) and
            not NumpyFrameHelper.is_rgb_normalized(frame) and
            not NumpyFrameHelper.is_alpha_normalized(frame) and
            not NumpyFrameHelper.is_alpha_not_normalized(frame)
        ):
            # TODO: Print properties to know why it is not valid
            raise Exception('The provided "frame" is not a valid frame.')

        is_mask = False
        if NumpyFrameHelper.is_alpha(frame):
            is_mask = True
            # We ensure it is a normalized alpha frame to store it
            frame = NumpyFrameHelper.as_alpha(frame)
        elif NumpyFrameHelper.is_rgb(frame):
            # We ensure it is a not normalized normal frame to store it
            frame = NumpyFrameHelper.as_rgb(frame)
        else:
            raise Exception('The provided "frame" is not an alpha nor a rgb frame.')

        self.frame: np.ndarray = frame
        """
        The frame information as a numpy array.
        This array can only contain frames in
        the format of not normalized RGB (array
        of 3 values from 0 to 255 per pixel) or
        normalized alpha (1 single value per
        pixel from 0.0 to 1.0).
        """
        self._is_mask = is_mask
        """
        Boolean value, autodetected internally,
        to indicate if the frame is a mask
        frame or is not.
        """

    def as_mask(
        self,
        masking_method: MoviepyFrameMaskingMethod = MoviepyFrameMaskingMethod.MEAN
    ):
        """
        Return the frame as a mask by applying
        the 'masking_method' if necessary.
        """
        return (
            self.frame
            if self.is_mask else
            NumpyFrameHelper.as_alpha(self.frame, do_normalize = True, masking_method = masking_method)
        )

