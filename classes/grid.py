import pygame
from classes.colors import Colors
from classes.fonts import Fonts


class Grid:
    def __init__(self, surf, clicks, beat, actives):
        self.surf = surf
        self.clicks = clicks
        self.beat = beat
        self.actives = actives

        self.COLORS = Colors()
        self.FONTS = Fonts()

        self.boxes = []
        self.colors = [self.COLORS.gray, self.COLORS.white, self.COLORS.gray]

    def draw(self):
        pass
