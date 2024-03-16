import sys

import pygame
import random
import json

pygame.init()


def draw_square(column, row, color):
    screen_x = column * SQUARE_SIZE
    screen_y = row * SQUARE_SIZE
    pygame.draw.rect(screen, color, (screen_x, screen_y, SQUARE_SIZE, SQUARE_SIZE))

def score(score,surface,size,x,y):
    textfont = pygame.font.SysFont("comicansms",size)
    text = textfont.render("Score:"+str(score),True,(255,255,255))
    surface.blit(text,[x,y])

def text(screen,texts,x,y,size):
    textfont = pygame.font.SysFont("comicansms",size)
    text = textfont.render(texts,True,(255,255,255))
    screen.blit(text,[x,y])

def highscore(scores):
    with open("highscore.json") as file:
        data = json.load(file)

    screen.fill((0, 0, 0))
    score(scores - 1, screen, 200, 100, 100)
    text(screen, "Good job", 100, 300, 100)
    text(screen, "Press P to play again", 100, 600, 40)
    data = snake_length - 1
    pygame.display.update()
    if data < snake_length - 1:
        screen.fill((0, 0, 0))
        score(scores - 1, screen, 200, 100, 100)
        text(screen, "New highscore", 100, 300, 100)
        text(screen, "Press P to play again", 100, 600, 40)
        data = snake_length - 1
        pygame.display.update()

    with open("highscore.json", "w") as fout:
        fout.write(json.dumps(data))

WIN_SIZE = 900
SQUARE_COUNT = 20
SQUARE_SIZE = WIN_SIZE / SQUARE_COUNT
START_LENGTH = 1
DELAY = 100

screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

head_column = SQUARE_COUNT // 2
head_row = SQUARE_COUNT // 2
snake_length = START_LENGTH
body_parts = []
step_x = 0
step_y = 0
apple_row = random.randint(0, SQUARE_COUNT - 1)
apple_column = random.randint(0, SQUARE_COUNT - 1)

running = True
while running:

    run = True
    while run:
        pygame.time.delay(DELAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if step_x != -1:
                step_x = 1
                step_y = 0
        elif keys[pygame.K_LEFT]:
            if step_x != 1:
                step_x = -1
                step_y = 0
        elif keys[pygame.K_UP]:
            if step_y != 1:
                step_x = 0
                step_y = -1
        elif keys[pygame.K_DOWN]:
            if step_y != -1:
                step_x = 0
                step_y = 1

        if step_x != 0 or step_y != 0:
            body_parts.append((head_column, head_row))
            if len(body_parts) >= snake_length:
                body_parts.pop(0)

        head_column += step_x
        head_row += step_y

        if head_column == apple_column and head_row == apple_row:
            snake_length += 1
            apple_row = random.randint(0, SQUARE_COUNT - 1)
            apple_column = random.randint(0, SQUARE_COUNT - 1)

        if head_column < 0 or head_column >= SQUARE_COUNT or head_row < 0 or head_row >= SQUARE_COUNT:
            run = False

        self_hit = (head_column, head_row) in body_parts
        if self_hit:
            run = False

        screen.fill((0, 0, 0))

        draw_square(head_column, head_row, (0, 255, 255))

        for part in body_parts:
            part_column = part[0]
            part_row = part[1]
            draw_square(part_column, part_row, (0, 255, 0))

        draw_square(apple_column, apple_row, (255, 0, 0))

        for i in range(SQUARE_COUNT):
            line_pos = SQUARE_SIZE * i
            pygame.draw.line(screen, (100, 100, 100), (line_pos, 0), (line_pos, WIN_SIZE), 2)
            pygame.draw.line(screen, (100, 100, 100), (0, line_pos), (WIN_SIZE, line_pos), 2)

        score(snake_length-1,screen,70,0,0)

        pygame.display.update()

    runi = True
    screen.fill((0, 0, 0))
    highscore(snake_length)
    while runi:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            runi = False
            head_column = SQUARE_COUNT // 2
            head_row = SQUARE_COUNT // 2
            snake_length = START_LENGTH
            body_parts = []
            step_x = 0
            step_y = 0
            apple_row = random.randint(0, SQUARE_COUNT - 1)
            apple_column = random.randint(0, SQUARE_COUNT - 1)
            run = True

pygame.display.quit()