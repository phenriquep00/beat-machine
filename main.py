import pygame
from pygame import mixer

from classes.colors import Colors

pygame.init()


WIDTH = 1400
HEIGHT = 800

COLORS = Colors()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Drum Machine")
label_font = pygame.font.Font('freesansbold.ttf', 30)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

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
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
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

while run:
    timer.tick(fps)
    screen.fill(COLORS.black)

    boxes = draw_grid(clicked, active_beat, active_list)
    # lower buttons
    play_pause = pygame.draw.rect(screen, COLORS.gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, COLORS.white)
    screen.blit(play_text, (70, HEIGHT - 130))

    if playing:
        play_text2 = medium_font.render('Playing', True, COLORS.dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, COLORS.dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))

    # bpm
    bpm_rect = pygame.draw.rect(screen, COLORS.gray, [300, HEIGHT - 150, 220, 100], 5, 5)
    bpm_text = medium_font.render('Beats per Minute', True, COLORS.white)
    screen.blit(bpm_text, (308, HEIGHT - 130))

    bpm_text2 = label_font.render(f'{bpm}', True, COLORS.white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))

    bpm_add_rect = pygame.draw.rect(screen, COLORS.gray, [530, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sup_rect = pygame.draw.rect(screen, COLORS.gray, [530, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, COLORS.white)
    sub_text = medium_font.render('-5', True, COLORS.white)
    screen.blit(add_text, (540, HEIGHT - 140))
    screen.blit(sub_text, (540, HEIGHT - 90))

    # beats
    beats_rect = pygame.draw.rect(screen, COLORS.gray, [600, HEIGHT - 150, 220, 100], 5, 5)
    beats_text = medium_font.render('Beats in Loop', True, COLORS.white)
    screen.blit(beats_text, (628, HEIGHT - 130))

    beats_text2 = label_font.render(f'{beats}', True, COLORS.white)
    screen.blit(beats_text2, (700, HEIGHT - 100))

    beats_add_rect = pygame.draw.rect(screen, COLORS.gray, [830, HEIGHT - 150, 48, 48], 0, 5)
    beats_sup_rect = pygame.draw.rect(screen, COLORS.gray, [830, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, COLORS.white)
    sub_text2 = medium_font.render('-1', True, COLORS.white)
    screen.blit(add_text2, (840, HEIGHT - 140))
    screen.blit(sub_text2, (840, HEIGHT - 90))

    # instruments
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)

    # save/load
    save_button = pygame.draw.rect(screen, COLORS.gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, COLORS.white)
    screen.blit(save_text, (920, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, COLORS.gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, COLORS.white)
    screen.blit(load_text, (920, HEIGHT - 90))

    # clear board
    clear_button = pygame.draw.rect(screen, COLORS.gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear', True, COLORS.white)
    screen.blit(clear_text, (1200, HEIGHT - 110))

    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rect, loaded_info = draw_load_menu(index)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sup_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sup_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
                playing = False
            elif load_button.collidepoint(event.pos):
                load_menu = True
                playing = False
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            if load_menu:
                if loaded_rect.collidepoint(event.pos):
                    index = (event.pos[1] - 100) // 50
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_info[0]
                        bpm = loaded_info[1]
                        clicked = loaded_info[2]
                        index = 100
                        load_menu = False
            if save_menu:
                if entry_rectangle.collidepoint(event.pos):
                    if typing:
                        typing = False
                    elif not typing:
                        typing = True
                if saving_button.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w')
                    saved_beats.append(f'name: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    typing = False
                    beat_name = ''
                    playing = True

        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

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
