from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_multimedia.video.edition.effect.constants import EFFECTS_RESOURCES_FOLDER
from yta_multimedia.resources.video.effect.sound.drive_urls import SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL
from yta_multimedia.resources import Resource
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_validation.parameter import ParameterValidator
from moviepy import Clip, ImageClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.BlackAndWhite import BlackAndWhite


class SadMomentEffect(Effect):
    """
    This method gets the first frame of the provided 'clip' and returns a
    new clip that is an incredible 'sad_moment' effect with black and white
    filter, zoom in and rotating effect and also sad violin music.

    The 'duration' parameter is to set the returned clip duration, but the
    default value is a perfect one and it should be keept as it is if 
    possible.

    What to do with the result? **CONCATENATE**

    The result should be added to the clip and must not replace it because
    it freezes one frame so it should continue with the next frame and the
    video as it is.
    """

    # TODO: Is this working (?)
    result_must_replace = False

    def apply(
        self,
        video: Clip,
        duration: float = None
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlurEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        duration = (
            duration
            if duration is not None else
            4.8
        )

        ParameterValidator.validate_mandatory_number_between('duration', duration, 0, 120)
        
        # We freeze the first frame
        aux = ImageClip(video.get_frame(0), duration = duration)
        aux.fps = video.fps
        video = aux

        # We then build the whole effect
        # TODO: I don't want to use the moviepy b&w effect
        video = video.with_effects([BlackAndWhite()]).resized(lambda t: 1 + 0.30 * (t / video.duration)).with_position(lambda t: (-(0.15 * video.w * (t / video.duration)), -(0.15 * video.h * (t / video.duration)))).rotated(lambda t: 5 * (t / video.duration), expand = False)

        # We set the effect audio
        TMP_FILENAME = Resource.get(SAD_MOMENT_GOOGLE_DRIVE_DOWNLOAD_URL, EFFECTS_RESOURCES_FOLDER + 'sounds/sad_moment.mp3')
        video.audio = AudioFileClip(TMP_FILENAME).with_duration(video.duration)

        return CompositeVideoClip([
            ClipGenerator.get_default_background_video(size = video.size, duration = video.duration, fps = video.fps),
            video,
        ])
    
    # TODO: I don't need this
    def apply_over_video(
        self,
        video,
        background_video
    ):
        return super().apply_over_video(video, background_video)