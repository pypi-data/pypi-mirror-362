from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video import MPVideo
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from yta_validation import PythonValidator
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip
from typing import Union


class MoviepyArgument:
    """
    Arguments used for 'with_position', 'resized' and 'rotated'
    simplified and unified to have the same structure to build
    new videos by modifying the basic moviepy effects.
    """

    def __init__(
        self,
        start: Union[int, tuple, float],
        end: Union[int, tuple, float],
        t_function: type,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        # TODO: 'start' and 'end' must be pure values which
        # means tuples if positions or numbers if resize or
        # rotate
        # TODO: Validate parameters
        self.start = start
        self.end = end
        self.t_function = t_function
        self.rate_function = rate_function
        # TODO: *args or **kwargs should be avoided as we must
        # define the 't_function' with the only parameters 
        # needed and make as much as we need. For example, we
        # should have '.arc_bottom' and '.arc_top' to avoid
        # passing a 'is_bottom' parameter because it would 
        # lost the common structure.

class WithPositionArgument:
    """
    A wrapper to hold a 'with_position' value generator.
    """
    
    def __init__(
        self,
        argument: Union[tuple[int, int], 'Map'],
        extra_argument: Union[any, None] = None
    ):
        # TODO: Implement an 'extra_movement' that allows us
        # make an aditional movement (shaking, doing circles,
        # etc.) while going from start to end. See the
        # TFunctionSetPosition to get inspiration
        if (
            (
                not PythonValidator.is_tuple(argument) or
                len(argument) != 2
            ) and
            not PythonValidator.is_instance(argument, 'Map')
        ):
            raise Exception('The provided "argument" parameter is not valid.')
        
        self.argument = argument

    def get_values(
        self,
        n: int
    ):
        """
        Generates a with_position value for each frame
        position, which is a pair of (x, y) values that
        are the place in which the center of the video
        must be placed. The 'n' parameter is the number
        of frames.
        """
        return (
            [self.argument] * n
            if PythonValidator.is_tuple(self.argument) else
            self.argument.get_n_values(n)
            if PythonValidator.is_instance(self.argument, 'Map') else
            None # TODO: Maybe raise Exception (?)
        )

class RotatedArgument:
    """
    A wrapper to hold a 'rotated' value generator.
    """

    def __init__(
        self,
        argument: Union[int, 'SubClipSetting', 'Graphic']
    ):
        if (
            not PythonValidator.is_number(argument) and
            not PythonValidator.is_instance(argument, 'SubClipSetting') and
            not PythonValidator.is_instance(argument, 'Graphic')
        ):
            raise Exception('The provided "argument" parameter is not a valid modifier.')
        
        self.argument = argument

    def get_values(
        self,
        n: int
    ):
        """
        Generates a rotation value for each frame
        position, where 'n' is the number of frames.
        """
        return (
            [int(self.argument)] * n
            if PythonValidator.is_number(self.argument) else
            [
                int(value)
                for value in self.argument.get_values(n)
            ]
            if PythonValidator.is_instance(self.argument, 'SubClipSetting') else
            [
                int(value[1])
                for value in self.argument.get_n_values(n)
            ]
            if PythonValidator.is_instance(self.argument, 'Graphic') else
            None # TODO: Maybe raise Exception (?)
        )

class ResizedArgument:
    """
    A wrapper to hold a 'resized' value generator.
    """

    # TODO: This doesn't allow a double generator in
    # which the first and the second factor are being
    # generated individually. This generates only one
    # resize factor that is applied for w and h
    def __init__(
        self,
        argument: Union[tuple[float, float], 'SubClipSetting', 'Graphic']
    ):
        if (
            (not PythonValidator.is_tuple(argument) or
            (PythonValidator.is_tuple(argument) and len(argument) != 2)) and
            not PythonValidator.is_instance(argument, 'SubClipSetting') and
            not PythonValidator.is_instance(argument, 'Graphic')
        ):
            raise Exception('The provided "argument" parameter is not a valid modifier.')
        
        self.argument = argument

    def get_values(
        self,
        n: int
    ):
        """
        Generates an array with a pair of resize factors
        (first for width, second for height) for each
        frame position, where 'n' is the number of frames.
        """
        return (
            [self.argument] * n
            if PythonValidator.is_tuple(self.argument) else
            [
                [value, value]
                for value in self.argument.get_values(n)
            ]
            if PythonValidator.is_instance(self.argument, 'SubClipSetting') else
            [
                [value[1], value[1]]
                for value in self.argument.get_n_values(n)
            ]
            if PythonValidator.is_instance(self.argument, 'Graphic') else
            None # TODO: Maybe raise Exception (?)
        )

# TODO: Rename to MoviepyWithProcess or something more clear
# TODO: We need to accept a GraphicInterpolation as, at least,
# the 'with_position' parameter and build the needed values
# as it is happening for the example I leave in the 
# video\edition\effect\moviepy\position\move\refactor_this.py
# file code.
class MoviepyWith:
    """
    Class to encapsulate the 'resized', 'with_position' and
    'rotated' functionality and to be able to make one depend
    on the other by pre-calculating the values and then using
    them when positioning, resizing and rotating.

    You should use the same RateFunction if you are planning
    to move and resize the clip at the same time.
    """

    @staticmethod
    def apply(
        video: Clip,
        with_position: Union[MoviepyArgument, None] = None,
        resized: Union[MoviepyArgument, None] = None,
        rotated: Union[MoviepyArgument, None] = None
    ):
        """
        Apply the property effects on the provided 'video'. This
        method will use a default background video to apply the
        effect.

        Default background is 1920x1080.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        return MoviepyWith.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration, fps = video.fps), with_position, resized, rotated)

    @staticmethod
    def apply_over_video(
        video: Clip,
        background_video: Clip,
        with_position: Union[MoviepyArgument, None] = None,
        resized: Union[MoviepyArgument, None] = None,
        rotated: Union[MoviepyArgument, None] = None
    ):
        """
        Apply the property effects on the provided 'video'. This
        method will use the provided 'background_video' and 
        recalculate the position according to it.

        Background can be different to default scene of 1920x1080
        so positions will be adjusted to it.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)
        background_video = VideoParser.to_moviepy(background_video, True)

        # Prepare data for pre-calculations
        video_handler = MPVideo(video)

        background_video = video_handler.prepare_background_clip(background_video)

        if resized:
            resizes = [
                resized.t_function(t, video_handler.duration, resized.start, resized.end, resized.rate_function)
                for t in video_handler.frames_time_moments
            ]
        else:
            # We build always this array because position calculation 
            # depends on it to be able to handle movement and resizing
            # at the same time
            resizes = [
                1
                for _ in video_handler.frames_time_moments
            ]

        positions = None
        if with_position:
            # TODO: Maybe this 'get_moviepy_position' can be replaced
            # with the Coordinate scene adapter method
            initial_position = get_moviepy_position(video, background_video, with_position.start)
            final_position = get_moviepy_position(video, background_video, with_position.end)
            positions = []
            for i, t in enumerate(video_handler.frames_time_moments):
                # Calculate each frame position based on each frame size
                initial_position = (initial_position[0] * resizes[i], initial_position[1] * resizes[i])
                final_position = (final_position[0] * resizes[i], final_position[1] * resizes[1])

                # TODO: This 'with_position.t_function' can have different
                # parameters to be able to work, so I don't know how to
                # dynamically handle this. For example, the 'at_position'
                # needs the video.size to be able to calculate where to
                # be centered...
                positions.append(with_position.t_function(t, video.duration, initial_position, final_position))
                
        rotations = None
        if rotated:
            rotations = [
                rotated.t_function(t, video_handler.duration, rotated.start, rotated.end, rotated.rate_function)
                for t in video_handler.frames_time_moments
            ]

        # TODO: Maybe avoid the 'resizes' with ones if is the
        # only one we will pass as param

        video = MoviepyWithPrecalculated.apply(video, positions, resizes, rotations)

        return CompositeVideoClip([
            background_video,
            video
        ])

        # I add frame_duration * 0.1 to make sure it fits the
        # next index
        video = video.resized(lambda t: resizes[int((t + frame_duration * 0.1) // frame_duration)])
        if positions:
            video = video.with_position(lambda t: positions[int((t + frame_duration * 0.1) // frame_duration)])
        if rotated:
            video = video.rotated(lambda t: rotations[int((t + frame_duration * 0.1) // frame_duration)])
        
        return video
        
    # TODO: This below is being tested
    @staticmethod
    def get_arrays(
        number_of_frames: int,
        with_position: Union[WithPositionArgument, None] = None,
        resized: Union[ResizedArgument, None] = None,
        rotated: Union[RotatedArgument, None] = None
    ):
        """
        Return the calculated arrays for the given 'with_position',
        'resized' and 'rotated' parameters as array of values that
        can be mixed directly with the SubClip base values.

        Each of those arrays can be None if it is not affected by
        the effect.
        """
        if with_position is None and resized is None and rotated is None:
            return None, None, None
        
        resized = (
            resized.get_values(number_of_frames)
            if resized is not None else
            None
        )
        # TODO: TFunctionSetPosition has not only a rate function
        # for the path but also a function to apply some movement
        # meanwhile it goes from A to B
        with_position = (
            with_position.get_values(number_of_frames)
            if with_position is not None else
            None
        )
        rotated = (
            rotated.get_values(number_of_frames)
            if rotated is not None else
            None
        )

        return with_position, resized, rotated
    
class MoviepyWithPrecalculated:
    """
    Class to encapsulate the 'resized', 'with_position' and
    'rotated' functionality and to be able to make one depend
    on the other by the pre-calculated values provided and
    then using them when positioning, resizing and rotating.

    This class is just to apply the 'with_position', 'resized'
    and 'rotated' moviepy basic effects that must have been
    pre-calculated and passed as a list to be applied for each
    video frame.

    This class is useful when you want to pre-calculate your
    values by a custom function and not only a basic TFuntion
    available through the MoviepyWithArgument class.
    """

    @staticmethod
    def apply(
        video: Clip,
        with_position_list: Union[list, None] = None,
        resized_list: Union[list, None] = None,
        rotated_list: Union[list, None] = None
    ):
        """
        Apply the property effects on the provided 'video'. This
        method will use the provided 'background_video' and 
        recalculate the position according to it.

        Background can be different to default scene of 1920x1080
        so positions will be adjusted to it.

        :param list with_position: The list of pre-calculated positions to apply.

        :param list resized: The list of pre-calculated resizes to apply.

        :param list rotated: The list of pre-calculated rotation effect to apply.
        """
        return MoviepyWithPrecalculated.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration, fps = video.fps), with_position_list, resized_list, rotated_list)

    @staticmethod
    def apply_over_video(
        video: Clip,
        background_video: Clip,
        with_position_list: Union[list, None] = None,
        resized_list: Union[list, None] = None,
        rotated_list: Union[list, None] = None
    ):
        video = VideoParser.to_moviepy(video, do_include_mask = True)
        background_video = VideoParser.to_moviepy(background_video, True)
        
        # Prepare data for pre-calculations
        video_handler = MPVideo(video)
        
        background_video = video_handler.prepare_background_clip(background_video)

        # Validate provided lists
        if (
            resized_list is not None and
            len(resized_list) != video_handler.number_of_frames
        ):
            raise Exception(f'The provided "resized_list" contains {str(len(resized_list))} elements and there are "{str(video_handler.number_of_frames)} frames.')
        
        if (
            with_position_list is not None and
            len(with_position_list) != video_handler.number_of_frames
        ):
            raise Exception(f'The provided "with_position_list" contains {str(len(with_position_list))} elements and there are "{str(video_handler.number_of_frames)} frames.')
        
        if (
            rotated_list is not None and
            len(rotated_list) != video_handler.number_of_frames
        ):
            raise Exception(f'The provided "rotated_list" contains {str(len(rotated_list))} elements and there are "{str(video_handler.number_of_frames)} frames.')
        
        # TODO: Remove this comment below if nothing else 
        # commented below that comment
        # I add frame_duration * 0.1 to make sure it fits the

        # next index
        video = (
            #video = video.resized(lambda t: resized_list[video_handler.get_frame_number_by_time_moment(t)])
            video.resized(lambda t: resized_list[video_handler.frame_time_to_frame_index(t, video_handler.fps)])
            #video = video.resized(lambda t: resized_list[int((t + frame_duration * 0.1) // frame_duration)])
            if resized_list is not None else
            video
        )

        video = (
            video.with_position(lambda t: with_position_list[video_handler.frame_time_to_frame_index(t, video_handler.fps)])
            #video = video.with_position(lambda t: with_position_list[int((t + frame_duration * 0.1) // frame_duration)])
            if with_position_list is not None else
            video
        )

        video = (
            video.rotated(lambda t: rotated_list[video_handler.frame_time_to_frame_index(t, video_handler.fps)])
            #video = video.rotated(lambda t: rotated_list[int((t + frame_duration * 0.1) // frame_duration)])
            if rotated_list is not None else
            video
        )
        
        return CompositeVideoClip([
            background_video,
            video
        ])

