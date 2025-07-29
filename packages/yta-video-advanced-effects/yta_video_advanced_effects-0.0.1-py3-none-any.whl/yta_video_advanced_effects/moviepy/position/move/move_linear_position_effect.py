from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWith, WithPositionArgument
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from yta_validation import PythonValidator
from moviepy.Clip import Clip
from typing import Union


class MoveLinearPositionEffect(Effect):
    """
    Move from A to B doing a straight line
    effect while moving.
    """

    # TODO: Is this working (?)
    result_must_replace = True

    def apply(
        cls,
        video: Union[Clip, str],
        initial_position: Union[Coordinate, Position],
        final_position: Union[Coordinate, Position]
    ):
        video = VideoParser.to_moviepy(video)

        # TODO: Validate and parse 'initial_position' and 
        # 'final_position'. These positions must be coordinates
        # on a 1920x1080 scene.
        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.linear, RateFunctionArgument.default())

        return MoviepyWith.apply(video, with_position = arg)
    
    def apply_over_video(
        cls,
        video: Union[Clip, str],
        background_video: Union[Clip, str],
        initial_position: Union[Coordinate, Position],
        final_position: Union[Coordinate, Position]
    ):
        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.linear, RateFunctionArgument.default())

        return MoviepyWith.apply_over_video(video, background_video, with_position = arg)
    
    # TODO: Should be static (?)
    def get_arrays(
        self,
        number_of_frames: int,
        fps: float,
        initial_position: Union[Coordinate, Position, tuple[int, int]],
        final_position: Union[Coordinate, Position, tuple[int, int]]
    ):
        """
        Get the 'with_position', 'resized', and 'rotated' arrays
        to apply the effect on a SubClip instance. Each array can
        be None if not affected by this effect.
        """
        from yta_general_utils.math.map.map import Map

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

        return MoviepyWith.get_arrays(
            number_of_frames,
            fps,
            with_position = WithPositionArgument(Map().add_coordinate(initial_position).add_coordinate(final_position))
        )