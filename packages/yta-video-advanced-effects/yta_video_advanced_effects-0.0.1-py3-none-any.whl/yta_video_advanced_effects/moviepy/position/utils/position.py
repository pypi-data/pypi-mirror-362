# TODO: This package is 'position.utils.position' so it doesn't make sense
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.position import Position
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from typing import Union


"""
    Coords related functions below
"""
def get_moviepy_position(
    video,
    background_video,
    position: Union[Coordinate, Position, tuple]
):
    """
    In the process of overlaying and moving the provided 'video' over
    the also provided 'background_video', this method calculates the
    (x, y) tuple position that would be, hypothetically, adapted from
    a 1920x1080 black color background static image. The provided 
    'position' will be transformed into the (x, y) tuple according
    to our own definitions in which the video (that starts in upper left
    corner) needs to be placed to fit the desired 'position'.
    """
    video = VideoParser.to_moviepy(video)
    background_video = VideoParser.to_moviepy(background_video)
    
    ParameterValidator.validate_mandatory_instance_of('position', position, [Coordinate, Position, tuple])
    
    if PythonValidator.is_tuple(position) and len(position) != 2:
        # TODO: Maybe apply the normalization limits as limits
        # here for each position tuple element
        raise Exception('Provided "position" is a tuple but does not have 2 values.')
    
    return (
        position.get_moviepy_upper_left_corner_tuple(video.size, background_video.size)
        if PythonValidator.is_instance(position, Position) else
        position.update_scene_size(background_video.size).get_moviepy_upper_left_corner_tuple(video.size)
        if PythonValidator.is_instance(position, Coordinate) else
        position
    )