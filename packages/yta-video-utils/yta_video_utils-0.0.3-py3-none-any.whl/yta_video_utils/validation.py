from yta_general_utils.coordinate import NORMALIZATION_MAX_VALUE, NORMALIZATION_MIN_VALUE
from yta_validation import PythonValidator
from yta_validation.number import NumberValidator
from yta_validation.parameter import ParameterValidator
from typing import Union


# TODO: These 2 methods below are similar to the ones in
# yta_multimedia\video\edition\effect\moviepy\position\objects\coordinate.py
# TODO: Maybe wrap in a 'VideoParametersValidator'
# class (?)
def is_size_valid(
    size: Union[tuple, list]
):
    """
    Check if the provided 'size' is a valid
    value or not, which means that is a tuple,
    list or array of 2 elements that are
    between the expected values.
    """
    return PythonValidator.is_numeric_tuple_or_list_or_array_of_2_elements_between_values(size, 1, NORMALIZATION_MAX_VALUE, 1, NORMALIZATION_MAX_VALUE)

def validate_size(
    size: tuple,
    parameter_name: str = 'size'
):
    """
    Validate the provided 'size' and raises an Exception if
    not valid.
    """
    ParameterValidator.validate_mandatory_numeric_tuple_or_list_or_array_of_2_elements_between_values(parameter_name, size, 1, NORMALIZATION_MAX_VALUE, 1, NORMALIZATION_MAX_VALUE)

def is_duration_valid(
    duration: float
) -> bool:
    """
    Check if the provided 'duration' is a valid
    duration, which means a positive number.
    """
    # TODO: We could maybe accept 'fps' parameter to check
    # if 'duration' is a multiple
    return NumberValidator.is_positive_number('duration', duration, do_include_zero = False)

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

def is_fps_valid(
    fps: float
) -> bool:
    """
    Check if the provided 'fps' is valid to
    build a moviepy video clip, which must
    be a positive number.
    """
    return NumberValidator.is_positive_number('fps', fps, do_include_zero = False)

def validate_fps(
    fps: float
):
    """
    Check if the provided 'fps' is valid
    to build a moviepy video clip or
    raises an exception if not.
    """
    ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

def is_opacity_valid(
    opacity: float
) -> bool:
    """
    Check if the provided 'opacity' is 
    valid to build a moviepy video clip,
    which must be a value between 0.0 
    and 1.0.
    """
    return NumberValidator.is_number_between(opacity, 0.0, 1.0)

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
    
def is_position_valid(
    position: Union[list, tuple]
):
    """
    It is a list or tuple of 2 values which are between
    our min and max normalization values.
    """
    return PythonValidator.is_numeric_tuple_or_list_or_array_of_2_elements_between_values(position, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)

def validate_position(
    position: Union[list, tuple],
    parameter_name: str = 'position'
):
    """
    Validate if the given 'position' is a valid position,
    which must be a tuple or array of 2 elements between
    our min and max normalization values.
    """
    ParameterValidator.validate_mandatory_numeric_tuple_or_list_or_array_of_2_elements_between_values(parameter_name, position, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE)

