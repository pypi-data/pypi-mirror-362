from yta_video_base.concatenation import concatenate_videos
from yta_video_base.generator import MoviepyNormalClipGenerator
from yta_constants.video import ExtendVideoMode, EnshortVideoMode
from yta_validation.parameter import ParameterValidator
from typing import Union


def set_video_duration(
    video: Union[str, 'Clip'],
    duration: float,
    extend_mode: Union[ExtendVideoMode, None] = None,
    enshort_mode: Union[EnshortVideoMode, None] = None
):
    """
    Get a copy of the provided 'video' with
    the provided 'duration' by applying the
    strategy the also given 'extend_mode'
    and 'enshort_mode' determine.

    If the 'duration' provided is smaller
    than the original duration, the enshort
    strategy will be applied. If it is 
    bigger, the enlarge strategy will be 
    used.

    There are some options that don't modify
    the video duration, so use the different
    options carefully.
    """
    ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
    video = VideoParser.to_moviepy(video)

    extend_mode = (
        ExtendVideoMode.to_enum(extend_mode)
        if extend_mode is not None else
        None
    )
    enshort_mode = (
        EnshortVideoMode.to_enum(enshort_mode)
        if extend_mode is not None else
        None
    )

    final_video = video.copy()

    if (
        (
            video.duration > duration and
            enshort_mode is None
        ) or
        (
            video.duration < duration and
            extend_mode is None
        )
    ):
        return final_video

    if video.duration > duration:
        # We need to enshort it
        if enshort_mode == EnshortVideoMode.CROP:
            final_video = final_video.with_subclip(0, duration)
        elif enshort_mode == EnshortVideoMode.SPEED_UP:
            final_video = FitDurationEffect().apply(video, duration)
            #final_video = final_video.with_effects([MultiplySpeed(final_duration = duration)])
            # TODO: Remove this below when effects reviewed and
            # functionality is working perfectly
            #final_video = ChangeSpeedVideoEffect.apply(final_video, duration)
    elif video.duration < duration:
        # We need to enlarge it
        remaining_time = duration % video.duration

        if extend_mode == ExtendVideoMode.LOOP:
            times_to_loop = int((duration / video.duration) - 1)
            for _ in range(times_to_loop):
                final_video = concatenate_videos([
                    final_video,
                    video
                ])
            final_video = concatenate_videos([final_video, video.with_subclip(0, remaining_time)])
        elif extend_mode == ExtendVideoMode.FREEZE_LAST_FRAME:
            remaining_time = duration - video.duration
            frame = VideoFrameExtractor.get_frame_by_t(video, video.duration)
            frame_freezed_video = generate_video_from_image(frame, remaining_time, fps = video.fps)
            final_video = concatenate_videos([
                video,
                frame_freezed_video
            ])
        elif extend_mode == ExtendVideoMode.SLOW_DOWN:
            final_video = FitDurationEffect().apply(video, duration)
            #final_video = final_video.with_effects([MultiplySpeed(final_duration = duration)])
            # TODO: Remove this below when effects reviewed and
            # functionality is working perfectly
            #final_video = ChangeSpeedVideoEffect.apply(final_video, duration)
        elif extend_mode == ExtendVideoMode.BLACK_TRANSPARENT_BACKGROUND:
            final_video = concatenate_videos([
                video,
                MoviepyNormalClipGenerator.get_static_default_color_background(
                    size = video.size,
                    duration = remaining_time,
                    fps = video.fps,
                    is_transparent = False
                )
            ])

    return final_video