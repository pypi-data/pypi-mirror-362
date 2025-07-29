from yta_constants.enum import YTAEnum as Enum
from abc import ABC, abstractmethod
from typing import Tuple, Union

import numpy as np


FRAMES_TO_CHECK = 2
"""
The amount of frames we use to check what arrays
are being affected by the effect.
"""

# TODO: Move this class to its own file
class SEffectType(Enum):
    """
    Type of SEffects that we are able to handle, useful to
    recognize if we are trying to apply two (or more) 
    effects of the same type and use only one of them.

    TODO: I don't know how to indicate the type correctly
    so I can decide I'm only able to use one of that type.
    """
    GENERAL = 'general'
    """
    I don't know which type is this effect and I'm not
    blocking it.
    """
    MOVEMENT = 'movement'
    """
    Effect that only affects to 'with_position' array.
    """

class SEffect(ABC):
    """
    Class to apply and effect and return its 'with_position',
    'rotated' and 'resized' parameters.

    This class must be implemented by any specific and 
    custom effect that applies to a SubClip instance.
    """
    type: SEffectType = None
    """
    The type of the effect.
    """
    _number_of_frames: int = None
    _values: tuple[list, list, list, list] = None
    """
    The array containing the 4 arrays of values that have
    been calculated in a previous iteration. These values
    are stored to avoid recalculating them.
    """

    def __init__(
        self,
        number_of_frames: int,
        type: SEffectType = SEffectType.GENERAL,
        *args,
        **kwargs
    ):
        type = SEffectType.to_enum(type)

        self._number_of_frames = number_of_frames
        self._values = None
        self.type = type
        self.args = args
        self.kwargs = kwargs

    @property
    def number_of_frames(
        self
    ):
        return self._number_of_frames
    
    @number_of_frames.setter
    def number_of_frames(
        self,
        value: int
    ):
        """
        Set the number of frames, useful if we need to
        recalculate the values according to this new
        value. This method will force the effect values
        to be recalculated.
        """
        # TODO: Validate (?)
        self._number_of_frames = value
        # We reset the values so they have to be calculated
        # again due to 'number_of_frames' change that makes
        # them different from the previous calculation
        self._values = None

    @property
    def do_affect_frames(
        self
    ) -> bool:
        """
        Return True if the effect affects to the 'frames'
        array or not.
        """
        return self.calculate(FRAMES_TO_CHECK, *self.args, **self.kwargs)[0] is not None

    @property
    def do_affect_with_position(
        self
    ) -> bool:
        """
        Return True if the effect affects to the 'with_position'
        array or not.
        """
        return self.calculate(FRAMES_TO_CHECK, *self.args, **self.kwargs)[1] is not None

    @property
    def do_affect_resized(
        self
    ) -> bool:
        """
        Return True if the effect affects to the 'resized'
        array or not.
        """
        return self.calculate(FRAMES_TO_CHECK, *self.args, **self.kwargs)[2] is not None

    @property
    def do_affect_rotated(
        self
    ) -> bool:
        """
        Return True if the effect affects to the 'rotated'
        array or not.
        """
        return self.calculate(FRAMES_TO_CHECK, *self.args, **self.kwargs)[3] is not None

    @property
    def values(
        self
    ) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 4 arrays 'frames',
        'with_position', 'resized', and 'rotated' and return
        each of them if affected, or None if not.
        """
        self._values = (
            self.calculate(self.number_of_frames, *self.args, **self.kwargs)
            if self._values is None else
            self._values
        )

        return self._values
    
    @staticmethod
    @abstractmethod
    def calculate(
        number_of_frames: int,
        *args,
        **kwargs
    ) -> Tuple[Union[list[np.ndarray], None], Union[list[int, int], None], Union[list[float, float], None], Union[int, None]]:
        """
        Calculate the values for the 4 arrays:
         
        - frames
        - with_position
        - resized
        - rotated
        
        with the provided 'number_of_frames' and
        additional arguments and return each of
        them if affected, or None if not.
        """
        return (
            None,
            None,
            None,
            None
        )