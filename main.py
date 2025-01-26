import pygame
import sys
import os
import random
from db.datab import init_db, save_score, get_scores


def start_screen():
    start_bg_path = 'images/startwindow.png'
    if not os.path.exists(start_bg_path):
        print(f"Файл '{start_bg_path}' не найден. Убедитесь, что он находится в директории:", os.getcwd())
        sys.exit()

    start_bg = pygame.image.load(start_bg_path)
    start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_path = 'font/flappy_font.ttf'
    try:
        title_font = pygame.font.Font(font_path, 72)
        subtitle_font = pygame.font.Font(font_path, 30)
        input_font = pygame.font.Font(font_path, 24)
    except FileNotFoundError:
        print(f"Шрифт '{font_path}' не найден. Используется системный шрифт.")
        title_font = pygame.font.SysFont('Arial', 72)
        subtitle_font = pygame.font.SysFont('Arial', 30)
        input_font = pygame.font.SysFont('Arial', 24)

    title_text = title_font.render('Flappy bird', True, (255, 255, 255))
    subtitle_text = subtitle_font.render('by zhenikh and koykan', True, (255, 255, 255))

    button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2), (150, 50))
    button_color = (50, 150, 250)
    button_text = subtitle_font.render('Start Game', True, (255, 255, 255))

    difficulty_button_rect_easy = pygame.Rect((SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 70), (150, 50))
    difficulty_button_text_easy = subtitle_font.render('Easy', True, (255, 255, 255))
    difficulty_button_rect_hard = pygame.Rect((SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 130), (150, 50))
    difficulty_button_text_hard = subtitle_font.render('Hard', True, (255, 255, 255))

    player_name_input = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 50, 150, 30)
    player_name_text = ''

    difficulty = 'easy'

    while True:
        for v in pygame.event.get():
            if v.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if v.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(v.pos):
                    return player_name_text, difficulty
                if difficulty_button_rect_easy.collidepoint(v.pos):
                    difficulty = 'easy'
                if difficulty_button_rect_hard.collidepoint(v.pos):
                    difficulty = 'hard'

            if v.type == pygame.KEYDOWN:
                if v.key == pygame.K_BACKSPACE:
                    player_name_text = player_name_text[:-1]
                elif v.key == pygame.K_RETURN:
                    return player_name_text, difficulty
                elif len(player_name_text) < 15:
                    player_name_text += v.unicode

        screen.blit(start_bg, (0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        subtitle_rect = subtitle_text.get_rect(midtop=(title_rect.right, title_rect.bottom + 5))
        screen.blit(subtitle_text, subtitle_rect)

        pygame.draw.rect(screen, button_color, button_rect)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.draw.rect(screen, button_color, difficulty_button_rect_easy)
        pygame.draw.rect(screen, button_color, difficulty_button_rect_hard)
        screen.blit(difficulty_button_text_easy, difficulty_button_rect_easy)
        screen.blit(difficulty_button_text_hard, difficulty_button_rect_hard)

        pygame.draw.rect(screen, (255, 255, 255), player_name_input, 2)
        name_surface = input_font.render(player_name_text, True, (255, 255, 255))
        screen.blit(name_surface, (player_name_input.x + 5, player_name_input.y + 5))

        pygame.display.flip()
        clock.tick(fps)


def update_game(st):
    global status, boost, speed, position_y, time, running, old_pipes
    global RETURN_SPEED, BIRD_LIVES, BIRD_POINTS, PIPES_SPEED

    if st == 'beginning':
        position_y += RETURN_SPEED * ((SCREEN_HEIGHT / 2.5) - position_y)
        bird.y = position_y
        if len(pipes) == 0:
            if time == 0 and mouse:
                status = 'playing'

    elif st == 'falling':
        falling_sound.play()
        BIRD_LIVES -= 1
        boost = 0
        speed = 0
        if BIRD_LIVES == 0:
            status = 'end'
        else:
            status = 'beginning'
        time = 0

    elif st == 'playing':
        position_y += speed
        bird.y = position_y

        if mouse:
            boost = JUMP_POWER
        else:
            boost = 0

        pipe_position = SCREEN_WIDTH - PIPES_DISTANCE
        if (len(pipes) == 0) or (pipe_position > pipes[-1].x):
            pipe_high_height = random.randint(100, SCREEN_HEIGHT // 2)
            pipe_low_height = random.randint(100, SCREEN_HEIGHT // 2)
            pipe_high = pygame.Rect(SCREEN_WIDTH, 0, PIPES_WIDTH, pipe_high_height)
            pipe_low = pygame.Rect(SCREEN_WIDTH, pipe_high.bottom + PIPES_DISTANCE, PIPES_WIDTH, pipe_low_height)
            pipes.append(pipe_high)
            pipes.append(pipe_low)

        for x in pipes:
            if bird.colliderect(x):
                status = 'falling'
            if x not in old_pipes:
                if x.right < bird.left:
                    BIRD_POINTS += (PIPE_POINTS // 2)
                    old_pipes.append(x)

        if (bird.bottom > SCREEN_HEIGHT) or (bird.top < 0):
            status = 'falling'
        speed = BIRD_GRAVITY * (1 + (boost + speed))

    elif st == 'end':
        if time == 0:
            running = False


if __name__ == '__main__':
    pygame.init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Flappy Animal')
    font = pygame.font.Font(None, 40)
    fps = 40
    dt = 0
    JUMP_POWER = -3
    BIRD_GRAVITY = 0.95
    RETURN_SPEED = 0.15
    PIPES_WIDTH = 150
    PIPES_SPEED = 7
    PIPES_DISTANCE = 180

    bird_image1 = pygame.image.load('images/bird_image1.png')
    bird_image1 = pygame.transform.scale(bird_image1, (35, 25))
    bird_image2 = pygame.image.load('images/bird_image2.png')
    bird_image2 = pygame.transform.scale(bird_image2, (35, 25))
    bird_image3 = pygame.image.load('images/bird_image3.png')
    bird_image3 = pygame.transform.scale(bird_image3, (35, 25))

    background_image = pygame.image.load('images/background_image.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pipe_high_image = pygame.image.load('images/pipe_low_image.png')
    pipe_high_image = pygame.transform.scale(pipe_high_image, (PIPES_WIDTH, 200))
    pipe_high_image.set_colorkey((255, 255, 255))

    pipe_low_image = pygame.image.load('images/pipe_high_image.png')
    pipe_low_image = pygame.transform.scale(pipe_low_image, (PIPES_WIDTH, 200))
    pipe_low_image.set_colorkey((255, 255, 255))

    falling_sound = pygame.mixer.Sound('sounds/falling_sound.mp3')
    flopping_sound = pygame.mixer.Sound('sounds/flopping_sound.mp3')
    pygame.mixer.music.load('sounds/game_music.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)

    clock = pygame.time.Clock()
    running = True

    position_x = SCREEN_WIDTH / 8
    position_y = SCREEN_HEIGHT / 2.5
    bird_form = 1
    flopping_speed = 2
    time = 0
    speed = 0
    boost = 0

    status = 'beginning'
    bird = pygame.Rect(position_x, position_y, 35, 25)

    BIRD_LIVES = 2
    BIRD_POINTS = 0
    PIPE_CENTER = SCREEN_HEIGHT // 2
    PIPE_POINTS = 10

    pipes = []
    old_pipes = []

    init_db()
    player_name, difficulty = start_screen()

    if difficulty == 'hard':
        BIRD_LIVES = 1
        PIPE_POINTS = 20
        PIPES_SPEED = 9
        PIPES_DISTANCE = 150
        PIPES_HEIGHT = 300

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if time > 0:
            time -= 1

        k = len(pipes) - 1
        for j in range(k, -1, -1):
            i = pipes[j]
            i.x -= PIPES_SPEED
            if i.right < 0:
                if i in old_pipes:
                    old_pipes.remove(i)
                pipes.remove(i)

        bird_form = (flopping_speed + bird_form) % 4

        mouse = pygame.mouse.get_pressed()[0]
        update_game(status)
        screen.blit(background_image, (0, 0))

        for i in pipes:
            if i.y == 0:
                screen.blit(pipe_low_image, i)
            else:
                screen.blit(pipe_high_image, i)

        if bird_form == 1:
            screen.blit(bird_image1, bird)
        elif bird_form == 2:
            screen.blit(bird_image2, bird)
        elif bird_form == 3:
            screen.blit(bird_image3, bird)

        lives = font.render('lives: ' + str(BIRD_LIVES), 1, 'black')
        points = font.render('points: ' + str(BIRD_POINTS), 1, 'black')
        screen.blit(lives, (SCREEN_WIDTH - 100, 10))
        screen.blit(points, (10, 10))

        pygame.display.flip()
        dt = clock.tick(fps)
    pygame.quit()
