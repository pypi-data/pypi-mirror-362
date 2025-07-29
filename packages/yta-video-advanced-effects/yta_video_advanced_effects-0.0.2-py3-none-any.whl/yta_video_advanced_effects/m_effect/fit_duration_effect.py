from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_validation.parameter import ParameterValidator
from moviepy.video.fx import MultiplySpeed
from moviepy import Clip


class FitDurationEffect(Effect):
    """
    This effect changes the speed of
    the video to fit the requested
    'duration', that will accelerate
    or decelerate the video speed.
    """

    def apply(
        self,
        video: Clip,
        duration: float = None
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        ParameterValidator.validate_mandatory_number_between('duration', duration, 0, 120)

        return MultiplySpeed(final_duration = duration).apply(video)
    
    # TODO: I don't need this
    def apply_over_video(
        self,
        video,
        background_video
    ):
        return super().apply_over_video(video, background_video)
    
# TODO: Maybe I can create another effect to set
# the speed by multiplying it by a factor, but 
# by now this one is enough