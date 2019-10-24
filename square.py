import math
import random

moss_growth = 4


class Square():
    """
    a superclass for all types of squares
    """
    pass


class SquareUnfinished(Square):
    """
    a square that is just a place holder
    """
    pass


class SquareBiome(Square):
    """
    square with a biome type for starting highspots and lowspots
    """

    def __init__(self):
        biome = random.randrange(5)
        self.biome = biome


class SquareMoss(Square):
    """
    square with an amount of moss
    """

    def __init__(self, moss):
        self.moss = moss


class SquareDone(Square):
    """
    a finished square with starting moss and the rainfall
    """

    max_moss = 0

    def __init__(self, rainfall, moss):
        self.rainfall = rainfall
        self.moss = moss
        self.dying = 0

    def tick(self, speed):

        if self.dying > 0:
            self.dying -= 1
            self.moss -= math.sqrt(self.rainfall) / speed / moss_growth

        elif self.moss < SquareDone.max_moss:
            self.moss += math.sqrt(self.rainfall) / speed / moss_growth
            pass
        else:
            self.moss -= math.sqrt(self.rainfall) / speed / moss_growth
            self.dying = speed
