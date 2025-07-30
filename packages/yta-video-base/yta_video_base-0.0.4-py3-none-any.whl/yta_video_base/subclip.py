"""
All this file is currently in 'yta_multimedia' library
because I'm testing it, but the concepts contained in
this file don't belong to this library because they are
related to a VideoEditor concept, not to image or video
simple editing.

We need to handle, when working in building a whole video
project, videos as SubClips so we handle all attributes
and, if we subclip a SubClip instance, we .copy() the
previous attributes to the left, center and right clips
we obtain when subclipping. This would preserve previous
configurations and let us manage all the clips, so we
work on top of moviepy library in any change we process
and use moviepy only for basic and frame transformations.

TODO: These classes below will be moved in a near future
to its own project or to 'youtube_autonomous'.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.edition.settings import VOLUME_LIMIT, ZOOM_LIMIT, LAYERS_INDEXES_LIMIT, COLOR_TEMPERATURE_LIMIT, MAX_TIMELINE_LAYER_DURATION, BRIGHTNESS_LIMIT, CONTRAST_LIMIT, WHITE_BALANCE_LIMIT, SHARPNESS_LIMIT, SPEED_FACTOR_LIMIT, ROTATION_LIMIT
from yta_multimedia.video.edition.video_frame_t_helper import VideoFrameTHelper
from yta_multimedia.video.edition.settings import SMALL_AMOUNT_TO_FIX
from yta_constants.multimedia import DEFAULT_SCENE_SIZE
from yta_audio.edition.audio_frame_editor import AudioFrameEditor
from yta_image.edition.editor import ImageEditor
from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_validation.number import NumberValidator
from yta_constants.enum import YTAEnum as Enum
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip, concatenate_videoclips
from typing import Union

import numpy as np


END_OF_CLIP = 999999
END_OF_TIMELINE = 120
"""
The limit of the timeline length. It is not possible
to generate a project which length is larger than 
this value.

