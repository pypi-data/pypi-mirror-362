from yta_numpy.video.moviepy.frame_handler import MoviepyVideoFrameHandler, MoviepyVideoNormalFrameHandler
from yta_constants.video import MoviepyFrameMaskingMethod

import numpy as np


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