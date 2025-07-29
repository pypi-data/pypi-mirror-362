from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from moviepy.video.fx import MirrorY
from moviepy import Clip


class FlipVerticallyEffect(Effect):
    """
    This effect flips the video vertically
    (including the mask).
    """

    def apply(
        self,
        video: Clip
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        return MirrorY().apply(video)
    
    # TODO: I don't need this
    def apply_over_video(
        self,
        video,
        background_video
    ):
        return super().apply_over_video(video, background_video)