from yta_video_base.frame.utils import frame_time_to_frame_index


class VideoFilter:
    # TODO: Move these methods to a more specific file
    # or class
    
    @staticmethod
    def apply_t_effect(frame, t: float, fps: int, frames_indexes: list[int], effect: callable, *args):
        if frame_time_to_frame_index(t, fps) in frames_indexes:
            return effect(frame, *args)

        return frame


def test():
    # TODO: This below has been used in 'youtube-stuff' to
    # test a new way of handling frame effects
    # TODO: 'video' is just a video
    from yta_image.edition.filter import ImageFilter
    from yta_image.edition.filter.motion_blur import MotionBlurDirection
    from random import choice

    def image_filter_arguments(index: int):
        # TODO: Of course, index must be ok
        # TODO: This can be whatever I want, maybe a class
        # in which I push my arrays in execution time and
        # have the logic in code

        # We have the effect values ordered in the same 
        # order as per each frame, so we return them to 
        # be applied like that
        effect_values = [10, 20, 30, 40, 30, 20, 10, 20, 10, 80]

        return effect_values[index], choice(MotionBlurDirection.get_all())

    frames_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    from moviepy.Clip import Clip
    from typing import Union

    class FramesEffect:
        frames_indexes: list[int] = None
        method: callable = None
        args_generator_function: callable = None

        def __init__(self, frames_indexes: list[int], method: callable, args_generator_function: callable):
            self.frames_indexes = frames_indexes
            self.method = method
            self.args_generator_function = args_generator_function

        def validate(self):
            # TODO: The length of all args returned by
            # 'args_generator_function' must be equal to
            # 'frames_indexes' length

            # TODO: Raise Exception if invalid
            return True
        
        def apply(self, video: Clip, output_filename: Union[str, None] = None):
            def apply_effect_on_frame(frame, t: float):
                try:
                    index = self.frames_indexes.index(frame_time_to_frame_index(t, video.fps))
                    print(f'Hi, I am in {index}')

                    return self.method(frame, *self.args_generator_function(index))
                except:
                    pass

                return frame
                                        
            video = video.transform(lambda get_frame, t: apply_effect_on_frame(get_frame(t), t))

            if output_filename is not None:
                video.write_videofile(output_filename)

            return video
        

    # # TODO: Think about how to make the method that
    # # returns the arguments be easier to create and
    # # apply, because it is not easy to understand...
    # FramesEffect(frames_indexes, ImageFilter.motion_blur, image_filter_arguments).apply(FramesEffect(frames_indexes, ImageFilter.motion_blur, image_filter_arguments).apply(video)).write_videofile('a_a_borrame.mp4')


"""
# Example of a function using those frame numbers
# or indexes in a condition to apply or not an
# effect to a frame
apply_motion_blur_at_begining(frame, t, motion_blur_kernels, fps):
    frame_number = MPVideo.frame_time_to_frame_index(t, fps)
    
    if frame_number < len(motion_blur_kernels):
        return ImageFilter.motion_blur(frame, motion_blur_kernels[frame_number])
    
    return frame
"""