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
game_over = False

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)

img = pygame.image.load('green.jpg').convert()
ananas_img = pygame.image.load('ananasik.png').convert_alpha()
new_size = int(SIZE * 1.1)  # увеличение размера на 10%
ananas_img = pygame.transform.scale(ananas_img, (new_size, new_size))

sound_backroud = pygame.mixer.Sound('nature.mp3')
pygame.mixer.music.load('nature.mp3')
pygame.mixer.music.play(-1)

ananas_img = pygame.image.load('ananasik.png').convert_alpha()
new_size = int(SIZE * 1.5)
ananas_img = pygame.transform.scale(ananas_img, (new_size, new_size))

# загрузка картинки змейки
snake_img = pygame.image.load('ananasik.png').convert_alpha()
snake_img = pygame.transform.scale(snake_img, (new_size, new_size))

# функция отображения текста на кнопке
def draw_button_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# кнопка старт
start_button = pygame.Rect(RES // 2 - 75, RES // 2 - 50, 150, 50)
start_color = pygame.Color('black')
start_text = font_score.render('Играть', 1, pygame.Color('white'))

# кнопка выход
exit_button = pygame.Rect(RES // 2 - 75, RES // 2 + 50, 150, 50)
exit_color = pygame.Color('black')
exit_text = font_score.render('Выйти', 1, pygame.Color('white'))

while True:
    sc.blit(img, (0, 0))
    # отображение меню при game_over
    if game_over:
        pygame.draw.rect(sc, pygame.Color('white'), (RES // 4, RES // 4, RES // 2, RES // 2))
        draw_button_text('Всё(', font_end, pygame.Color('purple'), sc, RES // 2, RES // 3)
        draw_button_text(f'очки: {score}', font_score, pygame.Color('purple'), sc, RES // 2, RES // 1.8)
        pygame.draw.rect(sc, start_color, start_button)
        sc.blit(start_text, (start_button.centerx - start_text.get_width() // 2,
                            start_button.centery - start_text.get_height() // 2))
        pygame.draw.rect(sc, exit_color, exit_button)
        sc.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2,
                           exit_button.centery - exit_text.get_height() // 2))
    else:
        # отображение змейки
        for i, j in snake:
            sc.blit(snake_img, (i, j))
        sc.blit(ananas_img, (*ananas,))
        # show score очки
        # создаем поверхность для рамки
        score_rect = pygame.Surface((150, 50))
        score_rect.set_alpha(100) # задаем прозрачность
        score_rect.fill(pygame.Color('pink')) # заливаем цветом

        # рисуем рамку
        pygame.draw.rect(sc, pygame.Color('pink'), (10, 10, 150, 50), 2)

        # отображаем текст внутри рамки
        render_score = font_score.render(f'ОЧКИ: {score}', 1, pygame.Color('purple'))
        score_rect.blit(render_score, (5, 5))
        sc.blit(score_rect, (15, 15))

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
            game_over = True
            paused = False
    
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p and not game_over:
            paused = not paused
        # обработка нажатия кнопок мыши
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            # проверяем попадание курсора по кнопке старт
            if start_button.collidepoint(mouse_pos):
                x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
                ananas = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
                lenght = 1
                dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
                snake = [(x, y)]
                dx, dy = 0, 0
                score = 0 
                fps = 5
                paused = False
                game_over = False
                pygame.mixer.music.load('nature.mp3')
                pygame.mixer.music.play(-1)
            # проверяем попадание курсора по кнопке выход
            if exit_button.collidepoint(mouse_pos):
                exit() 

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
