from yta_video_advanced_effects.s_effect import SEffect, SEffectType
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.objects import WithPositionArgument
from yta_general_utils.math.map.map import Map
from yta_validation import PythonValidator
from typing import Tuple, Union

import numpy as np


class MoveLinearSEffect(SEffect):
    """
    This effect is handled frame by frame and returns
    the array of values for each frame to obtain the
    expected result.
    """
    
    def __init__(
        self,
        number_of_frames: int,
        initial_position: Union[Coordinate, Position, tuple[int, int]],
        final_position: Union[Coordinate, Position, tuple[int, int]]
    ):
        # TODO: Improve this by first raising Exceptions with 
        # non accepted values and then transforming them
        if PythonValidator.is_instance(initial_position, Coordinate):
            initial_position = initial_position.as_moviepy_tuple
        elif PythonValidator.is_instance(initial_position, Position):
            initial_position = initial_position.get_moviepy_center_tuple()
        elif PythonValidator.is_tuple(initial_position) and len(initial_position) == 2:
            # Default scene of 1920x1080
            initial_position = initial_position
        else:
            raise Exception('The provided "initial_position" parameter is not valid.')

        if PythonValidator.is_instance(final_position, Coordinate):
            final_position = final_position.as_moviepy_tuple
        elif PythonValidator.is_instance(final_position, Position):
            final_position = final_position.get_moviepy_center_tuple() 
        elif PythonValidator.is_tuple(final_position) and len(final_position) == 2:
            # Default scene of 1920x1080
            final_position = final_position
        else:
            raise Exception('The provided "final_position" parameter is not valid.')

        super().__init__(
            number_of_frames,
            SEffectType.MOVEMENT,
            initial_position = initial_position,
            final_position = final_position
        )

    @staticmethod
    def calculate(
        number_of_frames: int,
        initial_position: tuple[int, int],
        final_position: tuple[int, int]
    ) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 4 arrays:
         
        - frames
        - with_position
        - resized
        - rotated
        
        with the provided 'number_of_frames' and
        additional arguments and return each of
        them if affected, or None if not.
        """
        return (
            None,
            WithPositionArgument(Map().add_coordinate(initial_position).add_coordinate(final_position)).get_values(number_of_frames),
            None,
            None
        )