TODO: This value could be very low in alpha and beta
versions for testing.
"""

# TODO: Move this decorator below to another place (?)
def unset_video_processed(
    func
):
    """
    Decorator function that sets the '_video_processed'
    attribute to None to indicate that it has been
    modified and it must be processed again.
    """
    def wrapper(self, value):
        value = func(self, value)
        self._video_processed = None
        
        return value
    
    return wrapper


from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from yta_general_utils.math.progression import Progression


class SubClipAttributeModifier:
    """
    Class to encapsulate the possible ways to modify a 
    video attribute.

    This will be passed as an instance to a SubClip to 
    calculate the modification values array for each 
    frame and set those modifying values in the video
    instance to be lately applied to the video when
    processing it.

    This is a wrapper to simplify the way we interact
    with different object types valid to generate
    values.

    The only accepted values by now are:
    - Single value
    - SubClipSetting
    - Graphic
    """
    modifier: Union[any, 'SubClipSetting', 'Graphic'] = None

    @property
    def is_single_value(
        self
    ) -> bool:
        """
        Return True if the modifier is just a single value.
        """
        return PythonValidator.is_number(self.modifier)

    def __init__(
        self,
        modifier: Union[any, 'SubClipSetting', 'Graphic']
    ):
        # TODO: Change SubClipSetting name as its purpose is
        # now different and not to appropiate for this
        if (
            # TODO: Maybe we accept some non-numeric modifier
            # single values (?)
            not PythonValidator.is_number(modifier) and
            not PythonValidator.is_instance(modifier, 'SubClipSetting') and
            not PythonValidator.is_instance(modifier, 'Graphic')
        ):
            raise Exception('The provided "modifier" parameter is not a valid modifier.')
        
        self.modifier = modifier

    def get_values(
        self,
        n: float
    ):
        """
        Obtain an array of 'n' values that will modify the
        attribute this instance is designed for. The 'n'
        value must be the number of frames.
        """
        # I don't like float 'fps' but it is possible, and I
        # should force any clip to be 30 or 60fps always
        return (
            [self.modifier] * n
            if PythonValidator.is_number(self.modifier) else
            self.modifier.get_values(n)
            if PythonValidator.is_instance(self.modifier, 'SubClipSetting') else
            [
                self.modifier.get_xy_from_normalized_d(d)[1]
                for d in Progression(0, 1, n).values
            ]
            if PythonValidator.is_instance(self.modifier, 'Graphic') else
            1 # TODO: What about this option (?)
        )
        # if PythonValidator.is_number(self.modifier): return [self.modifier] * n
        # if PythonValidator.is_instance(self.modifier, 'SubClipSetting'): return self.modifier.get_values(n)
        # if PythonValidator.is_instance(self.modifier, 'Graphic'): return [self.modifier.get_xy_from_normalized_d(d)[1] for d in Progression(0, 1, n).values]

    def validate_values(
        self,
        n: float,
        limit: list[float, float]
    ):
        """
        Validate that any of those 'values' is between the
        limit range. The 'n' parameter must be the number of
        frames in the video, and 'limit' a tuple of the lower
        and upper limit.

        This method must be called when a SubClipAttributeModifier
        instance is set in a SubClip because we know the number
        of frames and the limit for that specific attribute (it
        is being added to that attribute modifier) in that 
        moment.
        """
        if any(
            (
                value < limit[0] or
                value > limit[1]
            )
            for value in self.get_values(n)
        ):
            raise Exception(f'One of the generated "values" is out of the limit [{limit[0]}, {limit[1]}]')

    def copy(
        self
    ):
        """
        Make a copy of the instance.
        """
        return SubClipAttributeModifier(self.modifier.copy())


# TODO: Think again about this because now we have the
# SubClipAttributeModifier to be passed as the modifier
# and it accepts this SubClipSetting, that must be renamed
# for its new purpose
class SubClipSetting:
    """
    Class to represent a video setting to be able to handle
    dynamic setting values and not only simple values. This
    means we can make a video go from 0 contrast to 10 
    contrast increasing it smoothly (for example: 0, 2, 4,
    6, 8 and 10) and not only abruptly (from 0 in one frame
    to 10 in the next frame).
    """

    initial_value: float = None
    final_value: float = None
    rate_function: RateFunctionArgument = None
    _values: list[float] = None
    """
    The list of values calculated in a previous method call
    to avoid recalculating them. The amount of elements is
    the amount of steps used in the previous calculation.
    """

    def __init__(
        self,
        initial_value: float,
        final_value: float,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        # TODO: Maybe validate something? I don't know the
        # limits because each setting is different, but by
        # now I'm verifying the 'initial_value' and the
        # 'final_value' when using them on a SubClip
        self.initial_value = initial_value
        self.final_value = final_value
        self.rate_function = rate_function

    def get_values(
        self,
        steps: int
    ):
        """
        Obtain an array with the values between the 'initial_value'
        and the 'final_value' according to the 'rate_function'.

        The 'steps' parameter must be the amount of frames in which
        we are planning to apply this setting so we are able to read
        the value for each frame according to its index.
        """
        # Same limits cannot be handled by the Progression class as
        # it is just an array of the same value repeated 'steps' 
        # times
        if self.initial_value == self.final_value:
            return [
                self.initial_value
                for _ in range(steps)
            ]
        
        if self._values is None or len(self._values) != steps:
            # We recalculate only if needed
            self._values = Progression(self.initial_value, self.final_value, steps, self.rate_function).values
            
        return self._values
    
    def copy(
        self
    ):
        """
        Make a copy of the instance.
        """
        return SubClipSetting(
            self.initial_value,
            self.final_value,
            self.rate_function
        )


class SubClip:
    """
    Class to represent a subclip of a clip in which we
    can apply different modifications such as color
    temperature, zoom, movement, etc.

    This class represent the same as one of the subclips
    in any of your video editor apps.
    """

    # TODO: This, as the original video clip (moviepy),
    # maybe must be private to avoid using it directly
    video: Clip = None
    _video_processed: Clip = None
    """
    The video once it's been processed with all its
    attributes and effects.
    """
    # TODO: Add all needed attributes
    # Volume
    _volume: list[float] = None
    """
    A single value or a list of values for the volume 
    modification in which the whole video audio volume
    is modified by that single factor or those factor
    values.
    """

    # Attributes that can be modified
    _color_temperature: list[float] = None
    """
    A list of values for the color temperature modification
    in which each position is the modifier for each video
    frame.
    """
    _brightness: list[float] = None
    """
    A list of values for the brightness modification in
    which each position is the modifier for each video
    frame.
    """
    _contrast: list[float] = None
    """
    A list of values for the contrast modification in which
    each position is the modifier for each video frame.
    """
    _sharpness: list[float] = None
    """
    A list of values for the sharpness modification in which
    each position is the modifier for each video frame.
    """
    _white_balance: list[float] = None
    """
    A list of values for the white balance modification in
    which each position is the modifier for each video frame.
    """

    # Special modifiers
    # TODO: This is special because it affects to the video
    # duration. It has to be applied at the end
    _speed_factor: Union[float, list[float]] = None
    """
    A single value or a list of values for the speed 
    modification in which the whole video duration is
    modified by that single speed factor or those speed
    factor values.
    """

    # Zoom, movement and rotation. These attributes are
    # single values that are changed the base clip size,
    # position and rotation.
    _zoom: float = None
    """
    A single value to zoom the clip.
    """
    _x_movement: float = None
    """
    A single value to move the clip in X axis.
    """
    _y_movement: float = None
    """
    A single value to move the clip in Y axis.
    """
    _rotation: float = None
    """
    A single value to rotate the clip in clockhise.
    """

    # These 3 values below are the most especial ones
    # because are the ones that actually build the
    # video by applying other effects or attributes
    # on themselves
    _resized: list[tuple[float, float]] = None
    """
    A list of tuples with the width and height resize
    factors that must be applied for each frame to 
    the original video.
    """
    _with_position: list[tuple[int, int]] = None
    """
    A list of positions in which the center of the
    video must be placed. These positions must be
    transformed into upper left corner positions just
    when processing and rendering.
    """
    _rotated: list[int] = None
    """
    A list of rotation angles for each frame of the
    video.

    The rotation effect makes a frame with a new size
    so it has to be considered when positioning to
    calculate the actual size of each frame.
    """
    
    # Custom effects
    _effects: list['SEffect'] = None

    @staticmethod
    def init(
        video: Clip,
        start_time: Union[float, None] = 0,
        end_time: Union[float, None] = END_OF_CLIP
    ):
        """
        This is the only method we need to use when instantiating
        a SubClip so we can obtain the left and right clip result
        of the subclipping process and also the new SubClip
        instance.

        This method returns a tuple with 3 elements, which are the
        left part of the subclipped video, the center part and the
        right part as SubClip instances. If no left or right part,
        they are return as None. So, the possibilities are (from
        left to right):

        - SubClip, SubClip, SubClip
        - SubClip, SubClip, None
        - None, SubClip, SubClip
        - None, SubClip, SubClip
        """
        video = VideoParser.to_moviepy(video)

        # We use a flag to indicate the end of the clip so
        # we replace it by its actual duration
        end_time = video.duration if end_time == END_OF_CLIP else end_time

        left_clip, center_clip, right_clip = subclip_video(video, start_time, end_time)

        return (
            SubClip(left_clip) if left_clip is not None else None,
            SubClip(center_clip),
            SubClip(right_clip) if right_clip is not None else None
        )

    def __init__(
        self,
        video: Clip
    ):
        """
        I recommend you to use the static '.init()'method 
        instead of this because you are able to keep the 
        remaining part of the clip if you subclip them.

        The SubClip instantiating method has to be called only
        in the static 'init' method of this class so we are able
        to handle the rest of the clips (if existing) according
        to the subclipping process we do. If you use this method
        and then subclip
        """
        self.video = VideoParser.to_moviepy(video)
        
        self._speed_factor = 1
        self._volume = 1
        self._zoom = 1
        self._x_movement = 0
        self._y_movement = 0
        self._rotation = 0
        # TODO: This was being calculated by VideoHandler
        # to ensure the number of frames was ok
        self._resized = [(1, 1) for _ in range(self.number_of_frames)]
        self._rotated = [0 for _ in range(self.number_of_frames)]
        # TODO: Use constants
        self._with_position = [(DEFAULT_SCENE_SIZE[0] / 2, DEFAULT_SCENE_SIZE[1] / 2) for _ in range(self.number_of_frames)]
        self._effects = []

    @property
    def video_processed(
        self
    ):
        """
        The video once it's been processed with all the
        attributes that are set in this instance.
        """
        if not self._video_processed:
            self._video_processed = self._process()

        return self._video_processed

    @property
    def duration(
        self
    ):
        """
        Shortcut to the actual duration of the video once
        it's been processed.
        """
        # TODO: Maybe this has to be the pre-processed
        #return self.video_processed.duration
        return self.video.duration
    
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
    def size(
        self
    ):
        """
        Shortcut to the actual size of the video once
        it's been processed.
        """
        return self.video_processed.size
    
    @property
    def width(
        self
    ):
        """
        Shortcut to the actual width of the processed
        video.
        """
        return self.size[0]
    
    @property
    def height(
        self
    ):
        """
        Shortcut to the actual height of the processed
        video.
        """
        return self.size[1]
    
    @property
    def fps(
        self
    ):
        """
        Fps of the original video (the pre-processed one).
        """
        return self.video.fps
    
    @property
    def number_of_frames(
        self
    ):
        """
        Number of frames of the original video (the 
        pre-processed one).

        Due to a bug with the moviepy reading way, this
        number cannot be the real number. Check the 
        MPVideo class that looks for the exact number.
        """
        # TODO: Maybe use MPVideo to ensure the video
        # has the real number of frames, and also 
        # subclip the video to the real duration based
        # on this. I have a method that does it by 
        # trying to get the last frames and catching
        # the warnings
        return int(self.duration * self.fps + SMALL_AMOUNT_TO_FIX)
    
    @property
    def number_of_audio_frames(
        self
    ):
        """
        Number of frames of the original audio (the
        pre-processed one).
        """
        return int(self.video.audio.duration * self.video.audio.fps + SMALL_AMOUNT_TO_FIX)
    
    @property
    def volume(
        self
    ):
        return self._volume
    
    @volume.setter
    def volume(
        self,
        value: SubClipAttributeModifier
    ):
        """
        Set the video audio volume values by providing
        a SubClipAtrributeModifier that will set those
        values for this SubClip instance.

        TODO: Say the limit values and explain more.
        """
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'volume', VOLUME_LIMIT, self.number_of_frames)

        # Values from 0 to 100 are for humans, but this
        # is a factor so we normalize it
        self._volume = value.modifier / 100 if value.is_single_value else [value / 100 for value in value.get_values(self.number_of_frames)]

    @property
    def color_temperature(
        self
    ):
        return self._color_temperature
    
    @color_temperature.setter
    def color_temperature(
        self,
        value: SubClipAttributeModifier
    ):
        """
        Set the color temperature values by providing a 
        SubClipAttributeModifier that will set the values
        for the current SubClip.
        """
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'color_temperature', COLOR_TEMPERATURE_LIMIT, self.number_of_frames)

        self._color_temperature = value.get_values(self.number_of_frames)

    @property
    def brightness(
        self
    ):
        return self._brightness
    
    @brightness.setter
    def brightness(
        self,
        value: SubClipAttributeModifier
    ):
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'brightness', BRIGHTNESS_LIMIT, self.number_of_frames)

        self._brightness = value.get_values(self.number_of_frames)

    @property
    def contrast(
        self
    ):
        return self._contrast
    
    @contrast.setter
    def contrast(
        self,
        value: SubClipAttributeModifier
    ):
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'contrast', CONTRAST_LIMIT, self.number_of_frames)

        self._contrast = value.get_values(self.number_of_frames)

    @property
    def sharpness(
        self
    ):
        return self._sharpness

    @sharpness.setter
    def sharpness(
        self,
        value: SubClipAttributeModifier
    ):
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'sharpness', SHARPNESS_LIMIT, self.number_of_frames)

        self._sharpness = value.get_values(self.number_of_frames)

    @property
    def white_balance(
        self
    ):
        return self._white_balance
    
    @white_balance.setter
    def white_balance(
        self,
        value: SubClipAttributeModifier
    ):
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'white_balance', WHITE_BALANCE_LIMIT, self.number_of_frames)

        self._white_balance = value.get_values(self.number_of_frames)

    @property
    def speed_factor(
        self
    ):
        return self._speed_factor
    
    @speed_factor.setter
    def speed_factor(
        self,
        value: SubClipAttributeModifier
    ):
        _validate_is_video_attribute_modifier_instance(value)
        _validate_attribute_modifier(value, 'speed_factor', SPEED_FACTOR_LIMIT, self.number_of_frames)

        self._speed_factor = value.modifier if value.is_single_value else value.get_values(self.number_of_frames) 

    @property
    def zoom(
        self
    ):
        return self._zoom
    
    @zoom.setter
    @unset_video_processed
    def zoom(
        self,
        value: int
    ):
        """
        The zoom must be an integer number between [1, 500]. A
        zoom value of 100 means no zoom.
        
        - Zoom=100 means no zoom
        - Zoom=50 means zoom out until the clip size is the half.
        - Zoom=200 means zoom in until the clip size is the doubel
        """
        _validate_zoom(value)

        self._zoom = value / 100

    @property
    def x_movement(
        self
    ):
        return self._x_movement
    
    @x_movement.setter
    def x_movement(
        self,
        value: int
    ):
        """
        The movement in X axis must be a value between
        [-1920*4, 1920*4]. A positive number means moving
        the clip to the right side.
        """
        _validate_x_movement(value)
        
        self._x_movement = int(value)

    @property
    def y_movement(
        self
    ):
        return self._y_movement
    
    @y_movement.setter
    def y_movement(
        self,
        value: int
    ):
        """
        The movement in Y axis must be a value between
        [-1920*4, 1920*4]. A positive number means moving
        the clip to the bottom.
        """
        _validate_y_movement(value)
        
        self._y_movement = int(value)

    @property
    def rotation(
        self
    ):
        return self._rotation
    
    @rotation.setter
    def rotation(
        self,
        value: int
    ):
        """
        Rotation must be an integer value between -360
        and 360. A positive number means rotating the
        clip clockwise.
        """
        _validate_rotation(value)
        
        self._rotation = int(value)

    @property
    def effects(
        self
    ):
        return self._effects

    # Easy setters below, that are another way of setting
    # attributes values but just passing arguments. This
    # is interesting if you just need to apply a simple
    # and single value or an easy range
    def set_volume(
        self,
        start: float,
        end: Union[float, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new volume for the video that will be modified frame by
        frame.

        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('volume', start, end, rate_function)

    def set_color_temperature(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new color temperature that will be modified frame by frame.

        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('color_temperature', start, end, rate_function)

    def set_brightness(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new brightness that will be modified frame by frame.
        
        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('brightness', start, end, rate_function)

    def set_contrast(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new contrast that will be modified frame by frame.
        
        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('contrast', start, end, rate_function)

    def set_sharpness(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new sharpness that will be modified frame by frame.
        
        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('sharpness', start, end, rate_function)

    def set_white_balance(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new white balance that will be modified frame by frame.
        
        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('white_balance', start, end, rate_function)

    def set_speed_factor(
        self,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Set a new speed factor that will be modifier frame by frame.

        If only 'start' is provided, the change will be the same in all
        frames, but if a different 'end' value is provided, the also given
        'rate_function' will be used to calculate the values in between
        those 'start' and 'end' limits to be applied in the corresponding
        frames.
        """
        self._set_attribute('speed_factor', start, end, rate_function)

    def _set_attribute(
        self,
        attribute: str,
        start: int,
        end: Union[int, None] = None,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        setattr(
            self,
            attribute,
            SubClipAttributeModifier(
                SubClipSetting(
                    start,
                    start if end is None else end,
                    rate_function
                )
            )
        )

    # Other easy setters
    def set_zoom(
        self,
        value: int
    ):
        """
        Set a new zoom value.
        """
        self.zoom = value

    def set_x_movement(
        self,
        value: int
    ):
        """
        Set a new x movement value.
        """
        self.x_movement = value

    def set_y_movement(
        self,
        value: int
    ):
        """
        Set a new y movement value.
        """
        self.y_movement = value

    def set_rotation(
        self,
        value: int
    ):
        """
        Set a new rotation value.
        """
        self.rotation = value

    def add_effect(
        self,
        effect: 'SEffect'
    ):
        """
        Add the provided 'effect' instance to be applied on the clip.
        """
        if not PythonValidator.is_an_instance(effect) or not PythonValidator.is_subclass(effect, 'SEffect'):
            raise Exception('The provided "effect" parameter is not an instance of a SEffect subclass.')
        
        # TODO: Check that effect is valid (times are valid, there is
        # not another effect that makes it incompatible, etc.)
        # We force the correct 'number_of_frames' attribute
        effect.number_of_frames = self.number_of_frames

        self._effects.append(effect)

    def subclip(
        self,
        start: float,
        end: float
    ):
        """
        This method will split the current SubClip instance
        into 3 different items, that will be new instances
        of SubClip class according to the 'start' and 'end'
        times provided.

        This method uses a copy of the current instance to
        not modify it but returning completely new (by
        using deepcopy). All settings and effects will be
        preserved as they were in the original instance for
        all of the new copies.

        This method will return 3 values: left part of the
        SubClip, center part and right part. Left and right
        part can be None.
        """
        ParameterValidator.validate_mandatory_positive_number('start', start, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('end', end, do_include_zero = True)
        
        if start >= end:
            raise Exception('The "start" parameter provided is greater or equal than the "end" parameter provided.')
        
        if end > self.duration:
            raise Exception(f'The "end" provided ({end}s) is longer than the current video duration ({self.duration}s).')

        # TODO: I need to calculate the frame index in which I'm
        # splitting the subclip to also subclip the arrays that
        # are inside the instance
        left = self.copy() if start not in (None, 0) else None
        center = self.copy()
        right = self.copy() if end is not None and end < self.duration else None

        def replace_attribute_values(instance: SubClip, start_index: Union[float, None], end_index: Union[float, None]):
            """
            Replaces the attribute values of the given 'instance' 
            considering the left, center and right videos that will
            be returned as result so each video can keep only their
            values.
            """
            def split_array(array: list, start_index: Union[float, None], end_index: Union[float, None]):
                # TODO: Validate 'start_index' and 'end_index' according
                # to 'array' size
                if start_index is not None and end_index is not None: return array[start_index:end_index]
                if start_index is not None: return array[start_index:]
                if end_index is not None: return array[:end_index]
                return array

            # TODO: Append here any new array of values per frame
            instance._color_temperature = split_array(instance._color_temperature, start_index, end_index) if instance._color_temperature is not None else None
            instance._brightness = split_array(instance._brightness, start_index, end_index) if instance._brightness is not None else None
            instance._contrast = split_array(instance._contrast, start_index, end_index) if instance._contrast is not None else None
            instance._sharpness = split_array(instance._sharpness, start_index, end_index) if instance._sharpness is not None else None
            instance._white_balance = split_array(instance._white_balance, start_index, end_index) if instance._white_balance is not None else None
            # TODO: '_speed_factor' is special and can be both a single
            # value or a list (or a None if no changes to apply)
            if PythonValidator.is_list(instance._speed_factor):
                instance._speed_factor = split_array(instance._speed_factor, start_index, end_index)
            
            return instance

        last_index = 0
        # Left
        if left is not None:
            left.video = left.video.with_subclip(0, start)
            last_index = left.number_of_frames
            # Modify all the attributes per frame values
            left = replace_attribute_values(left, 0, last_index)

        # Center
        center.video = center.video.with_subclip(start, end)
        # Modify all the attributes per frame values
        center = replace_attribute_values(center, last_index, last_index + center.number_of_frames)
        last_index = last_index + center.number_of_frames

        # Right
        if right is not None:
            right.video = right.video.with_subclip(start_time = end)
            # Modify all the attributes per frame values
            right = replace_attribute_values(right, last_index, None)

        return left, center, right
    
    def write_videofile(self, output_filename: str):
        """
        Writes the video once it is processed to the provided
        'output_filename'.
        """
        # TODO: Validate 'output_filename'

        self.video_processed.write_videofile(output_filename)

    def copy(self):
        # TODO: Complete this method to manually copy the instance
        # because 'deepcopy' is not working properly
        copy = SubClip(self.video.copy())

        # The only thing we need to preserve is the values that
        # modify each attribute. The modifier instance is only
        # passed to generate these values, so that generator is
        # only necessary once to generate those values
        copy._color_temperature = self._color_temperature.copy() if self._color_temperature is not None else None
        copy._brightness = self._brightness.copy() if self._brightness is not None else None
        copy._contrast = self._contrast.copy() if self._contrast is not None else None
        copy._sharpness = self._sharpness.copy() if self._sharpness is not None else None
        copy._white_balance = self._white_balance.copy() if self._white_balance is not None else None
        copy._speed_factor = self._speed_factor.copy() if self._speed_factor is not None else None

        copy._zoom = self._zoom if self._zoom is not None else None
        copy._x_movement = self._x_movement if self._x_movement is not None else None
        copy._y_movement = self._y_movement if self._y_movement is not None else None
        copy._rotation = self._rotation if self._rotation is not None else None

        # TODO: Maybe I need to apply the basic values here (?)
        copy._resized = self._resized.copy() if self._resized is not None else None
        copy._rotated = self._rotated.copy() if self._rotated is not None else None
        copy._with_position = self._with_position.copy() if self._with_position is not None else None

        return copy
    
    def _process(self):
        """
        Process the video clip with the attributes set and 
        obtain a copy of the original video clip with those
        attributes and effects applied on it. This method
        uses a black (but transparent) background with the
        same video size to make sure everything works 
        properly.

        This method doesn't change the original clip, it
        applies the changes on a copy of the original one
        and returns that copy modified.
        """
        video = self.video.copy()

        # Process video frames one by one
        def modify_video_frame_by_frame(get_frame, t):
            """
            Modificate anything related to frame image: pixel
            colors, distortion, etc.
            """
            frame = get_frame(t)
            frame_index = VideoFrameTHelper.get_frame_index_from_frame_t(t, video.fps)

            frame = ImageEditor.modify_color_temperature(frame, self._color_temperature[frame_index]) if self._color_temperature is not None else frame
            frame = ImageEditor.modify_brightness(frame, self._brightness[frame_index]) if self._brightness is not None else frame
            frame = ImageEditor.modify_contrast(frame, self._contrast[frame_index]) if self._contrast is not None else frame
            frame = ImageEditor.modify_sharpness(frame, self._sharpness[frame_index]) if self._sharpness is not None else frame
            frame = ImageEditor.modify_white_balance(frame, self._white_balance[frame_index]) if self._white_balance is not None else frame

            return frame
        
        # Apply frame by frame video modifications
        video = video.transform(lambda get_frame, t: modify_video_frame_by_frame(get_frame, t))

        # Process audio frames one by one
        def modify_audio_frame_by_frame(get_frame, t):
            # The 't' time moment is here a numpy array
            # of a lot of consecutive time moments (maybe
            # 1960). That ishow it works internally
            frame = get_frame(t)
            frame_index = VideoFrameTHelper.get_video_frame_index_from_video_audio_frame_t(t[500], video.fps, video.audio.fps)

            # Volume value 1 means no change
            if self._volume is not None and self._volume != 1:
                frame = AudioFrameEditor.modify_volume(
                    frame,
                    self._volume if PythonValidator.is_number(self._volume) else self._volume[frame_index]
                )
                # TODO: The result with this below is the same
                #frame *= self._volume if PythonValidator.is_number(self._volume) else self._volume[frame_index]

            return frame
        
        if video.audio is not None:
            audio = video.audio.copy()
            audio = audio.transform(lambda get_frame, t: modify_audio_frame_by_frame(get_frame, t))
            video = video.with_audio(audio)

        # Edit speed with speed factors (carefully)
        if PythonValidator.is_number(self.speed_factor) and self.speed_factor != 1:
            from yta_multimedia.video.edition.effect.fit_duration_effect import FitDurationEffect
            video = FitDurationEffect().apply(video, self.duration / self.speed_factor)
        elif PythonValidator.is_list(self.speed_factor):
            # TODO: 'resizes', 'positions' and 'rotations' must be
            # refactored also according to the new fps
            video = self._apply_speed_factor(video)

        # The '_apply_speed_factor' updates these arrays
        resizes = self._resized.copy()
        positions = self._with_position.copy()
        rotations = self._rotated.copy()

        # Modifications below affect to other important
        # attributes.
        # TODO: I don't know if I will accept these
        # modifications below in any case or if I will
        # block them if there are some effects or things
        # that can make conflicts or malfunctioning. If
        # I have a very specific effect, changing these
        # important attributes (resizes, positions and
        # rotations) could be a big headache.
        if self.zoom is not None and self.zoom != 1:
            resizes = [(resize[0] * self.zoom, resize[1] * self.zoom) for resize in resizes]
        if self.x_movement is not None and self.x_movement != 0:
            positions = [(position[0] + self.x_movement, position[1]) for position in positions]
        if self.y_movement is not None and self.y_movement != 0:
            positions = [(position[0], position[1] + self.y_movement) for position in positions]
        if self.rotation is not None and self.rotation != 0:
            rotations = [rotation + self.rotation for rotation in rotations]

        # TODO: Should we apply effects here after the
        # general basic attributes modifications and after
        # speed factor is applied, or before? That's a 
        # a good question that only testing can answer
        if len(self.effects) > 0:
            self._apply_effects()

        """
        The rotation process makes a redimension of the
        frame image setting the pixels out of the rotation
        as alpha to actually build this effect. Thats why
        we need to know the new frame size to be able to
        position it correctly in the position we want
        """
        # Apply the video rotation, frame by frame
        video = video.rotated(lambda t: rotations[VideoFrameTHelper.get_frame_index_from_frame_t(t, video.fps)], expand = True)

        # As the rotation changes the frame size, we need
        # to recalculate the resize factors
        # TODO: Move this method to a helper or something
        def get_rotated_image_size(size: tuple[int, int], angle: int):
            """
            Get the size of an image of the given 'size' when it
            is rotated the also given 'angle'.

            This method is based on the moviepy Rotate effect to
            pre-calculate the frame rotation new size so we are
            able to apply that resize factor to the other 
            attributes.

            This method returns the new size and also the width
            size change factor and the height size change factor.
            """
            from PIL import Image

            new_size = Image.new('RGB', size, (0, 0, 0)).rotate(
                angle,
                expand = True,
                resample = Image.Resampling.BILINEAR
            ).size

            width_factor = new_size[0] / size[0]
            height_factor = new_size[1] / size[1]

            return new_size, width_factor, height_factor
        
        for index, resize in enumerate(resizes):
            current_rotation = rotations[index]
            if current_rotation != 0:
                # Recalculate the resize according to the resize
                # factor that took place when rotating the image
                _, width_factor, height_factor = get_rotated_image_size(
                    (
                        int(self.original_width * resize[0]),
                        int(self.original_height * resize[1])
                    ),
                    current_rotation
                )
                
                resizes[index] = (
                    resize[0] * width_factor,
                    resize[1] * height_factor
                )

        """
        The video 'resized' method doesn't accept double
        factors so I have to manually calculate the new
        size according to the video size and pass that
        exact new size to be actually resized as I need.
        """
        # Resize the video dynamically frame by frame
        def resized(t):
            """
            Resizes the video by applying the resize factors to
            the original size and returns the new size to be
            applied.
            """
            current_frame_index = VideoFrameTHelper.get_frame_index_from_frame_t(t, video.fps)

            return (
                resizes[current_frame_index][0] * self.original_width,
                resizes[current_frame_index][1] * self.original_height
            )

        video = video.resized(lambda t: resized(t))

        """
        The position is very special because it depends on
        the size of each frame, that can change dynamically
        because of resizes, rotations, etc. The 'positions'
        array is pointing the center coordinate of the 
        position, so we need to recalculate the upper left
        corner according to that position.
        """

        def with_position(t):
            # This is very slow but I know the exact frame
            # size so I'm sure the positioning will be ok
            #frame = video.get_frame(t)
            #frame_size = frame.shape[1], frame.shape[0]
            current_frame_index = VideoFrameTHelper.get_frame_index_from_frame_t(t, video.fps)
            
            # Adjust position to its upper left corner
            upper_left_corner_position = [
                positions[current_frame_index][0] - self.width * resizes[current_frame_index][0] / 2,
                positions[current_frame_index][1] - self.height * resizes[current_frame_index][1] / 2
            ]

            return upper_left_corner_position[0], upper_left_corner_position[1]
        
        video = video.with_position(lambda t: with_position(t))

        # TODO: This below is repeated in VideoEditor class as
        # '._overlay_video()'
        return CompositeVideoClip([
            ClipGenerator.get_default_background_video(duration = video.duration, fps = video.fps),
            video
        ])#.with_audio(VideoAudioCombinator(audio_mode).process_audio(background_video, video))

    def _apply_speed_factor(self, video):
        """
        Apply the speed factors to the video. This method 
        will use the 'time_transform' method and also will
        set a new duration with the 'with_duration' method.

        This method returns the new video modified.
        """
        if PythonValidator.is_number(self.speed_factor) or self.speed_factor is None:
            raise Exception(f'The "speed_factor" parameter is not valid for this method. It must be an array of {self.number_of_frames} elements.')
        
        def _get_frame_ts_applying_speed_factors(self: SubClip):
            """
            Returns a tuple with the video and audio arrays
            affected by the speed factors.
            """
            if self.number_of_frames != len(self.speed_factor):
                raise Exception(f'The number of video frames {self.number_of_frames} and speed factors array {len(self.speed_factor)} must be the same.')

            # We only work with speed factors for video frames
            # as we know what is the audio associated to each
            # frame and can modify it according to it
            final_video_frame_ts = []
            final_audio_frame_ts = []
            # TODO: I need to have any array that has to be
            # recalculated according to the repeated or the
            # skipped indexes
            positions = []
            resizes = []
            rotations = []

            rest = 0
            current_frame_index = 0
            while current_frame_index < self.number_of_frames:
                current_speed_factor = self.speed_factor[current_frame_index]
                current_video_frame_t = VideoFrameTHelper.get_frame_t_from_frame_index(current_frame_index, self.video.fps)

                # We know current video frame 't', so we can obtain
                # the associated audio frame tts
                current_audio_frame_ts = VideoFrameTHelper.get_video_audio_tts_from_video_frame_t(current_video_frame_t, self.video.fps, self.video.audio.fps)

                if current_speed_factor < 1:
                    # If needed, repeat frames to slow down
                    times_to_append = 1
                    current_rest = (1 / current_speed_factor) - 1
                    rest -= current_rest

                    if rest <= -1:
                        times_to_append += int(abs(rest))
                        rest += int(abs(rest))
                    
                    final_video_frame_ts.extend([current_video_frame_t] * times_to_append)
                    """
                    We have two different ways of handling the audio
                    duplication.
                    
                    - One is duplicating block by block, so:
                    from [1, 2] to [1, 2, 1, 2, 1, 2]

                    - The other one duplicates value by value, so:
                    from [1, 2] to [1, 1, 1, 2, 2, 2]

                    TODO: What about from [1, 2] to [1, 1.33, 1.66,
                    2] (?)
                    """
                    # Block by block
                    #final_audio_frame_ts.extend([current_audio_frame_ts] * times_to_append)
                    # Value by value
                    final_audio_frame_ts.extend([
                        caft
                        for caft in current_audio_frame_ts
                        for _ in range(times_to_append)
                    ])

                    # Any other array that also has to be recalculated
                    resizes.extend([self._resized[current_frame_index]] * times_to_append)
                    positions.extend([self._with_position[current_frame_index]] * times_to_append)
                    rotations.extend([self._rotated[current_frame_index]] * times_to_append)

                else:
                    # Extend the video and the audio just once
                    final_video_frame_ts.append(current_video_frame_t)
                    final_audio_frame_ts.extend(current_audio_frame_ts)

                    # Any other array that also has to be recalculated
                    resizes.append(self._resized[current_frame_index])
                    positions.append(self._with_position[current_frame_index])
                    rotations.append(self._rotated[current_frame_index])

                    if current_speed_factor > 1:
                        # If needed, we skip frames to speed it up
                        current_rest = current_speed_factor - 1
                        rest += current_rest

                        if rest >= 1:
                            current_frame_index += int(rest)
                            rest -= int(rest)

                current_frame_index += 1

            return final_video_frame_ts, final_audio_frame_ts, resizes, positions, rotations

        final_video_frame_ts, final_audio_frame_ts, resizes, positions, rotations = _get_frame_ts_applying_speed_factors(self)

        # TODO: Remove this
        print(f'Total of {len(final_video_frame_ts)} ({len(final_video_frame_ts) / self.video.fps}) video frame ts and {len(final_audio_frame_ts)} ({len(final_audio_frame_ts) / self.video.audio.fps}) audio frame ts.')

        def transform_t_with_both_frames(t, video_fps: float, audio_fps: float):
            """
            Transform the time moment 't' we are processing
            to render in the new file according to the time
            moments of the original video/audio. We have
            pre-calculated them so we know what frame of the
            original video/audio has to be placed for each
            rendering time moment 't' we handle here.
            """
            if not PythonValidator.is_numpy_array(t):
                # Video frame. The 't' is just a time moment
                return final_video_frame_ts[
                    VideoFrameTHelper.get_frame_index_from_frame_t(t, video_fps)
                ]
            else:
                # Audio frame. The 't' is an array of time
                # moments. The amount of 't' is unespecific.
                # I think it's just a chunk. Mine was 1960
                t_indexes = [
                    VideoFrameTHelper.get_frame_index_from_frame_t(t_, audio_fps)
                    for t_ in t
                ]

                # I have to return an array that replaces
                # the original tts
                return np.array([final_audio_frame_ts[t_index] for t_index in t_indexes])

        # TODO: What if video has no audio (?)
        video = video.time_transform(
            lambda t: transform_t_with_both_frames(t, self.video.fps, self.video.audio.fps), apply_to = ['mask', 'audio']
        )
        video = video.with_duration(len(final_video_frame_ts) * 1 / video.fps)

        # TODO: I don't want this to be done here, please
        # return it and do in another place in this class
        self._resized = resizes
        # TODO: Positions must be the center of the 
        # position we want, and then calculate the upper
        # left corner when actually positioning it
        self._with_position = positions
        self._rotated = rotations

        return video

    def _apply_effects(self):
        """
        Apply the effects.
        """
        if len(self._effects) > 0:
            # TODO: Apply effects
            for effect in self._effects:
                if effect.do_affect_frames:
                    frames = effect.values[0]
                    # TODO: Handle 'frames' array, by now I'm just
                    # replacing the values
                    # TODO: Add or replace (?)
                    pass

                if effect.do_affect_with_position:
                    with_position = effect.values[1]
                    # TODO: Handle 'with_position' array, by now I'm just
                    # replacing the values
                    self._with_position = with_position
                    # TODO: Add or replace (?)

                if effect.do_affect_resized:
                    resized = effect.values[2]
                    # TODO: Handle 'resized' array, by now I'm just
                    # replacing the values
                    self._resized = resized
                    # TODO: Multiply or replace (?)

                if effect.do_affect_rotated:
                    rotated = effect.values[3]
                    # TODO: Handle 'rotated' array, by now I'm just
                    # replacing the values
                    self._rotated = rotated
                    # TODO: Add or replace (?)
    

class SubClipOnTimelineLayer:
    """
    Class to represent one of our SubClips but in
    the general project timeline and in a specific
    layer of it, with the start and end moment in
    that timeline, and also the layer in which it
    is placed.

    TODO: This is a concept in test phase. SubClip
    is a more definitive concept.
    """
    subclip: SubClip = None
    start_time: float = None
    """
    The start time on the general project timeline. Do 
    not confuse this term with the start time of a
    moviepy clip.
    """

    @property
    def video_processed(self):
        return self.subclip.video_processed

    @property
    def duration(self):
        """
        Shortcut to the actual duration of the video once
        it's been processed.
        """
        return self.subclip.duration
    
    @property
    def size(self):
        """
        Shortcut to the actual size of the video once it's
        been processed.
        """
        return self.subclip.size
    
    @property
    def width(self):
        """
        Shortcut to the actual weight of the video once
        it's been processed.
        """
        return self.size[0]
    
    @property
    def height(self):
        """
        Shortcut to the actual height of the video once
        it's been processed.
        """
        return self.size[1]
    
    @property
    def end_time(self):
        """
        The end moment on the timeline, based on this
        instance 'start_time' and the real video 'duration'.
        """
        return self.start_time + self.duration

    def __init__(self, subclip: SubClip, start_time: float):
        if not PythonValidator.is_instance(subclip, SubClip):
            raise Exception('The provided "subclip" parameter is not a valid SubClip instance.')
        
        if not NumberValidator.is_number_between(start_time, 0, END_OF_TIMELINE):
            raise Exception(f'The provided "start_time" parameter is not a valid number between in the range (0, {END_OF_TIMELINE})')
        
        self.subclip = subclip
        self.start_time = start_time

    # def _process(self):
    #     return self.subclip._process()

class TimelineLayerType(Enum):
    """
    The type of a timeline layer, which will determine
    which kind of SubClips are accepted by the layer
    with this type.
    """
    VIDEO = 'video'
    """
    The type of layer that only accept video SubClips.
    """
    AUDIO = 'audio'
    """
    The type of layer that only accept audio SubClips.
    """
    # TODO: Probably add 'GreenscreenLayer',
    # 'AlphascreenLayer', 'TextLayer', 'SubtitleLayer',
    # and all needed in a future when this concept 
    # evolves properly

class TimelineLayer:
    index: int = None
    type: TimelineLayerType = None
    _subclips: list[SubClipOnTimelineLayer] = None

    @property
    def subclips(self):
        """
        The list of subclips in this timeline layer, ordered
        according to its 'start_time' from first to be displayed
        to last ones.
        """
        return sorted(self._subclips, key = lambda subclip: subclip.start_time)
    
    @property
    def duration(self):
        """
        The duration of this timeline layer, which is the
        'end_time' of the last displayed subclip, or 0 if no
        clips.
        """
        return self.subclips[-1].end_time if self.subclips else 0
    
    @property
    def all_clips(self):
        """
        The list of all clips needed to fulfill the timeline
        layer completely. This involves the actual subclips
        but also the needed black background clips to put in
        the gaps between the subclips.
        """
        all_subclips = []
        current_time_moment = 0
        # TODO: This 'timeline_duration' must be calculated
        # according to all timeline layers, so the longest
        # one is the one we need to assign here
        timeline_duration = self.subclips[-1].end_time

        for subclip in self.subclips:
            # We fulfill the gap if existing
            if subclip.start_time > current_time_moment:
                all_subclips.append(ClipGenerator.get_default_background_video(size = subclip.size, duration = subclip.start_time - current_time_moment, fps = subclip.fps))
            
            # We add the existing subclip
            all_subclips.append(subclip.video_processed)
            
            current_time_moment = subclip.end_time
        
        # Check if gap at the end due to other longer layers
        if current_time_moment < timeline_duration:
            # TODO: Maybe we need to do something with the fps
            all_subclips.append(ClipGenerator.get_default_background_video(size = subclip.size, duration = timeline_duration - current_time_moment, fps = self.subclips[0].fps))
        
        return all_subclips

    def __init__(self, index: int = 0, type: TimelineLayerType = TimelineLayerType.VIDEO):
        _validate_layer_index(index)
        type = TimelineLayerType.to_enum(type) if type is not None else TimelineLayerType.VIDEO

        self.index = index
        self.type = type
        self._subclips = []

    def add_subclip(self, subclip: SubClip, start_time: float):
        """
        Append the provided 'subclip' at the end of the list.

        TODO: Being in the end of the list doesn't mean being
        the last one displayed. By now I'm storing them just
        one after another and ordering them when trying to get
        them as a property. This will change in a near future
        to be more eficient.
        """
        if not PythonValidator.is_instance(subclip, SubClip):
            raise Exception('The provided "subclip" parameter is not a valid instance of the SubClip class.')
        
        if not NumberValidator.is_number_between(start_time, 0, MAX_TIMELINE_LAYER_DURATION):
            raise Exception('The provided "start_time" is not a valid value')

        # 
        # TODO: Check that the 'start_time' or the 'duration'
        # doesn't collide with another existing subclip. If
        # yes, choose what strategy to follow
        if any(subclip.start_time <= start_time <= subclip.end_time for subclip in self.subclips):
            raise Exception(f'There is one existing subclip at the {str(start_time)} time position.')

        self._subclips.append(SubClipOnTimelineLayer(subclip, start_time))

    def remove_subclip(self, index: int):
        """
        Delete the subclip in the provided 'index' position of
        the list (if existing), or raises an Exception if it
        doesn't exist or the list is empty.
        """
        # TODO: Maybe remove by passing the instance (?)
        if PythonValidator.is_empty_list(self._subclips):
            # TODO: Maybe I should not raise an Exception here...
            raise Exception('No subclips to remove.')
        
        if not NumberValidator.is_number_between(0, len(self._subclips)):
            raise Exception(f'The provided "index" is not a valid index (must be between [0, {str(len(self._subclips))}).')

        # TODO: Be very careful, I have a 'subclips' property which
        # returns the subclips ordered, but the raw '_subclips'
        # property is not ordered, so here the 'index' is potentially
        # wrong. Think how to handle this in a near future, please.
        del self._subclips[index]

    def build(self):
        """
        Concatenate all the timeline layer subclips (fulfilling the
        gaps with black transparent background clips) and return the
        concatenated clip.
        """
        # TODO: What if I have one non-transparent and transparent
        # clips in this timeline layer? They will be treated in a
        # similar way so it is not the expected behaviour...
        return concatenate_videoclips(self.all_clips)
    
class VideoProject:
    """
    Class representing a whole but single video project
    in which we have a timeline with different layers
    and clips on them.
    """
    timeline_layers: list[TimelineLayer] = None
    screen_size: tuple[int, int] = None
    """
    Dimensions of the final video that has to be
    exported.
    """

    def __init__(self, screen_size: tuple[int, int] = (DEFAULT_SCENE_SIZE[0], DEFAULT_SCENE_SIZE[1])):
        self.timeline_layers = [
            TimelineLayer(0, TimelineLayerType.VIDEO),
            # TODO: I Simplify everything by now and I only
            # handle one video layer
            #TimelineLayer(0, TimelineLayerType.AUDIO)
        ]
        # TODO: Validate 'screen_size'
        self.screen_size = screen_size

    def get_layers(
        self,
        type: TimelineLayerType
    ) -> list[TimelineLayer]:
        """
        Get the timeline layers of the provided 'type' sorted by
        index in ascending order.
        """
        type = TimelineLayerType.to_enum(type)

        return sorted(
            [
                layer
                for layer in self.timeline_layers
                if layer.type == type
            ], 
            key = lambda layer: layer.index
        )
    
    def get_last_layer_index(
        self,
        type: TimelineLayerType
    ) -> Union[int, None]:
        """
        Get the last index used for the layers of the given
        'type', that will be None if no layers of that type.
        """
        type = TimelineLayerType.to_enum(type)

        layers = self.get_layers(type)

        return (
            layers[-1:].index
            if not PythonValidator.is_empty_list(layers) else
            None
        )

    def add_layer(
        self,
        type: TimelineLayerType = TimelineLayerType.VIDEO
    ) -> int:
        """
        Add a new layer of the provided 'type' and returns
        the index in which it has been placed.
        """
        type = (
            TimelineLayerType.to_enum(type)
            if type is not None else
            TimelineLayerType.VIDEO
        )

        layers = self.get_layers(type)
        index = (
            len(layers) + 1
            if layers else
            0
        )

        self.timeline_layers.append(TimelineLayer(index, type))

        return index
    
    def remove_layer(
        self,
        layer: TimelineLayer
    ):
        ParameterValidator.validate_mandatory_instance_of('layer', layer, TimelineLayer)
        
        if layer not in self.timeline_layers:
            raise Exception('The provided "layer" does not exist in this project.')

        self.timeline_layers.remove(layer)

    def build(
        self
    ):
        # TODO: Omg, cyclic import issue here again...
        from yta_multimedia.video.edition.duration import set_video_duration, ExtendVideoMode
        # TODO: Remove this code below when this is done 
        # individually by each layer. By now I'm forcing
        # all layers clips to have the same duration as
        # the longest layer clip has, but must be done
        # using a general and common 'max_duration'
        # property that is not calculated here.
        layers_clips = [
            layer.build()
            for layer in self.timeline_layers
        ]
        max_duration = max(
            layer_clip.duration
            for layer_clip in layers_clips
        )
        layers_clips = [
            set_video_duration(layer_clip, max_duration, extend_mode = ExtendVideoMode.BLACK_TRANSPARENT_BACKGROUND)
            for layer_clip in layers_clips
        ]

        return CompositeVideoClip(layers_clips)





def subclip_video(
    video: Clip,
    start_time: float,
    end_time: float
) -> tuple[Union[Clip, None], Clip, Union[Clip, None]]:
    """
    Subclip the provided 'video' into 3 different subclips,
    according to the provided 'start_time' and 'end_time',
    and return them as a tuple of those 3 clips. First and
    third clip could be None.

    The first clip will be None when 'start_time' is 0, and 
    the third one when the 'end_time' is equal to the given
    'video' duration.
    """
    video = VideoParser.to_moviepy(video)

    left = (
        None
        if (
            start_time == 0 or
            start_time == None
        ) else
        video.with_subclip(0, start_time)
    )
    center = video.with_subclip(start_time, end_time)
    right = (
        None
        if (
            end_time is None or
            end_time >= video.duration
        ) else
        video.with_subclip(start_time = end_time)
    )

    return left, center, right



# TODO: This must be maybe moved to another file
# because it is mixed with the 'subclip_video'
# method...
def _validate_layer_index(layer_index: int):
    if not NumberValidator.is_number_between(layer_index, LAYERS_INDEXES_LIMIT[0], LAYERS_INDEXES_LIMIT[1]):
        raise Exception(f'The provided "layer_index" is not a valid layer, it must be an int value between [{LAYERS_INDEXES_LIMIT[0]}, {LAYERS_INDEXES_LIMIT[1]}].')
    
def _validate_is_video_attribute_modifier_instance(element: SubClipAttributeModifier):
    if not PythonValidator.is_instance(element, SubClipAttributeModifier):
        raise Exception('The provided "element" parameter is not a SubClipAttributeModifier instance.')
    
def _validate_zoom(zoom: int):
    if not NumberValidator.is_number_between(zoom, ZOOM_LIMIT[0], ZOOM_LIMIT[1]):
        raise Exception(f'The "zoom" parameter provided is not a number between [{ZOOM_LIMIT[0]}, {ZOOM_LIMIT[1]}].')
    
def _validate_x_movement(x_movement: int):
    if not NumberValidator.is_number_between(x_movement, -DEFAULT_SCENE_SIZE[0] * 4, DEFAULT_SCENE_SIZE[0] * 4):
        raise Exception(f'The "x_movement" parameter provided is not a number between [{-DEFAULT_SCENE_SIZE[0] * 4}, {DEFAULT_SCENE_SIZE[0] * 4}].')
    
def _validate_y_movement(y_movement: int):
    if not NumberValidator.is_number_between(y_movement, -DEFAULT_SCENE_SIZE[0] * 4, DEFAULT_SCENE_SIZE[0] * 4):
        raise Exception(f'The "y_movement" parameter provided is not a number between [{-DEFAULT_SCENE_SIZE[0] * 4}, {DEFAULT_SCENE_SIZE[0] * 4}].')

def _validate_rotation(rotation: int):
    if not NumberValidator.is_number_between(rotation, ROTATION_LIMIT[0], ROTATION_LIMIT[1]):
        raise Exception(f'The "rotation" parameter provided is not a number between [{ROTATION_LIMIT[0]}, {ROTATION_LIMIT[1]}].')
    
def _validate_setting(setting: SubClipSetting, name: str, range: tuple[float, float]):
    if not PythonValidator.is_instance(setting, SubClipSetting):
        raise Exception(f'The provided "{name}" is not a SubClipSetting instance.')
    
    if not NumberValidator.is_number_between(setting.initial_value, range[0], range[1]):
        raise Exception(f'The "{name}" parameter provided "initial_value" is not a number between [{range[0]}, {range[1]}].')
    
    if not NumberValidator.is_number_between(setting.final_value, range[0], range[1]):
        raise Exception(f'The "{name}" parameter provided "final_value" is not a number between [{range[0]}, {range[1]}].')

def _validate_attribute_modifier(attribute_modifier: SubClipAttributeModifier, name: str, limit_range: tuple[float, float], number_of_frames: int):
    """
    Validate the provided 'attribute_modifier' according to
    the given 'limit_range' in which all the values must fit.
    Also, if it is a Graphic instance, the 'number_of_frames'
    will be used to generate the values and check them.
    """
    if not PythonValidator.is_instance(attribute_modifier, SubClipAttributeModifier):
        raise Exception(f'The parameter "{name}" provided is not a SubClipAttributeModifier instance.')
    
    if PythonValidator.is_list(attribute_modifier.modifier):
        # TODO: Validate all values
        if any(not NumberValidator.is_number_between(value, limit_range[0], limit_range[1]) for value in attribute_modifier.modifier):
            raise Exception(f'The parameter "{name}" provided has at least one value out of the limits [{limit_range[0]}, {limit_range[1]}]')
    elif PythonValidator.is_instance(attribute_modifier.modifier, SubClipSetting):
        if not NumberValidator.is_number_between(attribute_modifier.modifier.initial_value, limit_range[0], limit_range[1]):
            raise Exception(f'The parameter "{name}" provided "initial_value" is not a number between [{limit_range[0]}, {limit_range[1]}].')
        
        if not NumberValidator.is_number_between(attribute_modifier.modifier.final_value, limit_range[0], limit_range[1]):
            raise Exception(f'The parameter "{name}" provided "final_value" is not a number between [{limit_range[0]}, {limit_range[1]}].')
    elif PythonValidator.is_instance(attribute_modifier.modifier, 'Graphic'):
        # TODO: This is very agressive, according to the way
        # we join the pairs of nodes we could get outliers
        # that are obviously out of the limit range. Some
        # easing functions have values below 0 and over 1.
        if any(not NumberValidator.is_number_between(value, limit_range[0], limit_range[1]) for value in attribute_modifier.get_values(number_of_frames)):
            raise Exception(f'The parameter "{name}" provided has at least one value out of the limits [{limit_range[0]}, {limit_range[1]}]')