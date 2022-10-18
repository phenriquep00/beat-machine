import pygame
from classes.colors import Colors
from classes.fonts import Fonts
from utils.constants import *


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

        self.hi_hat_text = self.FONTS.label_font.render('High Hat', True, self.colors[actives[0]])
        self.snare_text = self.FONTS.label_font.render('Snare', True, self.colors[actives[1]])
        self.kick_text = self.FONTS.label_font.render('Bass Drum', True, self.colors[actives[2]])
        self.crash_text = self.FONTS.label_font.render('Crash', True, self.colors[actives[3]])
        self.clap_text = self.FONTS.label_font.render('Clap', True, self.colors[actives[4]])
        self.high_tom_text = self.FONTS.label_font.render('High Tom', True, self.colors[actives[5]])

        self.instruments = [
            self.hi_hat_text, self.snare_text, self.kick_text, self.crash_text, self.clap_text, self.high_tom_text
        ]
        self.beats = 8

    def draw(self):
        for _ in self.instruments:
            self.surf.blit(_, (30, (self.instruments.index(_) * 100) + 30))

        for i in range(len(self.instruments)):
            pygame.draw.line(self.surf, self.COLORS.gray, (0, (i * 100) + 100), (198, (i * 100) + 100), 3)

        for i in range(self.beats):
            for j in range(len(self.instruments)):
                if self.clicks[j][i] == -1:
                    color = self.COLORS.gray
                else:
                    if self.actives[j] == 1:
                        color = self.COLORS.green
                    else:
                        color = self.COLORS.dark_gray
                rect = pygame.draw.rect(self.surf, color,
                                        [i * ((WIDTH - 200) // self.beats) + 205, (j * 100) + 5,
                                         ((WIDTH - 200) // self.beats) - 10,
                                         90], 0, 3)
                pygame.draw.rect(self.surf, self.COLORS.gold,
                                 [i * ((WIDTH - 200) / self.beats) + 200, (j * 100), ((WIDTH - 200) // self.beats),
                                  ((HEIGHT - 200) // len(self.instruments))], 5, 5)
                pygame.draw.rect(self.surf, self.COLORS.black,
                                 [i * ((WIDTH - 200) / self.beats) + 200, (j * 100), ((WIDTH - 200) // self.beats),
                                  ((HEIGHT - 200) // len(self.instruments))], 2, 5)
                self.boxes.append((rect, (i, j)))

            active = pygame.draw.rect(self.surf, self.COLORS.blue, [self.beat * ((WIDTH - 200) / self.beats) + 200, 0, ((WIDTH - 200) // self.beats),
                                                     len(self.instruments) * 100], 5, 3)
