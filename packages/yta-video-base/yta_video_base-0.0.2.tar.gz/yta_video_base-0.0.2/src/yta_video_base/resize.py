from yta_constants.video import ResizeMode


def resize_video(
    video: 'Clip',
    size: tuple[int, int],
    resize_mode: ResizeMode = ResizeMode.RESIZE_KEEPING_ASPECT_RATIO
):
    """
    Make the provided 'video' fit the
    also provided 'size' by applying
    the given 'resize_mode' strategy.
    """
    # TODO: This generates a cyclic import issue
    #from yta_multimedia.video.parser import VideoParser
    
    #video = VideoParser.to_moviepy(video)

    if (video.w, video.h) == size:
        return video

    resize_mode = (
        ResizeMode.to_enum(resize_mode)
        if resize_mode is not None else
        ResizeMode.default()
    )

    # TODO: Maybe I could use a simulated image of provided
    # size and use the existing resizing methods
    if resize_mode == ResizeMode.RESIZE:
        video = video.resized(size)
    elif resize_mode == ResizeMode.RESIZE_KEEPING_ASPECT_RATIO:
        # We need to resize it first until we reach the greatest
        # dimension (width or height depending on the source element)
        original_ratio = video.w / video.h
        new_ratio = size[0] / size[1]

        if original_ratio > new_ratio:
            # Original video is wider than the expected one
            video = video.resized(height = size[1])
        elif original_ratio < new_ratio:
            # Original video is higher than the expected one
            video = video.resized(width = size[0])
        else:
            video = video.resized(size)

        # Now, with the new video resized, we look for the
        # cropping points we need to apply and we crop it
        top_left, bottom_right = get_cropping_points_to_keep_aspect_ratio((video.w, video.h), size)
        # Crop the video to fit the desired aspect ratio
        # TODO: Maybe avoid this if nothing to crop
        video = video.with_effects([Crop(width = bottom_right[0] - top_left[0], height = bottom_right[1] - top_left[1], x_center = video.w / 2, y_center = video.h / 2)])
        # Resize it to fit the desired 'size'
        video = video.resized(size)
    elif resize_mode == ResizeMode.FIT_LIMITING_DIMENSION:
        # We need to resize setting the most limiting dimension
        # to the one provided in the expected 'size' and then
        # place it over a background
        original_ratio = video.w / video.h
        new_ratio = size[0] / size[1]

        if original_ratio > new_ratio:
            # Original video is wider than the expected one
            video = video.resized(height = size[1])
        elif original_ratio < new_ratio:
            # Original video is higher than the expected one
            video = video.resized(width = size[0])
        else:
            video = video.resized(size)

        video = CompositeVideoClip([
            ClipGenerator.get_default_background_video(size = size, duration = video.duration, fps = video.fps, is_transparent = False),
            video.with_position(('center', 'center'))
        ])
    elif resize_mode == ResizeMode.BACKGROUND:
        if video.w > size[0] or video.h > size[1]:
            video = resize_video(video, size, ResizeMode.FIT_LIMITING_DIMENSION)
        else:
            # Just place it in the center of a black background
            video = CompositeVideoClip([
                ClipGenerator.get_default_background_video(size = size, duration = video.duration, fps = video.fps, is_transparent = False),
                video.with_position(('center', 'center'))
            ])

    return video