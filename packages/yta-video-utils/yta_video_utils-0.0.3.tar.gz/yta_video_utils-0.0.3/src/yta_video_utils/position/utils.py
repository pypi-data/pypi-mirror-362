from yta_video_utils.validation import validate_position, validate_size
# TODO: Move this to 'yta_constants.video'
from yta_constants.multimedia import DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT
from typing import Union


def get_moviepy_center_position(
    background_video_size: Union[tuple, list],
    position: Union[tuple, list]
):
    """
    Considering an scene of 1920x1080, calculate the
    given 'position' according to the real scene 
    which is the provided 'background_video_size'.
    This position will be the place in which the
    center of the element we are positioning must be
    placed to make its center be in the given
    'position'.

    The provided 'position' must be a tuple or list
    of two elements (x, y) or [x, y], accepting not
    the Position nor the DependantPosition Enums.

    This method must be used with the moviepy engine.
    """
    validate_size(background_video_size)
    validate_position(position)

    # Adapt 1920x1080 'position' to real background video size
    return (
        position[0] * background_video_size[0] / DEFAULT_SCENE_WIDTH,
        position[1] * background_video_size[1] / DEFAULT_SCENE_HEIGHT
    )
    
def get_moviepy_upper_left_position(
    background_video_size: Union[tuple, list],
    video_size: Union[tuple, list],
    position: Union[tuple, list]
):
    """
    Considering an scene of 1920x1080, calculate the
    given 'position' according to the real scene 
    which is the provided 'background_video_size'.
    This position will be the place in which the
    upper left corner of the element we are
    positioning must be placed to make its center be
    in the given 'position'.

    The provided 'position' must be a tuple or list
    of two elements (x, y) or [x, y], accepting not
    the Position nor the DependantPosition Enums.

    This method must be used with the moviepy engine.
    """
    validate_size(background_video_size)
    validate_size(video_size)
    validate_position(position)

    position = get_moviepy_center_position(background_video_size, position)

    # Recalculate to fit the video size
    return (
        position[0] - video_size[0] / 2,
        position[1] - video_size[1] / 2
    )

