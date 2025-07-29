from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionResize
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWithPrecalculated
from yta_multimedia.video import MPVideo
from yta_multimedia.video.position import Position
from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from yta_general_utils.math.rate_functions.rate_function import RateFunction
from moviepy.Clip import Clip


class ZoomInDisplayAndZoomOutEffect(Effect):
    """
    Makes the provided clip have a zoom in effect, then
    being displayed at all, and later being zoomed out
    before finishing.

    This effect is recommended to be used with a pure 
    white background.
    """
    def apply(
        self,
        video: Clip
    ) -> Clip:
        background_video = ClipGenerator.get_default_background_video(duration = video.duration, fps = video.fps)

        return self.apply_over_video(video, background_video)
    
    def apply_over_video(
        self,
        video: Clip,
        background_video: Clip
    ):
        video = VideoParser.to_moviepy(video)
        background_video = VideoParser.to_moviepy(background_video)

        video_handler = MPVideo(video)
        zoom_duration = 30 * video_handler.frame_duration

        # TODO: This has to be passed as argument, but it is a good
        # background for the movement
        #first_white_background = ClipGenerator.generate_color_background((1920, 1080), [255, 255, 255], video.duration, video.fps)
        
        resizes = []
        for t in video_handler.frames_time_moments:
            if t < zoom_duration:
                resizes.append(TFunctionResize.resize_from_to(t, zoom_duration, 1.0, 0.7, RateFunctionArgument(RateFunction.EASE_IN_EXPO)))
            elif t < (video.duration - zoom_duration):
                resizes.append(0.7)
            else:
                resizes.append(TFunctionResize.resize_from_to(t - (video.duration - zoom_duration), zoom_duration, 0.7, 1.0, RateFunctionArgument(RateFunction.EASE_IN_EXPO)))

        positions = [
            Position.CENTER.get_moviepy_upper_left_corner_tuple((video.w * resizes[i], video.h * resizes[i]), background_video.size)
            for i in range(len(resizes))
        ]

        return MoviepyWithPrecalculated().apply_over_video(video, background_video, resized_list = resizes, with_position_list = positions)