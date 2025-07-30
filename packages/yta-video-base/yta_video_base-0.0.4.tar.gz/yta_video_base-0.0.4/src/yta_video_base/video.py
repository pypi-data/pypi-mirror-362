from yta_video_base.utils import calculate_real_video_duration, wrap_video_with_transparent_background
from yta_video_base.frame.utils import get_number_of_frames, get_frame_duration, get_frame_indexes, get_video_frames_indexes_from_duration_and_fps, get_video_frames_ts_from_duration_and_fps
from yta_video_base.parser import VideoParser
from yta_video_base.frame.extractor import VideoFrameExtractor
from yta_video_base.frame import VideoFrame
from yta_validation.parameter import ParameterValidator
from moviepy.Clip import Clip
from moviepy import VideoClip
from typing import Union

import numpy as np


class VideoWrapped:
    """
    Class to wrap a moviepy video, simplify
    the way we work with them and also fix
    some issues with bugs.
    """

    video: 'Clip'
    """
    The original moviepy video clip.
    """

    @property
    def duration(
        self
    ) -> float:
        """
        Real duration of the video, that has been
        checked according to the available frames.
        """
        return self.video.duration
    
    @property
    def fps(
        self
    ) -> float:
        """
        Frames per second of the original video.
        """
        return self.video.fps
    
    @property
    def audio_fps(
        self
    ) -> Union[float, None]:
        """
        Frames per second of the audio clip attached
        to this video clip, that can be None if no
        audio attached.
        """
        return (
            None
            if not self.has_audio else
            self.audio.fps
        )

    @property
    def original_size(
        self
    ):
        """
        The size of the original video clip.
        """
        return self.video.size

    @property
    def original_width(
        self
    ):
        """
        The width of the original video clip.
        """
        return self.original_size[0]
    
    @property
    def original_height(
        self
    ):
        """
        The height of the original video clip.
        """
        return self.original_size[1]
    
    @property
    def number_of_frames(
        self
    ) -> int:
        """
        Number of frames of the moviepy
        video.
        """
        return get_number_of_frames(self.duration, self.fps)
    
    @property
    def frame_duration(
        self
    ) -> float:
        """
        Frame duration, based on the video
        frames per second (fps).
        """
        return get_frame_duration(self.fps)

    @property
    def audio_frame_duration(
        self
    ) -> Union[float, None]:
        """
        Frame duration of the audio clip attached
        to this video clip, if attached, or None
        if not.
        """
        return (
            None
            if not self.has_audio else
            1 / self.audio_fps
        )
    
    @property
    def audio(
        self
    ) -> Union['AudioClip', None]:
        """
        Get the audio of the video, if an AudioClip is
        attached, or None if not.
        """
        return self.video.audio
    
    @property
    def has_audio(
        self
    ) -> bool:
        """
        Indicate if the video has an audio clip attached
        or not.
        """
        return self.audio is not None
    
    @property
    def without_audio(
        self
    ) -> 'Clip':
        """
        Get the video clip but without any audio clip 
        attached to it.
        
        This method doesn't affect to the original
        video, it is just a copy.
        """
        return self.video.without_audio()

    # TODO: Should I keep this here? I think this is
    # an additional functionality that is not about
    # wrapping the class but adding functionality, and
    # that must be done in another library related
    # to video editing
    # @property
    # def with_audio(
    #     self
    # ) -> 'Clip':
    #     """
    #     Get the video clip with an audio clip attached
    #     to it. If there is not an audio clip attached,
    #     a new silent audio clip will be created and
    #     attached to it.

    #     This method doesn't affect to the original
    #     video, it is just a copy.
    #     """
    #     # TODO: Create a silent audio clip with the
    #     # same duration and return a copy with it
    #     # attached to
    #     return self.video.copy()

    @property
    def mask(
        self
    ) -> Union['Clip', None]:
        """
        Get the mask video clip attached to this video,
        if existing, or None if not.
        """
        return self.video.mask
    
    @property
    def is_mask(
        self
    ) -> bool:
        """
        Indicate if the video is set as a mask video. A
        video that is a mask cannot has another video
        attached as a mask.
        """
        return self.video.is_mask

    @property
    def has_mask(
        self
    ) -> bool:
        """
        Indicate if the video has another video attached
        as a mask.
        """
        return self.mask is not None
    
    @property
    def has_transparent_mask(
        self
    ) -> bool:
        """
        Check if the first frame of the mask of this
        video has, at least, one transparent pixel,
        which means that the mask is actually a
        transparent mask.
        """
        # TODO: I would like to check all the frames not
        # only the first one, but that takes time...
        # TODO: While 1 means that the mask is fully
        # transparent, it could have partial transparency
        # which is a value greater than 0.0, and we are
        # not considering that here...
        return (
            self.has_mask and
            #np.any(self.mask.get_frame(t = 0) == 1) # Full transparent pixel only
            np.any(self.mask.get_frame(t = 0) > 0) # Partial transparent pixel
        )

    @property
    def frames(
        self
    ):
        """
        All the frames of this video clip.
        """
        # TODO: Maybe map in an internal variable (?)
        return VideoFrameExtractor.get_all_frames(self.video)

    @property
    def audio_frames(
        self
    ) -> Union[list[any], None]:
        """
        All the frames of the audio clip that is
        attached to this video, if attached, or None
        if not.
        """
        # TODO: Maybe map in an internal variable (?)
        return (
            None
            if not self.has_audio else
            VideoFrameExtractor.get_all_frames(self.audio)
        )

    @property
    def number_of_frames(
        self
    ) -> int:
        """
        Get the number of video frames that exist in
        the video, using the duration of this instance
        that can be the one checked if it was requested
        in the '__init__' method.
        """
        return get_number_of_frames(self.duration, self.fps)
    
    @property
    def number_of_audio_frames(
        self
    ) -> Union[int, None]:
        """
        Get the number of audio frames that exist in
        the audio clip that is attached to the video,
        if attached, or None if not audio.
        """
        return (
            None
            if not self.has_audio else
            get_number_of_frames(self.duration, self.audio_fps)
        )
    
    @property
    def frame_indexes(
        self
        # TODO: Please, type
    ) -> list[int]:
        """
        Array containing all the indexes of video frames,
        that can be used to obtain its corresponding
        frame time moment, or to make things simpler.
        """
        self._frames_indexes = (
            get_frame_indexes(self.duration, self.fps)
            if not hasattr(self, '_frames_indexes') else
            self._frames_indexes
        )
        
        return self._frames_indexes
        # TODO: Maybe map in an internal variable (?)
        return get_video_frames_indexes_from_duration_and_fps(self.duration, self.fps)
    
    @property
    def audio_frame_indexes(
        self
        # TODO: Please, type
    ) -> Union[list[int], None]:
        """
        The indexes of all the audio frames if there is
        an audio clip attached to this video clip, or 
        None if not.
        """
        return (
            None
            if not self.has_audio else
            get_video_frames_indexes_from_duration_and_fps(self.duration, self.audio_fps)
        )
    
    @property
    def frame_time_moments(
        self
    ) -> list[float]:
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
        # self._frames_time_moments = (
        #     get_frame_time_moments(self.duration, self.fps)
        #     if not hasattr(self, '_frames_time_moments') else
        #     self._frames_time_moments
        # )

        # return self._frames_time_moments
        # TODO: Maybe map in an internal variable (?)
        return get_video_frames_ts_from_duration_and_fps(self.duration, self.fps)
    
    @property
    def audio_frame_time_moments(
        self
    ) -> Union[list[float], None]:
        """
        All the frame time moments of the audio clip
        that is attached to this video clip, if
        attached, or None if not.
        """
        return (
            None
            if not self.has_audio else
            get_video_frames_ts_from_duration_and_fps(self.duration, self.audio_fps)
        )
    
    @property
    def inverted(
        self
    ):
        """
        The video but inverted, a process in which the numpy
        array values of each frame are inverted by
        substracting the highest value. If the frame is an
        RGB frame with values between 0 and 255, it will be
        inverted by doing 255 - X on each frame pixel value.
        If it is normalized and values are between 0 and 1
        (it is a mask clip frame), by doing 1 - X on each
        mask frame pixel value.
        """
        mask_frames = [
            VideoFrame(frame).inverted
            for frame in self.video.iter_frames()
        ]

        # TODO: Which calculation is better, t * fps or t // frame_duration (?)
        # TODO: What if we have fps like 29,97 (?) I proposed forcing
        # the videos to be 60fps always so we avoid this problem
        return VideoClip(
            make_frame = lambda t: mask_frames[int(t * self.video.fps)],
            is_mask = self.is_mask
        ).with_fps(self.fps)

    @property
    def wrapped_with_transparent_video(
        self
    ) -> 'Clip':
        """
        Place a full transparent background
        behind the video if its size its not
        our default 1920x1080 scene and also
        places this video on the center of
        the background.

        This method generates a copy of the
        original video so it remains
        unchanged.
        """
        return wrap_video_with_transparent_background(self.video)

    def __init__(
        self,
        video: Union[str, Clip],
        is_mask: Union[bool, None] = None,
        do_include_mask: Union[bool, None] = None,
        do_force_60_fps: bool = True,
        do_fix_duration: bool = False
    ):
        """
        If 'is_mask' or 'do_include_mask' is None is 
        because we don't know and/or it must be handled
        automatically
        """
        # TODO: What about 'str' video (?)
        # TODO: Is this 'Clip' validating properly (?)
        ParameterValidator.validate_mandatory_instance_of('video', video, Clip)
        ParameterValidator.validate_bool('is_mask', is_mask)
        ParameterValidator.validate_bool('do_include_mask', do_include_mask)
        ParameterValidator.validate_mandatory_bool('do_force_60_fps', do_force_60_fps)
        ParameterValidator.validate_mandatory_bool('do_fix_duration', do_fix_duration)
        
        # A moviepy video can be a 'normal'
        # video or a 'mask' video. Remember,
        # a 'normal' video can have another
        # 'mask' video attached, but a 'mask'
        # video cannot ('normal' nor 'mask')
        is_mask = (
            is_mask
            if is_mask is not None else
            # TODO: Maybe auto-check? How (?)
            False
        )

        # If a 'normal' video, we need to
        # include the mask if requested
        # (and if existing)
        do_include_mask = (
            do_include_mask
            if do_include_mask is not None else
            False
        )

        # Force to read the video with or
        # without mask and recalculating
        # the duration if needed
        video = VideoParser.to_moviepy(
            video,
            do_include_mask = do_include_mask,
            do_calculate_real_duration =  do_fix_duration
        )

        # Forcing the fps to be 60 solves a
        # problem with some strange fps values
        # like 29.97 and also makes easier
        # handling the videos
        video = (
            video.with_fps(60)
            if do_force_60_fps else
            video
        )

        # Solve the moviepy bug about some
        # unreadable frames at the end that
        # make the video having not the
        # expected duration
        video = (
            video.subclipped(0, calculate_real_video_duration(video))
            if do_fix_duration else
            video
        )

        self.video = video
        """
        The moviepy original clip.
        """