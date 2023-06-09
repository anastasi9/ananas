import pygame
from random import randrange

RES = 800
SIZE = 50

x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
ananas = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
lenght = 1
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
snake = [(x, y)]
dx, dy = 0, 0
fps = 5

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()

while True:
    sc.fill(pygame.Color('green'))
    # drawing snake
    [(pygame.draw.rect(sc, pygame.Color('yellow'), (i, j, SIZE, SIZE))) for i, j in snake]
    pygame.draw.rect(sc, pygame.Color('red'), (*ananas, SIZE, SIZE))
    # snake movement
    x += dx * SIZE
    y += dy * SIZE
    snake.append((x, y))
    snake = snake[-lenght:]
    # eating ananas
    if snake[-1] == ananas:
        ananas = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
        lenght += 1
        fps += 1

    # game over
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE:
        break
    if len(snake) != len(set(snake)):
        break



    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
    if key[pygame.K_s] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True,}
    if key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False,}
    if key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True,}