from yta_validation.number import NumberValidator

import random


SMALL_AMOUNT_TO_FIX = 0.0000000001
"""
Small amount we need to add to fix some floating
point number issues we've found. Something like
0.3333333333333326 will turn into 9 frames for a 
fps = 30 video, but this is wrong, as it should
be 10 frames and it is happening due to a minimal
floating point difference.
"""

# Below extracted from MPVideo
def get_frame_indexes(
    duration: float,
    fps: float
):
    """
    Get the list of the frame indexes of
    the video with the given 'duration'
    and 'fps'.

    If a video lasts 1 second and has 5
    fps, this method will return: 0, 1,
    2, 3, 4.
    """
    return [
        i
        for i in range(int(duration * fps + SMALL_AMOUNT_TO_FIX))
    ]

def get_first_n_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the first 'n' frames indexes of the current
    video to be able to use them within a condition
    with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_odd_frames_indexes(duration, fps)[:n]

def get_last_n_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the last 'n' frames indexes of the current
    video to be able to use them within a condition
    with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_odd_frames_indexes(duration, fps)[-n:]

def get_even_frames_indexes(
    duration: float,
    fps: float
):
    """
    Array containing all the even indexes of video
    frames that can be used to obtain its corresponding
    frame time moment, or to simplify calculations.
    """
    frame_indexes = get_frame_indexes(duration, fps)

    return frame_indexes[frame_indexes % 2 == 0]

def get_first_n_even_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the first 'n' even frames indexes of the 
    current video to be able to use them within a
    condition with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    If 'n' is greater than the real number of even
    frames, 'n' will get that value so the result will
    be all the even frames indexes.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_even_frames_indexes(duration, fps)[:n]

def get_last_n_even_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the last 'n' even frames indexes of the
    current video to be able to use them within a
    condition with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    If 'n' is greater than the real number of even
    frames, 'n' will get that value so the result will
    be all the even frames indexes.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_even_frames_indexes(duration, fps)[-n:]

def get_odd_frames_indexes(
    duration: float,
    fps: float,
):
    """
    Array containing all the odd indexes of video
    frames that can be used to obtain its corresponding
    frame time moment, or to simplify calculations.
    """
    frame_indexes = get_frame_indexes(duration, fps)

    return frame_indexes[frame_indexes % 2 != 0]

def get_last_n_odd_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the last 'n' odd frames indexes of the
    current video to be able to use them within a
    condition with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    If 'n' is greater than the real number of odd
    frames, 'n' will get that value so the result will
    be all the odd frames indexes.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_odd_frames_indexes(duration, fps)[-n:]

def get_first_n_odd_frames_indexes(
    duration: float,
    fps: float,
    n: int
):
    """
    Obtain the first 'n' odd frames indexes of the 
    current video to be able to use them within a
    condition with the '.get_frame(t)' method.

    This list can be used to check if the current frame
    number (index) is on it or not, to apply the frame
    image effect or to leave it as it is.

    If 'n' is greater than the real number of odd
    frames, 'n' will get that value so the result will
    be all the odd frames indexes.

    Each frame time moment has been increased by 
    a small amount to ensure it is greater than 
    the base frame time value (due to decimals
    issue).
    """
    return get_odd_frames_indexes(duration, fps)[:n]

def get_frame_time_moments(
    duration: float,
    fps: float
):
    """
    Get the time moment of each video
    frame according to the provided video
    'duration' and 'fps'. This will always
    include the second 0 and the
    inmediately before the duration.

    If a video lasts 1 second and has 5
    fps, this method will return: 0, 0.2,
    0.4, 0.6, 0.8.

    This method can return non-exact
    decimal values so we recommend you to
    add a small amount to ensure it is
    above the expected base frame time.
    """
    return [
        (1 / fps * i) + SMALL_AMOUNT_TO_FIX
        for i in range(int(duration * fps + SMALL_AMOUNT_TO_FIX) + 1)
    ][:-1]

def frame_time_to_frame_index(
    t: float,
    fps: float
):
    """
    Transform the provided 't' frame time to 
    its corresponding frame index according
    to the 'fps' provided.

    This method applies the next formula:

    int(t * fps + SMALL_AMOUNT_TO_FIX)
    """
    return int((t + SMALL_AMOUNT_TO_FIX) * fps)

def frame_index_to_frame_time(
    i: int,
    fps: float
):
    """
    Transform the provided 'i' frame index to
    its corresponding frame time according to
    the 'fps' provided.

    This method applies the next formula:

    i * 1 / fps + SMALL_AMOUNT_TO_FIX
    """
    return i * 1 / fps + SMALL_AMOUNT_TO_FIX

# Other more complex utils, extracted
# from VideoFrameTHelper
def get_video_frames_indexes_from_duration_and_fps(
    duration: float,
    fps: float,
    do_invert_order: bool = False
):
    """
    Get all the video frame indexes that
    a video with the 'duration' and 'fps'
    given, ordered from first to last if
    'do_invert_order' is False, or from
    last to first if it is True.
    """
    return (
        list(range(get_number_of_frames(duration, fps) - 1, -1, -1))
        if do_invert_order else
        list(range(get_number_of_frames(duration, fps)))
    )

