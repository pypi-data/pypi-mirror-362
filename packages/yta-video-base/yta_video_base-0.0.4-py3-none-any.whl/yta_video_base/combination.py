from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.position import Position, DependantPosition, get_moviepy_upper_left_position
from yta_multimedia.video.edition.duration import set_video_duration
from yta_audio.silences import AudioSilence
# TODO: Where is this method now (?)
from yta_multimedia.video.dimensions import resize_video
from yta_constants.video import VideoCombinatorAudioMode
from yta_validation import PythonValidator
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip, CompositeAudioClip
from typing import Union


class VideoAudioCombinator:
    """
    Class to simplify and encapsulate the way we handle
    the audio combination between videos.
    """

    _audio_mode: VideoCombinatorAudioMode = None

    def __init__(
        self,
        audio_mode: VideoCombinatorAudioMode = VideoCombinatorAudioMode.BOTH_CLIPS_AUDIO
    ):
        self._audio_mode = (
            VideoCombinatorAudioMode.to_enum(audio_mode)
            if audio_mode is not None else
            VideoCombinatorAudioMode.default()
        )

    def process_audio(
        self,
        main_video: Clip,
        added_video: Clip
    ):
        """
        Process the 'video' and 'background_video' audios
        according to the instance audio mode defined when
        instantiated.

        This method must be called just before combining
        the videos and after video enlargment has been
        applied (if needed).
        """
        # TODO: What about silence 'frame_rate' (?)
        added_video_audio = (
            added_video.audio
            if added_video.audio is not None else
            AudioSilence.create(added_video.duration)
        )
        main_video_audio = (
            main_video.audio
            if main_video.audio is not None else
            AudioSilence.create(main_video.duration)
        )

        return {
            VideoCombinatorAudioMode.BOTH_CLIPS_AUDIO: lambda: CompositeAudioClip([
                added_video_audio, 
                main_video_audio
            ]),
            VideoCombinatorAudioMode.ONLY_MAIN_CLIP_AUDIO: lambda: main_video_audio,
            VideoCombinatorAudioMode.ONLY_ADDED_CLIP_AUDIO: lambda: added_video_audio
        }[self._audio_mode]()

class VideoCombinator:
    """
    A class to encapsulate and simplify the way we
    combine videos.
    """

    _audio_combinator: VideoAudioCombinator = None

    def __init__(
        self,
        audio_mode: VideoCombinatorAudioMode = VideoCombinatorAudioMode.BOTH_CLIPS_AUDIO
    ):
        self._audio_combinator = VideoAudioCombinator(audio_mode)

    def video_cover_video(
        self,
        video: Clip,
        background_video: Clip
    ) -> CompositeVideoClip:
        """
        Place the provided 'video' covering the 'background_video'.

        The 'video' will be forced to last the same as the 
        'background_video' to be able to cover it.

        TODO: Explain more
        """
        background_video = VideoParser.to_moviepy(background_video)
        video = VideoParser.to_moviepy(video)

        # We adjust the 'video' size to cover the 
        # 'background_video'
        video = resize_video(video, background_video.size)

        return self.video_over_video(video, background_video, Position.CENTER)

    def video_over_video(
        self,
        video: Clip,
        background_video: Clip,
        position: Union[Position, DependantPosition, tuple, list]
    ) -> CompositeVideoClip:
        """
        Place the provided 'video' over the 'background_video'
        in the given 'position' (adapted to the real background
        video size). The 'background_video' will be played 
        entirely, and the 'video' clip will be enlarged 
        according to our default enlarging videos strategy. So,
        you should call this method with the parts of the videos
        you want actually combine entirely and pre-processed.

        Pay attention to the size of the videos you provide as
        this method is not considering this part.

        This method returns a CompositeVideoClip with both 
        videos combined.
        """
        if (
            not PythonValidator.is_instance(position, [Position, DependantPosition]) and
            not PythonValidator.is_tuple(position) and
            not PythonValidator.is_list(position)
        ):
            raise Exception('The provided "position" is not valid, it must be a Position, DependantPosition or a tuple or list with 2 values.')
        
        background_video = VideoParser.to_moviepy(background_video)
        video = VideoParser.to_moviepy(video)

        # TODO: What about sizes (?)

        # TODO: This length strategy is open to changes
        video = set_video_duration(video, background_video.duration)

        # We will place the 'video's center in the 'position'
        # but of the provided 'background_video'
        position = (
            position.get_moviepy_upper_left_corner_tuple(video.size, background_video.size)
            if PythonValidator.is_instance(position, Position) else
            position.get_moviepy_position_upper_left_corner(video.size, background_video.size)
            if PythonValidator.is_instance(position, DependantPosition) else
            get_moviepy_upper_left_position(background_video.size, video.size, position)
        )

        video = video.with_position(position)

        return CompositeVideoClip([
            background_video,
            video
        ]).with_audio(self._audio_combinator.process_audio(background_video, video))