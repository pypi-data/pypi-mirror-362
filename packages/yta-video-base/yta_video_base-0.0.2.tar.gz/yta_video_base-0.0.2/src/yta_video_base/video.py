from yta_video_base.utils import calculate_real_video_duration, wrap_video_with_transparent_background
from yta_video_base.frame.utils import get_number_of_frames, get_frame_duration
from yta_validation.parameter import ParameterValidator


class VVideo:
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
        video: 'Clip',
        do_force_60_fps: bool = True,
        do_fix_duration: bool = False
    ):
        ParameterValidator.validate_mandatory_instance_of('video', video, ['Clip', 'VideoFileClip', 'VideoClip'])
        ParameterValidator.validate_mandatory_bool('do_force_60_fps', do_force_60_fps)
        ParameterValidator.validate_mandatory_bool('do_fix_duration', do_fix_duration)
        
        video = (
            video.with_fps(60)
            if do_force_60_fps else
            video
        )
        video = (
            video.with_subclip(0, calculate_real_video_duration(video))
            if do_fix_duration else
            video
        )

        self.video = video
        """
        The moviepy original clip.
        """

    # TODO: Interesting method I should
    # preserve but in a better way
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