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
active_beat = 1
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


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, COLORS.gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, COLORS.gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [COLORS.gray, COLORS.white, COLORS.gray]
    hi_hat_text = label_font.render('High Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    hi_hat_text = label_font.render('High Tom', True, colors[actives[5]])
    screen.blit(hi_hat_text, (30, 530))

    for i in range(instruments):
        pygame.draw.line(screen, COLORS.gray, (0, (i * 100) + 100), (198, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = COLORS.gray
            else:
                if actives[j] == 1:
                    color = COLORS.green
                else:
                    color = COLORS.dark_gray
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     90], 0, 3)
            pygame.draw.rect(screen, COLORS.gold,
                             [i * ((WIDTH - 200) / beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, COLORS.black,
                             [i * ((WIDTH - 200) / beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                                            ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, COLORS.blue, [beat * ((WIDTH - 200) / beats) + 200, 0, ((WIDTH - 200) // beats),
                                  instruments * 100], 5, 3)
    return boxes


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, COLORS.black, (0, 0, WIDTH, HEIGHT))
    menu_text = label_font.render('SAVE MENU: Enter a name for the current beat', True, COLORS.white)
    saving_btn = pygame.draw.rect(screen, COLORS.gray, [WIDTH // 2 - 200, HEIGHT * .75, 400, 100], 0, 5)
    saving_text = label_font.render('Save Beat', True, COLORS.white)
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * .75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, COLORS.gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, COLORS.white)
    screen.blit(exit_text, (WIDTH - 180, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, COLORS.dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, COLORS.gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, COLORS.white)
    screen.blit(entry_text, (430, 250))

    return exit_btn, saving_btn, entry_rect


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, COLORS.black, (0, 0, WIDTH, HEIGHT))
    menu_text = label_font.render('LOAD MENU: Select a beat to load', True, COLORS.white)
    loading_btn = pygame.draw.rect(screen, COLORS.gray, [WIDTH // 2 - 200, HEIGHT * .87, 400, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, COLORS.white)
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * .87 + 30))
    screen.blit(menu_text, (400, 40))
    delete_btn = pygame.draw.rect(screen, COLORS.gray, [WIDTH//2 - 500, HEIGHT * .87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete beat', True, COLORS.white)
    screen.blit(delete_text, (WIDTH//2 - 485, HEIGHT * .87 + 30))
    exit_btn = pygame.draw.rect(screen, COLORS.gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, COLORS.white)
    screen.blit(exit_text, (WIDTH - 180, HEIGHT - 70))
    loaded_rectangle = pygame.draw.rect(screen, COLORS.gray, [190, 90, 1000, 600], 5, 5)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, COLORS.light_gray, [190, 100 + index*50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, COLORS.white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start: name_index_end], True, COLORS.white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8 : beat_index_end])
            bpm_index_end = saved_beats[beat].index(', selected:')
            loaded_bpm = int(saved_beats[beat][beat_index_end + 6 : bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split('], ['))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row =  (loaded_clicks_rows[row]).split(', ')
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    return exit_btn, loading_btn, delete_btn, loaded_rectangle, loaded_info


run = True
grid = Grid(screen, clicked, active_beat, active_list)

while run:
    timer.tick(fps)
    screen.fill(COLORS.black)

    grid.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()