def get_video_frames_indexes_from_number_of_frames(
    number_of_frames: int,
    do_invert_order: bool = False
):
    """
    Get all the video frame indexes that
    a video with the 'number_of_frames'
    given, ordered from first to last if
    'do_invert_order' is False, or from
    last to first if it is True.
    """
    return (
        list(range(number_of_frames - 1, -1, -1))
        if do_invert_order else
        list(range(number_of_frames))
    )

def get_video_frames_ts_from_duration_and_fps(
    duration: float,
    fps: float
):
    """
    Get all the video frame time moments
    t for a video with the provided
    'duration' and 'fps'. Each 't' includes
    a small amount increased to fix some
    issues.
    """
    return [
        get_frame_t_from_frame_index(i, fps)
        for i in get_video_frames_indexes_from_duration_and_fps(duration, fps)
    ]

def get_video_frames_ts_from_number_of_frames(
    number_of_frames: int,
    fps: float
):
    """
    Get all the video frame time moments
    t for a video with the provided
    'number_of_frames'. Each 't' includes
    a small amount increased to fix some
    issues.
    """
    return [
        get_frame_t_from_frame_index(i, fps)
        for i in get_video_frames_indexes_from_number_of_frames(number_of_frames)
    ]

def get_frame_t_from_frame_index(
    index: int,
    fps: float
) -> float:
    """
    Get the frame time moment 't' from
    the given 'index' and the provided
    video 'fps'.
    """
    return index / fps + SMALL_AMOUNT_TO_FIX

def get_frame_index_from_frame_t(
    t: float,
    fps: float
) -> int:
    """
    Get the frame index from the given
    frame time moment 't' and the also
    provided video 'fps'.
    """
    frame_duration = 1 / fps

    return int((t + SMALL_AMOUNT_TO_FIX) // frame_duration)

def get_frame_t_base(
    t: float,
    fps: float
):
    """
    Get the base frame time moment t
    (the one who is the start of the
    frame time interval plus a small
    amount to fix issues) from the 
    given time moment 't' of the video
    with the also provided 'fps'.
    """
    return get_frame_index_from_frame_t(t, fps) / fps + SMALL_AMOUNT_TO_FIX

def get_video_audio_tts_from_video_frame_t(
    video_t: float,
    video_fps: float,
    audio_fps: float
):
    """
    Get all the audio time moments
    attached to the given video time
    moment 't', as an array.

    One video time moment 't' includes
    a lot of video audio 't' time 
    moments. The amount of video audio
    frames per video frame is calculated
    with the division of the audio fps
    by the video fps.

    The result is an array of 't' video
    audio time moments. Maybe you need
    to turn it into a numpy array.

    This is useful to obtain all the 
    video audio time moments attached to
    the given video time moment 
    'video_t'.
    """
    from yta_general_utils.math.progression import Progression

    audio_frames_per_video_frame = int(audio_fps / video_fps)
    audio_frame_duration = 1 / audio_fps
    video_frame_duration = 1 / video_fps

    t = get_frame_t_base(video_t, video_fps)

    return Progression(
        start = t, 
        end = t + video_frame_duration - audio_frame_duration,
        n = audio_frames_per_video_frame
    ).values

def get_video_frame_t_from_video_audio_frame_t(
    audio_t: float,
    video_fps: float
):
    """
    Get the video frame time moment t
    from the given video udio frame time
    moment 'audio_t', according to its
    'video_fps' frames per second.

    This method is useful to obtain the
    video frame attached to the given
    audio time moment 'audio_t'.
    """
    return get_frame_t_base(audio_t , video_fps)

def get_video_frame_index_from_video_audio_frame_index(
    audio_index: int,
    video_fps: float,
    audio_fps: float
):
    """
    Get the video frame index from the
    provided video audio frame index
    'audio_index', using the also given
    'video_fps' and 'audio_fps'.
    """
    return round(audio_index * (video_fps / audio_fps))

def get_video_frame_t_from_video_audio_frame_index(
    audio_index: int,
    video_fps: float,
    audio_fps: float
):
    """
    Get the video frame time moment t
    from the given video audio frame
    index 'audio_index', using the also
    provided 'video_fps' and 
    'audio_fps'.
    """
    return get_frame_t_from_frame_index(
        get_video_frame_index_from_video_audio_frame_index(
            audio_index,
            video_fps,
            audio_fps
        ),
        video_fps
    )

def get_video_frame_index_from_video_audio_frame_t(
    audio_t: float,
    video_fps: float,
    audio_fps: float
):
    """
    Get the video frame index from the
    the given video audio frame time
    moment 'audio_t', using the also
    provided 'video_fps' and 'audio_fps'.
    """
    return get_video_frame_index_from_video_audio_frame_index(
        get_frame_index_from_frame_t(
            audio_t,
            audio_fps
        ),
        video_fps,
        audio_fps
    )



# Based on properties of MPVideo
def get_frame_duration(
    fps: float
) -> float:
    """
    Get the frame duration based on the
    video frames per second ('fps')
    provided.

    The formula is:
    - `1 / fps`
    """
    return 1 / fps

def get_number_of_frames(
    duration: float,
    fps: float
) -> int:
    """
    Get the number of frames of the video
    with the given 'duration' and 'fps'
    and using a small amount to fix the
    rounding bug.

    The formula is:
    - `int(duration * fps + SMALL_AMOUNT)`
    """
    return int(duration * fps + SMALL_AMOUNT_TO_FIX)