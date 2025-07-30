from yta_video_base.subclip import subclip_video
from yta_validation.parameter import ParameterValidator
from moviepy.Clip import Clip
from moviepy import concatenate_videoclips
from abc import ABC, abstractmethod


class VideoModification(ABC):
    """
    A modification that must be applied in a video. This
    class must be implemented by the specific video
    modifications.
    """
    start_time: float = None
    end_time: float = None
    layer: int = None
    
    def __init__(
        self,
        start_time: float,
        end_time: float,
        layer: int
    ):
        ParameterValidator.validate_mandatory_positive_number('start_time', start_time, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('end_time', end_time, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_int('layer', layer, do_include_zero = True)
        
        if end_time <= start_time:
            raise Exception('The provided "end_time" is before the also provided "start_time".')
        
        self.start_time = start_time
        self.end_time = end_time
        self.layer = layer

    def apply(
        self,
        video: Clip
    ):
        """
        Apply the modification making the necessary subclips.
        This method will apply the modification that must be
        set in the 'apply' method in the subclass subclipping
        the necessary according to the 'start_time' and
        'end_time'.
        """
        if (
            self.start_time > video.duration or
            self.end_time > video.duration
        ):
            raise Exception('This VideoModification cannot be applied in the provided "video".')

        left_clip, center_clip, right_clip = subclip_video(video, self.start_time, self.end_time)
        center_clip = self._modificate(center_clip)

        clips = [
            clip
            for clip in [left_clip, center_clip, right_clip]
            if clip is not None
        ]

        return concatenate_videoclips(clips)

    @abstractmethod
    def _modificate(
        self,
        video: Clip
    ):
        """
        Method to be specifically set in each modification
        with the custom video modification code. This method
        will generate a video that will replace the original
        'video' provided.

        Do not call this method, call the '.apply()' method
        to actually apply it.
        """
        pass