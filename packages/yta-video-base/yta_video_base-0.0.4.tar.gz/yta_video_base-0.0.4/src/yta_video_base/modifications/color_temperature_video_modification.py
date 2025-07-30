from yta_video_base.modifications.video_modification import VideoModification
from yta_multimedia.video.edition.video_editor import VideoEditor
from moviepy.Clip import Clip


class ColorTemperatureVideoModification(VideoModification):
    factor: int = None
    
    def __init__(
        self,
        start_time: float,
        end_time: float,
        layer: int,
        factor: int = 45
    ):
        super().__init__(start_time, end_time, layer)
        
        # TODO: Validate that 'factor' is actually between
        # the limits
        self.factor = factor

    def _modificate(self, video: Clip) -> Clip:
        # TODO: What do I do with the VideoEditor (?)
        return VideoEditor(video).change_color_temperature(self.factor)