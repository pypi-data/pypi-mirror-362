from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_advanced_effects.moviepy.position.objects.coordinate import Coordinate
from yta_video_advanced_effects.moviepy.objects import MoviepyWith, MoviepyArgument
from yta_video_advanced_effects.moviepy.t_function import TFunctionSetPosition
from yta_video_base.position import Position
from yta_video_base.generator import MoviepyNormalClipGenerator
from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from moviepy.Clip import Clip
from typing import Union


class StayAtPositionEffect(Effect):

    def apply(
        self,
        video: Clip,
        position: Union[Position, Coordinate, tuple] = Position.CENTER
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        background_video = MoviepyNormalClipGenerator.get_static_default_color_background(duration = video.duration, fps = video.fps)

        return self.apply_over_video(video, background_video, position)
    
    # TODO: What about this (?)
    def apply_over_video(
        self,
        video: Clip,
        background_video: Clip,
        position: Union[Position, Coordinate] = Position.CENTER
    ) -> Clip:
        arg = MoviepyArgument(position, position, TFunctionSetPosition.linear, RateFunctionArgument.default())

        return MoviepyWith().apply_over_video(video, background_video, with_position = arg)