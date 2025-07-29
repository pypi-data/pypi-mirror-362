"""
Some validation utils to avoid
repeating code.
"""
from yta_validation.parameter import ParameterValidator
from yta_validation.number import NumberValidator
from yta_validation import PythonValidator


def validate_size(
    size: tuple
) -> None:
    """
    Check if the provided 'size' is 
    valid to build a moviepy video clip
    or raises an exception if not.
    """
    if (
        not PythonValidator.is_tuple(size) or
        len(size) != 2 or
        not NumberValidator.is_number_between(size[0], 0, 5000) or
        not NumberValidator.is_number_between(size[1], 0, 5000)
    ):
        raise Exception('The provided "duration" is not a tuple or does not have the expected size (2) or the values are not between 0 and 5000.')
    
def validate_duration(
    duration: float
) -> None:
    """
    Check if the provided 'duration' is
    valid to build a moviepy video clip
    or raises an exception if not.
    """
    # TODO: We could maybe accept 'fps' parameter to check
    # if 'duration' is a multiple
    ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
    
def validate_fps(
    fps: float
):
    """
    Check if the provided 'fps' is valid
    to build a moviepy video clip or
    raises an exception if not.
    """
    ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

def validate_opacity(
    opacity: float
):
    """
    Check if the provided 'opacity' is
    valid to build a moviepy mask
    video clip or raises an exception
    if not.
    """
    ParameterValidator.validate_mandatory_number_between('opacity', opacity, 0.0, 1.0)