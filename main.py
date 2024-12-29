import pygame


def update_game(st):
    global status, boost, speed, position_y, RETURN_SPEED

    if st == 'beginning':
        position_y += RETURN_SPEED * ((SCREEN_HEIGHT / 2.5) - position_y)
        bird.y = position_y
        if mouse:
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

    clock = pygame.time.Clock()
    running = True

    position_x = SCREEN_WIDTH / 8
    position_y = SCREEN_HEIGHT / 2.5
    speed = 0
    boost = 0

    status = 'beginning'
    bird = pygame.Rect(position_x, position_y, 60, 60)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse = pygame.mouse.get_pressed()[0]
        update_game(status)

        screen.fill('green')
        pygame.draw.rect(screen, 'blue', bird)
        pygame.display.flip()
        dt = clock.tick(fps)

    pygame.quit()
