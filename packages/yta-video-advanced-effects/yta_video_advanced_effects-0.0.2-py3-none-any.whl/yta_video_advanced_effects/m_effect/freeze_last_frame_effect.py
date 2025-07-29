from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_multimedia.video.utils import generate_video_from_image
from yta_validation.number import NumberValidator
from moviepy.Clip import Clip


class FreezeLastFrameEffect(Effect):
    """
    Freeze the last frame of the provided
    'video' and returns a new video of the
    provided 'duration' that is that frame
    freezed.
    """

    def apply(
        self,
        video: Clip,
        duration: float = 1
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        duration = duration if duration is not None else 1

        if not NumberValidator.is_positive_number(duration, False):
            raise Exception(f'The provided "duration" parameter "{str(duration)}" is not valid.')

        frame = VideoFrameExtractor.get_frame_by_t(video, video.duration)
        frame_freezed_video = generate_video_from_image(frame, duration, fps = video.fps)

        return frame_freezed_video

    def apply_over_video(
        self
    ):
        pass