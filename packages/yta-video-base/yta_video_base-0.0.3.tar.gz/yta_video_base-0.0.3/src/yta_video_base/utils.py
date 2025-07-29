from yta_video_base.frame.utils import SMALL_AMOUNT_TO_FIX, get_frame_time_moments, frame_time_to_frame_index
from yta_constants.multimedia import DEFAULT_SCENE_SIZE, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT
from copy import copy


# This is to fix a problem with 
# the video duration extracted
# from the MPVideo class
# TODO: I don't know where to 
# place this
def calculate_real_video_duration(
    video: 'Clip'
):
    """
    Process the provided 'video' and obtain the real
    duration by trying to access to the last frames
    according to its duration attribute.

    This method will return the real duration, which
    is determined by the last accessible frame plus
    the frame duration and a small amount to avoid
    decimal issues.
    """
    import warnings
    
    #video = VideoParser.to_moviepy(video)

    # Moviepy library is throwing a warning when a 
    # frame is not accessible through its 
    # ffmpeg_reader, but will return the previous
    # valid frame and throw no Exceptions. As we
    # are trying to determine its real duration,
    # that warning is saying that the frame is not
    # valid, so it is not part of its real duration
    # so we must avoid it and continue with the
    # previous one until we find the first (last)
    # valid frame.
    warnings.filterwarnings('error')
    
    for t in get_frame_time_moments(video.duration, video.fps)[::-1]:
        try:
            # How to catch warnings: https://stackoverflow.com/a/30368735
            video.get_frame(t = t)
            last_frame = t
            break
        except:
            pass

    warnings.resetwarnings()

    frame_duration = 1 / video.fps
    # I sum a small amount to ensure it is over the
    # duration that guarantees the expected amount
    # of frames when calculating
    # Use this below to fix the video duration:
    # video = video.with_subclip(0, calculate_real_video_duration(video))#.with_fps(60)
    return ((last_frame + frame_duration + SMALL_AMOUNT_TO_FIX) // frame_duration) * frame_duration + SMALL_AMOUNT_TO_FIX


def wrap_video_with_transparent_background(
    video: 'Clip'
):
    """
    Put a full transparent background behind the video
    if its size is not our default scene (1920x1080) and
    places the video on the center of this background.

    This method works with a copy of the original video so
    only the returned one is changed.
    """
    #video = VideoParser.to_moviepy(video)

    video = copy(video)
    # TODO: Is this changing the variable value or do I
    # need to do by position (?)
    if video.size != DEFAULT_SCENE_SIZE:
        # I place the video at the center of the new background but
        # I reposition it to place with its center in the same place
        # as the original one
        original_center_positions = []
        # TODO: Careful with this t
        for t in get_frame_time_moments(video.duration, video.fps):
            pos = video.pos(t)
            original_center_positions.append((pos[0], pos[1]))

        video = CompositeVideoClip([
            ClipGenerator.get_default_background_video(duration = video.duration, fps = video.fps),
            video.with_position(('center', 'center'))
        ]).with_position(lambda t: (
            original_center_positions[frame_time_to_frame_index(t, 1 / video.fps)][0] - DEFAULT_SCENE_WIDTH / 2,
            original_center_positions[frame_time_to_frame_index(t, 1 / video.fps)][1] - DEFAULT_SCENE_HEIGHT / 2
        ))

    return video


# Other utils, from 'ya_multimedia.utils.py'
from yta_multimedia.video.parser import VideoParser
from yta_image.parser import ImageParser
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_programming.output import Output
from yta_constants.file import FileType
# TODO: We need to avoid the use of FileReturn
# because it uses a lot of dependencies to parse
# the file content dynamically and that is not a
# good thing...
from yta_general_utils.dataclasses import FileReturn
from moviepy import ImageClip
from moviepy.Clip import Clip
from typing import Union, Any
import numpy as np


def generate_video_from_image(
    image: Union[str, Any, ImageClip],
    duration: float = 1,
    fps: float = 60,
    output_filename: Union[str, None] = None
) -> Union[FileReturn, Clip]:
    """
    Create an ImageClip of 'duration' seconds with the
    given 'image' and store it locally if 'output_filename'
    is provided.

    This method return a Clip instance if the file is not
    written, and a FileReturn instance if yes.
    """
    ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)

    if not PythonValidator.is_instance(image, ImageClip):
        video = ImageClip(ImageParser.to_numpy(image), duration = duration).with_fps(fps)

    if output_filename:
        video.write_videofile(Output.get_filename(output_filename, FileType.VIDEO))

    return (
        video
        if output_filename is None else
        FileReturn(
            video,
            FileType.VIDEO,
            output_filename
        )
    )

def is_video_transparent(
    video: Clip
):
    """
    Checks if the first frame of the mask of the
    given 'video' has, at least, one transparent
    pixel.
    """
    # We need to detect the transparency from the mask
    video = VideoParser.to_moviepy(video, do_include_mask = True)

    # We need to find, by now, at least one transparent pixel
    # TODO: I would need to check all frames to be sure of this above
    # TODO: The mask can have partial transparency, which 
    # is a value greater than 0, so what do we consider
    # 'transparent' here (?)
    return np.any(video.mask.get_frame(t = 0) == 1)