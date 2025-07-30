from yta_video_base.modifications.video_modification import VideoModification
from yta_validation import PythonValidator
from moviepy.Clip import Clip


class VideoModifications:
    """
    Class to encapsulate different VideoModifications and
    to apply them in the order they must be applied.
    """
    _modifications: list[VideoModification] = None

    @property
    def modifications(self):
        """
        Return the list of 'modifications' sorted by
        layer and 'start_time' in ascending order.

        This means that the lowest layers are returned
        first, and for each 'layer' they are sorted by
        'start_time' in ascending order.
        """
        return sorted(self._modifications, key = lambda modification: (modification.layer, modification.start_time))

    # TODO: What about the type of modification? Maybe
    # I want to apply effects before greenscreens if
    # they are in the same layer, so I have to specify
    # one strategy when this happens

    def __init__(
        self,
        modifications: list[VideoModification]
    ):
        if not PythonValidator.is_list_of(modifications, VideoModification):
            raise Exception('Not all the elements in the "modifications" parameter provided are VideoModification instances.')

        self._modifications = modifications

    def apply(
        self,
        video: Clip
    ) -> Clip:
        for modification in self.modifications:
            previous_duration = video.duration
            
            video = modification.apply(video)

            if previous_duration != video.duration:
                # TODO: update the next modifications to
                # fit the new durations
                pass

        return video