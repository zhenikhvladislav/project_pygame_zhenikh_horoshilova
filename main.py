import pygame
import csv
import os
import time
import sys
from db.datab import add_player, update_player


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
    help_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 200, 150, 50)

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
        pygame.draw.rect(screen, (100, 100, 250), help_button)

        easy_text = button_font.render("Easy", True, WHITE)
        hard_text = button_font.render("Hard", True, WHITE)
        exit_text = button_font.render("Exit", True, WHITE)
        help_text = button_font.render("Help", True, WHITE)

        screen.blit(easy_text, easy_button.move(50, 10).topleft)
        screen.blit(hard_text, hard_button.move(50, 10).topleft)
        screen.blit(exit_text, exit_button.move(50, 10).topleft)
        screen.blit(help_text, help_button.move(50, 10).topleft)

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
                if help_button.collidepoint(event.pos):
                    show_help_window()
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


def show_help_window():
    help_running = True
    help_screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Help")

    if not os.path.exists('images/background_image.jpg'):
        print("Ошибка: Файл background_image.jpg не найден!")
        return
    background = pygame.image.load('images/background_image.jpg')
    background = pygame.transform.scale(background, (600, 400))

    title_font = pygame.font.Font('font/flappy_font.ttf', 48) if os.path.exists(
        'font/flappy_font.ttf') else pygame.font.SysFont('Arial', 48)
    text_font = pygame.font.Font('font/arial.ttf', 18) if os.path.exists('font/arial.ttf') else pygame.font.SysFont(
        'Arial', 18)

    text_lines = [
        "Flappy Bird",
        "Controls:",
        "- SPACE or Mouse Click: Jump",
        "- Avoid pipes to score points",
        "- Select difficulty at the start",
        "GitHub: https://github.com/zhenikhvladislav/project_pygame_zhenikh_horoshilova"
    ]

    while help_running:
        help_screen.blit(background, (0, 0))
        title_surface = title_font.render(text_lines[0], True, (255, 255, 255))
        help_screen.blit(title_surface, (50, 30))

        for i, line in enumerate(text_lines[1:]):
            text_surface = text_font.render(line, True, (255, 255, 255))
            help_screen.blit(text_surface, (50, 100 + i * 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                help_running = False

    pygame.display.set_mode((800, 600))

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
        title_font = pygame.font.Font(font_path, 100)
        flappy_font = pygame.font.Font(font_path, 36)
    else:
        title_font = pygame.font.SysFont('Arial', 100)
        flappy_font = pygame.font.SysFont('Arial', 36)

    arial_font = pygame.font.SysFont('Arial', 28)

    elapsed_time = round(time.time() - start_time, 2)
    best_score = get_best_score(player_name)
    money = score // 10

    exit_button = pygame.Rect(500, 500, 150, 50)
    new_game_button = pygame.Rect(150, 500, 150, 50)
    main_menu_button = pygame.Rect(325, 500, 150, 50)

    running = True
    while running:
        screen.blit(background, (0, 0))

        game_over_text = title_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 50))

        player_label = flappy_font.render("Player", True, (255, 255, 255))
        colon = arial_font.render(":", True, (255, 255, 255))
        player_name_text = flappy_font.render(player_name, True, (255, 255, 255))
        screen.blit(player_label, (250, 150))
        screen.blit(colon, (400, 150))
        screen.blit(player_name_text, (420, 150))

        score_label = flappy_font.render("Score", True, (255, 255, 255))
        score_text = arial_font.render(f": {score}", True, (255, 255, 255))
        screen.blit(score_label, (250, 200))
        screen.blit(score_text, (400, 200))

        best_label = flappy_font.render("Best", True, (255, 255, 255))
        best_text = arial_font.render(f": {best_score}", True, (255, 255, 255))
        screen.blit(best_label, (250, 250))
        screen.blit(best_text, (400, 250))

        time_label = flappy_font.render("Time", True, (255, 255, 255))
        time_text = arial_font.render(f": {elapsed_time}s", True, (255, 255, 255))
        screen.blit(time_label, (250, 300))
        screen.blit(time_text, (400, 300))

        money_label = flappy_font.render("Money", True, (255, 255, 255))
        money_text = arial_font.render(f": {money}", True, (255, 255, 255))
        screen.blit(money_label, (250, 350))
        screen.blit(money_text, (400, 350))

        pygame.draw.rect(screen, (50, 150, 250), new_game_button)
        pygame.draw.rect(screen, (50, 150, 250), main_menu_button)
        pygame.draw.rect(screen, (200, 50, 50), exit_button)

        new_game_text = flappy_font.render("New Game", True, (255, 255, 255))
        main_menu_text = flappy_font.render("Main Menu", True, (255, 255, 255))
        exit_text = flappy_font.render("Exit", True, (255, 255, 255))

        screen.blit(new_game_text, (new_game_button.x + 20, new_game_button.y + 10))
        screen.blit(main_menu_text, (main_menu_button.x + 10, main_menu_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 50, exit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if new_game_button.collidepoint(event.pos):
                    return "new_game"
                if main_menu_button.collidepoint(event.pos):
                    return "main_menu"

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


    def reset_game():
        global status, boost, speed, position_y, BIRD_LIVES, BIRD_POINTS, game_time, pipes, old_pipes
        status = 'beginning'
        boost = 0
        speed = 0
        position_y = SCREEN_HEIGHT / 2.5
        BIRD_LIVES = 2
        BIRD_POINTS = 0
        game_time = 0
        pipes.clear()
        old_pipes.clear()

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
            game_action = final_screen(player_name, BIRD_POINTS, difficulty, start_time)

            if game_action == "new_game":
                reset_game()
                continue

            elif game_action == "main_menu":
                player_name, difficulty = start_screen()
                reset_game()
                continue

            else:
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
