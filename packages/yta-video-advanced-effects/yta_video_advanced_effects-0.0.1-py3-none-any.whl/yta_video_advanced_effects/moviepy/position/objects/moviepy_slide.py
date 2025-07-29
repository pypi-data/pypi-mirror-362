from yta_multimedia.video.position import Position
from random import randrange


# TODO: Do I need this (?)
class MoviepySlide:

    # TODO: Maybe a list, not a class, or a property (?)
    @staticmethod
    def get_in_and_out_positions_as_list():
        """
        Returns a list of 2 elements containing the out edge from which
        the video will come into the screen, and the opposite edge to get
        out of the screen. This has been created to animate a random slide
        transition effect. The possibilities are horizontal, diagonal and
        vertical linear sliding transitions. The first element in the list
        is the initial position and the second one, the final position. 
        """
        return {
            0: [Position.OUT_RIGHT, Position.OUT_LEFT],
            1: [Position.OUT_TOP, Position.OUT_BOTTOM],
            2: [Position.OUT_BOTTOM, Position.OUT_TOP],
            3: [Position.OUT_TOP_LEFT, Position.OUT_BOTTOM_RIGHT],
            4: [Position.OUT_TOP_RIGHT, Position.OUT_BOTTOM_LEFT],
            5: [Position.OUT_BOTTOM_LEFT, Position.OUT_TOP_RIGHT],
            6: [Position.OUT_BOTTOM_RIGHT, Position.OUT_TOP_LEFT],
            7: [Position.OUT_LEFT, Position.OUT_RIGHT]
        }[randrange(0, 8)]