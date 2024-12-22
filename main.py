import pygame
import random


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

        for pipe in pipes:
            pipe.x -= PIPE_SPEED

        if pipes and pipes[0].right < 0:
            pipes.pop(0)
            create_pipe()

        for pipe in pipes:
            if bird.colliderect(pipe):
                status = 'falling'


def create_pipe():
    gap = 150
    height = random.randint(50, SCREEN_HEIGHT - gap - 50)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + gap, PIPE_WIDTH, SCREEN_HEIGHT - height - gap)
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)


if __name__ == '__main__':
    pygame.init()

    size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Flappy animal')
    fps = 30
    dt = 0
    JUMP_POWER = -10
    BIRD_GRAVITY = 0.5
    RETURN_SPEED = 0.15
    PIPE_WIDTH = 60
    PIPE_SPEED = 5

    clock = pygame.time.Clock()
    running = True

    position_x = SCREEN_WIDTH / 8
    position_y = SCREEN_HEIGHT / 2.5
    speed = 0
    boost = 0

    status = 'beginning'
    bird = pygame.Rect(position_x, position_y, 60, 60)

    pipes = []
    for _ in range(3):
        create_pipe()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse = pygame.mouse.get_pressed()[0]
        update_game(status)

        screen.fill('green')
        for pipe in pipes:
            pygame.draw.rect(screen, 'red', pipe)
        pygame.draw.rect(screen, 'blue', bird)
        pygame.display.flip()
        dt = clock.tick(fps)

    pygame.quit()
