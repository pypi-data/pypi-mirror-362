from yta_video_base.parser import VideoParser
from yta_multimedia.video.edition.subclip import subclip_video
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from yta_validation.number import NumberValidator
from moviepy.Effect import Effect
from moviepy.Clip import Clip
from moviepy import concatenate_videoclips
from abc import abstractmethod


# TODO: Maybe rename
class MEffect(Effect):
    """
    Effect to be applied on a single
    video without any other video
    dependence.

    This effect cannot be applied as
    a moviepy effect as the structure
    is different.

    TODO: If I want to make my own moviepy effects that
    are able to be applied as moviepy does, I need to
    respect the structure and just manipulate the frames.
    So, those new custom moviepy effects sohuld be placed
    in other folder as this MEffect is my own effect that
    works in a different way.
    """

    # TODO: Is this working (?)
    result_must_replace: bool = False
    """
    This parameter indicates if this effect, when applied,
    must replace the original clip part or, if False, must
    be concatenated.
    """
    @abstractmethod
    def apply_over_video(
        self,
        video: Clip,
        background_video: Clip
    ):
        # TODO: Should I (?)
        pass

    @staticmethod
    def apply_effect_partially_on_video(
        video: Clip,
        effect: 'MEffect',
        start_time: float = 0,
        end_time: float = None
    ):
        """
        Apply the provided 'effect' in the also provided 'video'
        in the part between the given 'start_time' and 'end_time'.
        """
        video = VideoParser.to_moviepy(video)

        # TODO: It will be a subclass of it, does it work (?)
        ParameterValidator.validate_mandatory_instance_of('effect', effect, MEffect)

        if (
            not NumberValidator.is_number_between(start_time, 0, video.duration) or
            not NumberValidator.is_number_between(end_time, 0, video.duration) or
            start_time >= end_time
        ):
            raise Exception('The provided "start_time" and "end_time" parameters ("{str(start_time)}" and "{str(end_time)}") must be values between 0 and the provided clip duration ("{str(video.duration)}"), and "end_time" must be greater than "start_time".')
        
        left, center, right = subclip_video(video, start_time, end_time)
        # TODO: What if only '.apply()' instead of '.apply_over_video()'
        # is needed (?)
        center = effect.apply_over_video(center.with_subclip(start_time, end_time))

        clips = [
            clip
            for clip in [left, center, right]
            if clip is not None
        ]

        return concatenate_videoclips(clips)#.with_start(start)