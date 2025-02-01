import pygame
import csv
import os
import time
import sys


def start_screen():
    WHITE = (255, 255, 255)
    BLUE = (50, 150, 250)
    RED = (200, 50, 50)

    if not os.path.exists('images/startwindow.png'):
        print("Ошибка: Файл startwindow.png не найден!")
        return

    start_bg = pygame.image.load('images/startwindow.png')
    start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_path = 'font/flappy_font.ttf'
    if os.path.exists(font_path):
        title_font = pygame.font.Font(font_path, 72)
        subtitle_font = pygame.font.Font(font_path, 24)
        input_font = pygame.font.Font(font_path, 24)
        button_font = pygame.font.Font(font_path, 36)
    else:
        print(f"Шрифт '{font_path}' не найден. Используется Arial.")
        title_font = pygame.font.SysFont('Arial', 72)
        subtitle_font = pygame.font.SysFont('Arial', 24)
        input_font = pygame.font.SysFont('Arial', 24)
        button_font = pygame.font.SysFont('Arial', 36)

    player_name = ""
    difficulty = 'easy'
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 50, 150, 30)
    easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 20, 150, 50)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 80, 150, 50)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 140, 150, 50)

    title_text = title_font.render('Flappy Bird', True, WHITE)
    subtitle_text = subtitle_font.render('by zhenikh and koykan', True, WHITE)

    clock = pygame.time.Clock()

    while True:
        screen.blit(start_bg, (0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        subtitle_rect = subtitle_text.get_rect(midtop=(title_rect.right - 50, title_rect.bottom + 5))
        screen.blit(subtitle_text, subtitle_rect)

        pygame.draw.rect(screen, WHITE, input_box, 2)
        name_surface = input_font.render(player_name, True, WHITE)
        screen.blit(name_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, BLUE, easy_button)
        pygame.draw.rect(screen, BLUE, hard_button)
        pygame.draw.rect(screen, RED, exit_button)

        easy_text = button_font.render("Easy", True, WHITE)
        hard_text = button_font.render("Hard", True, WHITE)
        exit_text = button_font.render("Exit", True, WHITE)

        screen.blit(easy_text, easy_button.move(50, 10).topleft)
        screen.blit(hard_text, hard_button.move(50, 10).topleft)
        screen.blit(exit_text, exit_button.move(50, 10).topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN and player_name:
                    return player_name, difficulty
                elif len(player_name) < 15:
                    player_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if easy_button.collidepoint(event.pos) and player_name:
                    return player_name, "easy"
                if hard_button.collidepoint(event.pos) and player_name:
                    return player_name, "hard"

        clock.tick(40)


def update_game(st):
    global status, boost, speed, position_y, RETURN_SPEED, BIRD_LIVES, BIRD_POINTS, game_time, running, old_pipes

    if st == 'beginning':
        position_y += RETURN_SPEED * ((SCREEN_HEIGHT / 2.5) - position_y)
        bird.y = position_y
        if len(pipes) == 0:
            if game_time == 0 and mouse:
                status = 'playing'

    elif st == 'falling':
        BIRD_LIVES -= 1
        boost = 0
        speed = 0
        if BIRD_LIVES == 0:
            status = 'end'
        else:
            status = 'beginning'
        game_time = 0

    elif st == 'playing':
        position_y += speed
        bird.y = position_y

        if mouse:
            boost = JUMP_POWER
        else:
            boost = 0

        pipe_position = SCREEN_WIDTH - PIPES_DISTANCE
        if (len(pipes) == 0) or (pipe_position > pipes[-1].x):
            pipe_high = pygame.Rect(SCREEN_WIDTH, 400, PIPES_WIDTH, 200)
            pipe_low = pygame.Rect(SCREEN_WIDTH, 0, PIPES_WIDTH, 200)
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
        if game_time == 0:
            running = False

def get_best_score(player_name):
    file_path = 'files/records_table.csv'
    best_score = 0
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == player_name:
                    best_score = max(best_score, int(row[1]))
    return best_score


def final_screen(player_name, score, level, start_time):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Over")

    if not os.path.exists('images/final_screen.png'):
        print("Ошибка: Файл final_screen.png не найден!")
        return
    background = pygame.image.load('images/final_screen.png')
    background = pygame.transform.scale(background, (800, 600))

    font_path = 'font/flappy_font.ttf'
    if os.path.exists(font_path):
        title_font = pygame.font.Font(font_path, 72)
        text_font = pygame.font.Font(font_path, 36)
    else:
        title_font = pygame.font.SysFont('Arial', 72)
        text_font = pygame.font.SysFont('Arial', 36)

    elapsed_time = round(time.time() - start_time, 2)
    best_score = get_best_score(player_name)

    exit_button = pygame.Rect(300, 450, 200, 50)
    restart_button = pygame.Rect(300, 380, 200, 50)
    main_menu_button = pygame.Rect(300, 310, 200, 50)

    running = True
    while running:
        screen.blit(background, (0, 0))

        game_over_text = title_font.render("GAME OVER", True, (255, 255, 255))
        name_text = text_font.render(f"Player: {player_name}", True, (255, 255, 255))
        score_text = text_font.render(f"Score: {score}", True, (255, 255, 255))
        best_score_text = text_font.render(f"Best: {best_score}", True, (255, 255, 255))
        time_text = text_font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))

        screen.blit(game_over_text, (250, 100))
        screen.blit(name_text, (300, 200))
        screen.blit(score_text, (300, 240))
        screen.blit(best_score_text, (300, 280))
        screen.blit(time_text, (300, 320))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    pygame.quit()


start_time = time.time()

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
    game_time = 0
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

    player_name, difficulty = start_screen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_time > 0:
            game_time -= 1

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

        if status == 'end':
            final_screen(player_name, BIRD_POINTS, difficulty, start_time)
            break

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
