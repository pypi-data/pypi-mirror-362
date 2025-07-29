from yta_general_utils.math.rate_functions.rate_function_argument import RateFunctionArgument
from abc import abstractmethod

import numpy as np


class PositionMovement:
    """
    Handles a movement from the 'initial_position' to
    the 'final_position'
    """

    def __init__(
        self,
        initial_position: tuple[int, int],
        final_position: tuple[int, int]
    ):
        # TODO: Validate 'initial_position' is valid
        # TODO: Validate 'final_position' is valid

        self.initial_position = initial_position
        self.final_position = final_position

    @abstractmethod
    def get_position(
        self,
        n: float,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        """
        Obtain the position on the given 'n' moment of
        the movement ('n' value must be a normalized
        value between 0 and 1 representing the amount
        of movement done for the moment to be
        calculated where 0 is the start and 1 the end).
        """
        pass

class LinearPositionMovement(PositionMovement):
    """
    Handles a linear movement from the 'initial_position'
    to the 'final_position'.
    """

    def get_position(
        self,
        n: float,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return linear(self.initial_position, self.final_position, n, rate_function)
    
class SinusoidalPositionMovement(PositionMovement):
    """
    Handles a sinusoidal movement from the 'initial_position'
    to the 'final_position'.
    """

    def get_position(
        self,
        n: float,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return sinusoidal(self.initial_position, self.final_position, n, rate_function)
    
class ZigZagPositionMovement(PositionMovement):
    """
    Handles a zigzag movement from the 'initial_position'
    to the 'final_position'.
    """
    
    def get_position(
        self,
        n: float,
        rate_function: RateFunctionArgument = RateFunctionArgument.default()
    ):
        return zigzag(self.initial_position, self.final_position, n, rate_function) 

def linear(
    initial_position: tuple[int, int],
    final_position: tuple[int, int],
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    # TODO: Validate 'initial_position' is valid
    # TODO: Validate 'final_position' is valid
    
    # Obtain the real factor according to the rate function
    n = rate_function.get_n_value(n)

    return (
        initial_position[0] + (final_position[0] - initial_position[0]) * n,
        initial_position[1] + (final_position[1] - initial_position[1]) * n,
    )

def sinusoidal(
    initial_position: tuple,
    final_position: tuple,
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    # TODO: Validate 'initial_position' is valid
    # TODO: Validate 'final_position' is valid

    WAVE_AMPLITUDE = 100
    WAVE_FREQUENCY = 2

    # Obtain the real factor according to the rate function
    n = rate_function.get_n_value(n)

    return (
        initial_position[0] + n * (final_position[0] - initial_position[0]),
        initial_position[1] + n * (final_position[1] - initial_position[1]) + WAVE_AMPLITUDE * np.sin(2 * np.pi * WAVE_FREQUENCY * n)
    )

def zigzag(
    initial_position: tuple[int, int],
    final_position: tuple[int, int],
    n: float,
    rate_function: RateFunctionArgument = RateFunctionArgument.default()
):
    # TODO: Validate 'initial_position' is valid
    # TODO: Validate 'final_position' is valid

    AMPLITUDE = 15

    # Obtain the real factor according to the rate function
    n = rate_function.get_n_value(n)

    return (
        initial_position[0] + n * (final_position[0] - initial_position[0]),
        initial_position[1] + n * (final_position[1] - initial_position[1]) + AMPLITUDE * np.sin(10 * np.pi * n)
    )