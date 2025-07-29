from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_colors import Color
from yta_constants.color import ColorString
from moviepy import Clip
from moviepy.video.fx import FadeOut as MoviepyFadeOut
from typing import Union


class FadeOutEffect(Effect):
    """
    This effect will make the video
    disappear progressively lasting the
    provided 'duration' time or the
    whole clip duration if None
    'duration' provided.

    The 'color' provided must be a valid
    color string, array, tuple or Color
    instance, or will be set as pure
    black if None provided.
    """

    def apply(
        self,
        video: Clip,
        duration: float,
        color: Union[list, tuple, str, Color] = None
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        duration = duration if duration is not None else video.duration
        color = Color.parse(color).as_rgb_array() if color is not None else Color.parse(ColorString.BLACK).as_rgb_array()

        return MoviepyFadeOut(duration, color).apply(video)
    
    # TODO: I don't need this
    def apply_over_video(
        self,
        video,
        background_video
    ):
        return super().apply_over_video(video, background_video)