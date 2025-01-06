import pygame


def update_game(st):
    global status, boost, speed, position_y, RETURN_SPEED, BIRD_LIVES, BIRD_POINTS, time, running, old_pipes

    if st == 'beginning':
        position_y += RETURN_SPEED * ((SCREEN_HEIGHT / 2.5) - position_y)
        bird.y = position_y
        if len(pipes) == 0:
            if time == 0 and mouse:
                status = 'playing'

    elif st == 'falling':
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
        if time == 0:
            running = False


if __name__ == '__main__':
    pygame.init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Flappy animal')
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
    PIPE_POINTS = 10

    pipes = []
    old_pipes = []

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
