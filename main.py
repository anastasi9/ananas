import pygame
from random import randrange

RES = 500
SIZE = 25

pygame.display.set_caption('Змеюшка')

x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
ananas = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
lenght = 1
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
snake = [(x, y)]
dx, dy = 0, 0
score = 0 
fps = 5
paused = False

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)

img = pygame.image.load('green.jpg').convert()

sound_backroud = pygame.mixer.Sound('nature.mp3')
pygame.mixer.music.load('nature.mp3')
pygame.mixer.music.play(-1)

while True:
    sc.blit(img, (0, 0))
    # drawing snake вид змейки
    [(pygame.draw.rect(sc, pygame.Color('yellow'), (i, j, SIZE - 2, SIZE - 2))) for i, j in snake]
    pygame.draw.rect(sc, pygame.Color('red'), (*ananas, SIZE, SIZE))
    # show score очки
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    sc.blit(render_score, (5, 5))
    # snake movement движения змейки
    if not paused:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-lenght:]
    # eating ananas
    if snake[-1] == ananas:
        ananas = randrange(0, RES, SIZE), randrange(0, RES, SIZE) 
        lenght += 1
        score += 1
        fps += 1
        sound_eat = pygame.mixer.Sound('nyam.mp3')
        pygame.mixer.music.load('nyam.mp3')
        sound_eat.play()
        music = pygame.mixer.music.load('nature.mp3')
        pygame.mixer.music.play(-1)
           
    # game over
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            sc.blit(render_end, (RES // 3 - 100, RES // 3))
            pygame.display.flip()
            for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     exit()
    
    # show "PAUSED" text if game is paused
    if paused:
        render_paused = font_end.render('PAUSED', 1, pygame.Color('orange'))
        sc.blit(render_paused, (RES // 2 - 100, RES // 3))

    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # toggle pause on 'p' key press
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused

    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'S': False, 'A': True, 'D': True,}
    if key[pygame.K_s] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'S': True, 'A': True, 'D': True,}
    if key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'S': True, 'A': True, 'D': False,}
    if key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'S': True, 'A': False, 'D': True,}