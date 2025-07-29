"""
TODO: Deprecated in favor of VVideo.
Please, remove it when possible.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame import VideoFrame
from yta_multimedia.video.edition.duration import set_video_duration
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_video_base.frame.utils import SMALL_AMOUNT_TO_FIX
from yta_constants.multimedia import DEFAULT_SCENE_SIZE
from yta_validation import PythonValidator
from yta_validation.number import NumberValidator
from typing import Union
from moviepy import VideoClip, CompositeVideoClip, concatenate_videoclips
from moviepy.Clip import Clip
from copy import copy

import warnings
import random


class MPVideo:
    """
    Custom class to solve some bugs or issues with
    moviepy videos duration and frames number and
    malfunctioning related to floating points, and
    to also include some recurrent functionality.
    """

    _video: Clip = None
    """
    The original moviepy video clip.
    """
    _frames_indexes: list[int] = None
    _even_frames_indexes: list[int] = None
    _odd_frames_indexes: list[int] = None

    def __init__(
        self,
        video: Clip
    ):
        self._video = video
        self.update_video_info()

    def update_video_info(
        self
    ):
        """
        Process its own video to update the information
        if changed.
        """
        self._video = MPVideo.process_video(self._video)

    def __str__(
        self
    ):
        return f'duration: {self.duration}\nfps: {self.fps}\nnumber_of_frames: {self.number_of_frames}\nframes_time_moments: {self.frames_time_moments}\nframes_indexes: {self.frames_indexes}\nframe_duration: {self.frame_duration}'

    @staticmethod
    def process_video(
        video: Clip
    ):
        """
        Process the provided 'video' and makes it fit
        perfectly its real duration and forced to be
        60 fps.

        This method will try to do .get_frame() for 
        the last frames to obtain the real duration
        and adjust it consequently. It could make the
        execution slower, but we avoid issues with
        wrong durations.
        """
        video = VideoParser.to_moviepy(video)

        # 1. Ensure real duration and force to 60fps
        video = video.with_subclip(0, calculate_real_video_duration(video))#.with_fps(60)

        return video

    @property
    def video(
        self
    ):
        """
        Original moviepy video clip.
        """
        return self._video

    @property
    def duration(
        self
    ):
        """
        Real duration of the video, that has been
        checked according to the available frames.
        """
        return self.video.duration
    
    @property
    def fps(
        self
    ):
        """
        Frames per second of the original video.
        """
        return self.video.fps
    
    @property
    def number_of_frames(
        self
    ):
        """
        Number of frames of the moviepy video, using
        the previously checked duration.
        """
        return int(self.duration * self.fps)

    @property
    def frames_time_moments(
        self
    ):
        """
        Array containing all the time moments of video
        frames, that can be used to obtain each frame
        individually with the 'video.get_frame(t = t)'
        method.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        return get_frame_time_moments(self.duration, self.fps)
    
    @property
    def frames_indexes(
        self
    ):
        """
        Array containing all the indexes of video frames,
        that can be used to obtain its corresponding
        frame time moment, or to make things simpler.
        """
        if self._frames_indexes is None:
            self._frames_indexes = get_frame_indexes(self.duration, self.fps)
        
        return self._frames_indexes
    
    @property
    def frame_duration(
        self
    ):
        """
        Frame duration, based on video frames per second.
        """
        return 1 / self.fps
    
    # TODO: Maybe move this method to a VideoMaskInverter
    # class...
    def invert(
        self
    ):
        """
        Invert the received 'video' (that must be a moviepy 
        mask or normal clip) and return it inverted as a
        VideoClip. If the provided 'video' is a mask, this 
        will be also a mask.

        If the 'clip' provided is a mask clip, remember to
        set it as the new mask of your main clip.

        This inversion is a process in which the numpy array
        values of each frame are inverted by substracting the
        highest value. If the frame is an RGB frame with 
        values between 0 and 255, it will be inverted by 
        doing 255 - X on each frame pixel value. If it is
        normalized and values are between 0 and 1 (it is a 
        mask clip frame), by doing 1 - X on each mask frame
        pixel value.
        """
        mask_frames = [
            VideoFrame(frame).inverted
            for frame in self.video.iter_frames()
        ]

        # TODO: Which calculation is better, t * fps or t // frame_duration (?)
        # TODO: What if we have fps like 29,97 (?) I proposed forcing
        # the videos to be 60fps always so we avoid this problem
        return VideoClip(lambda t: mask_frames[int(t * self.video.fps)], is_mask = self.video.is_mask).with_fps(self.video.fps)

    def prepare_background_clip(
        self,
        background_video: Union[str, Clip]
    ):
        """
        Prepares the provided 'background_video' by modifying its duration to
        be the same as the provided 'video'. By default, the strategy is 
        looping the 'background_video' if the 'video' duration is longer, or
        cropping it if it is shorter. This method returns the background_clip
        modified according to the provided 'video'.

        This method will raise an Exception if the provided 'video' or the provided
        'background_video' are not valid videos.

        TODO: Add a parameter to be able to customize the extend or enshort
        background strategy.
        """
        background_video = VideoParser.to_moviepy(background_video)

        background_video = set_video_duration(background_video, self.video.duration)

        return background_video

    def wrap_with_transparent_background(
        self
    ):
        return MPVideo.wrap_video_with_transparent_background(self.video)


    # TODO: I think static methods below must be
    # in another file because this class was born
    # to be used as instances
    @staticmethod
    def wrap_video_with_transparent_background(
        video: Clip
    ):
        """
        Put a full transparent background behind the video
        if its size is not our default scene (1920x1080) and
        places the video on the center of this background.

        This method works with a copy of the original video so
        only the returned one is changed.
        """
        video = VideoParser.to_moviepy(video)

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
                original_center_positions[MPVideo.frame_time_to_frame_index(t, 1 / video.fps)][0] - MOVIEPY_SCENE_DEFAULT_SIZE[0] / 2,
                original_center_positions[MPVideo.frame_time_to_frame_index(t, 1 / video.fps)][1] - MOVIEPY_SCENE_DEFAULT_SIZE[1] / 2
            ))

        return video

    @staticmethod
    def concatenate_videos(
        videos: list[Clip]
    ):
        """
        Concatenate the provided 'videos' but fixing the
        videos dimensions. It will wrap any video that
        doesn't fit the 1920x1080 scene size with a full
        transparent background to fit those dimensions.
        """
        if not PythonValidator.is_list(videos):
            videos = [videos]

        videos = [
            MPVideo.wrap_with_transparent_background(video) 
            for video in [
                VideoParser.to_moviepy(video)
                for video in videos
            ]
        ]
        
        return concatenate_videoclips(videos)



def get_frame_time_moments(
    duration,
    fps
):
    """
    Get the time moment of each video frame according
    to the provided video 'duration' and 'fps'. This
    will always include the second 0 and the 
    inmediately before the duration.

    If a video lasts 1 second and has fps = 5, this
    method will return: 0, 0.2, 0.4, 0.6, 0.8

    This method can return non-exact decimal values 
    so we recommend you to add a small amount to
    ensure it is above the expected base frame time.
    """
    return [
        (1 / fps * i) + SMALL_AMOUNT_TO_FIX
        for i in range(int(duration * fps + SMALL_AMOUNT_TO_FIX) + 1)
    ][:-1]

def calculate_real_video_duration(
    video: Clip
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
    video = VideoParser.to_moviepy(video)

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
    return ((last_frame + frame_duration + SMALL_AMOUNT_TO_FIX) // frame_duration) * frame_duration + SMALL_AMOUNT_TO_FIX
