"""
Module dedicated to concatenation of
videos.
"""
from yta_video_base.parser import VideoParser
from yta_video_base.utils import wrap_video_with_transparent_background
from yta_validation import PythonValidator
from moviepy import concatenate_videoclips as concatenate_videoclips_moviepy


@staticmethod
def concatenate_videos(
    videos: list['Clip']
):
    """
    Concatenate the provided 'videos' but fixing the
    videos dimensions. It will wrap any video that
    doesn't fit the 1920x1080 scene size with a full
    transparent background to fit those dimensions.
    """
    videos = (
        [videos]
        if not PythonValidator.is_list(videos) else
        videos
    )

    videos = [
        wrap_video_with_transparent_background(video) 
        for video in [
            VideoParser.to_moviepy(video)
            for video in videos
        ]
    ]
    
    return concatenate_videoclips_moviepy(videos)