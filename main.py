import pygame
from pygame import mixer
from classes.colors import Colors
from classes.fonts import Fonts
from classes.grid import Grid
from utils.constants import *

pygame.init()
COLORS = Colors()
FONTS = Fonts()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Drum Machine")
label_font = FONTS.label_font
medium_font = FONTS.medium_font

index = 100
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]


bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

# load sounds
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.wav')
tom = mixer.Sound("sounds/tom.WAV")
pygame.mixer.set_num_channels(instruments * 3)
save_menu = False
load_menu = False
saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False


def play_notes():
    for _ in range(len(clicked)):
        if clicked[_][active_beat] == 1 and active_list[_] == 1:
            if _ == 0:
                hi_hat.play()
            if _ == 1:
                snare.play()
            if _ == 2:
                kick.play()
            if _ == 3:
                crash.play()
            if _ == 4:
                clap.play()
            if _ == 5:
                tom.play()


run = True
boxes = []

while run:
    timer.tick(fps)
    screen.fill(COLORS.black)
    grid = Grid(screen, clicked, active_beat, active_list, boxes)
    grid.draw()
    boxes = grid.return_boxes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    grid.event_handle()

    if beat_changed:
        play_notes()
        beat_changed = False

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True
    pygame.display.flip()
pygame.quit()
