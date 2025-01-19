import pygame


def update_game(st):
    global status, boost, speed, position_y, RETURN_SPEED

    if st == 'beginning':
        position_y += RETURN_SPEED * ((SCREEN_HEIGHT / 2.5) - position_y)
        bird.y = position_y
        if len(pipes) == 0:
            if time == 0 and mouse:
                status = 'playing'

    elif st == 'falling':
        status = 'beginning'
        boost = 0
        speed = 0

    elif st == 'playing':
        position_y += speed
        bird.y = position_y

        if mouse:
            boost = JUMP_POWER
        else:
            boost = 0

        pipe_position = SCREEN_WIDTH - PIPES_DISTANCE
        if (len(pipes) == 0) or (pipe_position > pipes[-1].x):
            pipes.append(pygame.Rect(SCREEN_WIDTH, 400, PIPES_WIDTH, 200))
            pipes.append(pygame.Rect(SCREEN_WIDTH, 0, PIPES_WIDTH, 200))

        for x in pipes:
            if bird.colliderect(x):
                status = 'falling'

        if (bird.bottom > SCREEN_HEIGHT) or (bird.top < 0):
            status = 'falling'
        speed = BIRD_GRAVITY * (1 + (boost + speed))


if __name__ == '__main__':
    pygame.init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Flappy animal')
    fps = 30
    dt = 0
    JUMP_POWER = -3
    BIRD_GRAVITY = 0.95
    RETURN_SPEED = 0.15
    PIPES_WIDTH = 60
    PIPES_SPEED = 7
    PIPES_DISTANCE = 180
    bird_image1 = pygame.image.load('images/bird_image1.png')
    bird_image1 = pygame.transform.scale(bird_image1, (35, 25))
    bird_image1 = bird_image1.subsurface(0, 0, 35, 25)
    bird_image2 = pygame.image.load('images/bird_image2.png')
    bird_image2 = pygame.transform.scale(bird_image2, (35, 25))
    bird_image2 = bird_image2.subsurface(0, 0, 35, 25)
    bird_image3 = pygame.image.load('images/bird_image3.png')
    bird_image3 = pygame.transform.scale(bird_image3, (35, 25))
    bird_image3 = bird_image3.subsurface(0, 0, 35, 25)
    background_image = pygame.image.load('images/background_image.jpg')
    pipe_high_image = pygame.image.load('images/pipe_high_image.png')
    pipe_low_image = pygame.image.load('images/pipe_low_image.png')

    clock = pygame.time.Clock()
    running = True

    position_x = SCREEN_WIDTH / 8
    position_y = SCREEN_HEIGHT / 2.5
    bird_form = 1
    flopping_speed = 2
    time = 5
    speed = 0
    boost = 0

    status = 'beginning'
    bird = pygame.Rect(position_x, position_y, 35, 25)

    pipes = []

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
                pipes.remove(i)

        bird_form = (flopping_speed + bird_form) % 4

        mouse = pygame.mouse.get_pressed()[0]
        update_game(status)
        screen.fill('green')

        for i in pipes:
            pygame.draw.rect(screen, 'black', i)

        if bird_form == 1:
            screen.blit(bird_image1, bird)
        elif bird_form == 2:
            screen.blit(bird_image2, bird)
        elif bird_form == 3:
            screen.blit(bird_image3, bird)

        pygame.display.flip()
        dt = clock.tick(fps)
    pygame.quit()
