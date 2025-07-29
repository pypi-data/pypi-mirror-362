from yta_validation.parameter import ParameterValidator
from yta_file.filename.handler import FilenameHandler, FileType
from yta_file.handler import FileHandler

# TODO: Can I avoid the use of opencv? :)
import cv2


def get_video_size(
    video_filename: str
):
    """
    Return a tuple containing the provided
    'video_filename' size (w, h) if the parameter
    is a filename of a valid video file.
    """
    # TODO: Refactor this method to allow any kind
    # of video parameter and I detect dynamically
    # if str to use this below, or clip to use moviepy
    ParameterValidator.validate_mandatory_string('video_filename', video_filename)
    
    # TODO: This validation is not parsing the content
    if (
        not FileHandler.is_file(video_filename) or
        not FilenameHandler.is_of_type(video_filename, FileType.VIDEO)
    ):
        raise Exception('The provided "video_filename" is not a valid video file name.')
    
    # TODO: I don't know where did this method
    # 'file_is_video_file' go when refactoring X)
    # if not FileValidator.file_is_video_file(video_filename):
    #     raise Exception('The provided "video_filename" is not a valid video file name.')

    v = cv2.VideoCapture(video_filename)

    return (
        int(v.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

__all__ = [
    get_video_size
]

