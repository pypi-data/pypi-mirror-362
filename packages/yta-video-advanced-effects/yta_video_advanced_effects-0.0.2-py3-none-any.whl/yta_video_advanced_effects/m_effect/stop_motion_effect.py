from yta_video_advanced_effects.m_effect import MEffect as Effect
from yta_video_base.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from moviepy import Clip, ImageClip, concatenate_videoclips


class StopMotionEffect(Effect):
    """
    Creates a Stop Motion effect in the provided video
    by dropping the frames per second but maintaining
    the original frames ratio.
    """

    def apply(
        self,
        video: Clip
    ) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        FRAMES_TO_JUMP = 5

        clips = []
        for frame_number in range((int) (video.fps * video.duration)):
            if frame_number % FRAMES_TO_JUMP == 0:
                frame = VideoFrameExtractor.get_frame_by_index(video, frame_number)
                # TODO: What about the mask (?)
                clips.append(ImageClip(frame, duration = FRAMES_TO_JUMP / video.fps).with_fps(video.fps))

        return concatenate_videoclips(clips).with_audio(video.audio).with_fps(video.fps)
    
    # TODO: I don't need this
    def apply_over_video(
        self,
        video,
        background_video
    ):
        return super().apply_over_video(video, background_video)