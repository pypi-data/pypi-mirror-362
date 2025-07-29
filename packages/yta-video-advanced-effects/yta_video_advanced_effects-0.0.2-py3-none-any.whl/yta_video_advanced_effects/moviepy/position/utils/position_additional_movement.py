from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from random import randint
from abc import abstractmethod
from math import pi

import numpy as np


class PositionAdditionalMovement: 
    """
    The additional movement that can be added to
    an element in a position. This will move the
    element in some way but in the position in
    what it is.
    """

    @abstractmethod
    def get_position(
        self
    ):
        """
        Obtain the position on the given 'n' moment of
        the movement ('n' value must be a normalized
        value between 0 and 1 representing the amount
        of movement done for the moment to be
        calculated where 0 is the start and 1 the end).
        """
        pass

class ShakeAdditionalMovement(PositionAdditionalMovement):
    """
    Make the element shake at the same speed in
    the position it is.
    """

    def __init__(
        self,
        shake_speed: int = 4
    ):
        self.shake_speed = (
            4
            if shake_speed is None else
            shake_speed
        )

    def get_position(
        self,
        position: tuple[int, int],
    ):
        return shake(position, self.shake_speed)
    
class ShakeIncreasingAdditionalMovement(PositionAdditionalMovement):
    """
    Make the element shake in an increasing speed
    in the position it is.
    """

    def __init__(
        self,
        shake_speed: int = 4
    ):
        self.shake_speed = (
            4
            if shake_speed is None else
            shake_speed
        )

    def get_position(
        self,
        n: float,
        position: tuple[int, int],
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return shake_increasing(position, self.shake_speed, n, rate_function)
    
class ShakeDecreasingAdditionalMovement(PositionAdditionalMovement):
    """
    Make the element shake in a decreasing speed
    in the position it is.
    """

    def __init__(
        self,
        shake_speed: int = 4
    ):
        self.shake_speed = (
            4
            if shake_speed is None else
            shake_speed
        )

    def get_position(
        self,
        n: float,
        position: tuple[int, int],
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return shake_decreasing(position, self.shake_speed, n, rate_function)
        
class CirclesAdditionalmovement(PositionAdditionalMovement):
    """
    Make the element move in circles around the
    position in which it is.
    """
    
    def __init__(
        self,
        time_per_circle: float = 1,
        radius: int = 200
    ):
        self.time_per_circle = (
            1
            if time_per_circle is None else
            time_per_circle
        )
        self.radius = (
            200
            if radius is None else
            radius
        )

    def get_position(
        self,
        n: float,
        position: tuple[int, int],
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return circles(position, self.time_per_circle, self.radius, n, rate_function)

# TODO: Remove this in the next commit
# class AdditionalMovement(Enum):
#     """
#     The additional movement that can be added to
#     an element in a position. This will move the
#     element in some way but in the position in
#     what it is.
#     """

#     SHAKE = 'shake'
#     """
#     Make the element shake at the same speed in
#     the position it is.
#     """
#     SHAKE_INCREASING = 'shake_increasing'
#     """
#     Make the element shake in an increasing speed
#     in the position it is.
#     """
#     SHAKE_DECREASING = 'shake_decreasing'
#     """
#     Make the element shake in a decreasing speed
#     in the position it is.
#     """

#     def get_function(self):
#         """
#         Obtain the function to calculate the value of
#         the given 'n'. This function can be called by
#         providing the 'n' value and any other needed
#         key parameter.
#         """
#         return {
#             self.SHAKE: shake,
#             self.SHAKE_INCREASING: shake_increasing_movement,
#             self.SHAKE_DECREASING: shake_decreasing_movement
#         }[self]

#     def apply(self, n: float, **kwargs) -> float:
#         """
#         Apply the additional movement to the given 'n'
#         and kwargs.

#         The 'n' parameter must be a normalized value
#         (a value between 0 and 1).

#         The result will be the corresponding 'y' 
#         value for the given 'n' value.
#         """
#         if not NumberValidator.is_number_between(n, 0, 1):
#             raise Exception('The additional movement has been built to work with an "n" value between 0 and 1.')

#         return self.get_function()(n, **kwargs)

"""
        In place movements (static) effect position functions below
"""
def shake(
    position: tuple[int, int],
    shake_speed: int
):
    """
    Creates a shake effect on the given 'position',
    by moving the element in a random position,
    that is constant during the time.

    The 'shake_speed' is the amount of pixels to
    move in each movement. The value 4 is a good
    value.

    The 'n' parameter must be a normalized value
    between 0 and 1 representing the amount of
    animation that has been processed until the
    moment in which this method is executed.
    """
    # TODO: I think this is increasing also not a
    # constant shaking movement because of the *
    #shake_speed *= n
    # TODO: Use our own Random class
    direction = randint(0, 4)

    return {
        0: (position[0], position[1] + shake_speed),    # top
        1: (position[0] - shake_speed, position[1]),    # left
        2: (position[0], position[1] - shake_speed),    # right
        3: (position[0] + shake_speed, position[1])     # bottom
    }[direction]

def shake_increasing(
    position: tuple[int, int],
    shake_speed: int,
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    """
    Creates a shake effect on the given 'position',
    by moving the element in a random position, 
    that is being increased during the animation.

    The 'shake_speed' is the amount of pixels to
    move in each movement. The value 4 is a good
    value.

    The 'n' parameter must be a normalized value
    between 0 and 1 representing the amount of
    animation that has been processed until the
    moment in which this method is executed.
    """
    shake_speed *= rate_function.get_n_value(n)
    
    return shake(position, shake_speed)

def shake_decreasing(
    position: tuple[int, int],
    shake_speed: int,
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    """
    Creates a shake effect on the given 'position',
    by moving the element in a random position, 
    that is being decreased during the animation.

    The 'shake_speed' is the amount of pixels to
    move in each movement. The value 4 is a good
    value.

    The 'n' parameter must be a normalized value
    between 0 and 1 representing the amount of
    animation that has been processed until the
    moment in which this method is executed.
    """
    shake_speed *= 1 - rate_function.get_n_value(n)
    
    return shake(position, shake_speed)

def circles(
    position: tuple[int, int],
    time_per_circle: float,
    radius: int,
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    """
    Returns the (x, y) position tuple for the moviepy '.with_position()' effect,
    for each 't' provided, that will make the element move in circles with the
    provided 'radius'. The 'radius' parameter is the distance between the origin
    and the path the clip will follow. The 'cicle_time' is the time (in seconds)
    needed for a complete circle to be completed by the movement.

    If you provide the video duration as 'cicle_time', the video will make only
    one whole circle
    """
    circle_factor = rate_function.get_n_value(n) % time_per_circle

    return position[0] + radius * np.cos((circle_factor) * 2 * pi), position[1] + radius * np.sin((circle_factor) * 2 * pi)