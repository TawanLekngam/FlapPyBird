import os
import random
import sys

import pygame

pygame.init()

pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 30)

icon = pygame.image.load(os.path.join('assets', 'bBird_DownFlap.png')).convert_alpha()
pygame.display.set_icon(icon)

game_intro = True
game_over = False
high_score = 0
score = 0
gravity = 0.15
bird_movement = 0
pipe_speed = 1.85
pipe_max_speed = 7

bg_surface = pygame.image.load(os.path.join('assets', 'Background_Day.png')).convert()
bg_x_pos = 0

floor_surface = pygame.image.load(os.path.join('assets', 'Floor.png')).convert()
floor_x_pos = 0

FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(FLAP, 125)
bird_downFlip = pygame.image.load(os.path.join('assets', 'bBird_DownFlap.png')).convert_alpha()
bird_midFlip = pygame.image.load(os.path.join('assets', 'bBird_MidFlap.png')).convert_alpha()
bird_upFlap = pygame.image.load(os.path.join('assets', 'bBird_UpFlap.png')).convert_alpha()
bird_surfaces = [bird_downFlip, bird_midFlip, bird_upFlap]
bird_state = 0
bird_surface = bird_surfaces[bird_state]
bird_rect = bird_surface.get_rect(center=(75, 226))

pipe_surface = pygame.image.load(os.path.join('assets', 'Pipe_Green.png')).convert_alpha()
pipe_list = list()
PIPE = pygame.USEREVENT
pygame.time.set_timer(PIPE, 1500)
pipe_height = [200, 250, 300, 350, 400]

game_intro_surface = pygame.image.load(os.path.join('assets', 'Message.png')).convert_alpha()
game_intro_rect = game_intro_surface.get_rect(center=(144, 226))

game_over_surface = pygame.image.load(os.path.join('assets', 'GameOver.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 226))


def draw_bg():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos + 288, 0))


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def animation_bird():
    new_bird = bird_surfaces[bird_state]
    new_bird_rect = new_bird.get_rect(center=(75, bird_rect.centery))
    return new_bird, new_bird_rect


def rotate_bird(bird: pygame.Surface):
    rotation_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return rotation_bird


def generate_pipe():
    pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, pipe_pos - 125))
    return bottom_pipe, top_pipe


def move_pipe(pipes: list):
    for pipe in pipes:
        pipe.centerx -= 1.85
        if pipe.centerx <= -50:
            pipes.remove(pipe)
    return pipes


def draw_pipe(pipes: list):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def update_pipe_speed(current_speed):
    if current_speed % 10 == 0:
        current_speed += 0.1
    return current_speed


def check_collision(pipes: list):
    # pipe collision
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    # out of screen
    if bird_rect.top <= -100 or bird_rect.bottom >= 460:
        return True

    return False


def update_score(sCore: int, high_sCore: int):
    if sCore > high_sCore:
        high_sCore = sCore
    return high_sCore


def score_display(game_state: bool):
    if not game_state:
        score_surface = game_font.render(str(int(score)), True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(144, 100))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(144, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(144, 350))
        screen.blit(high_score_surface, high_score_rect)


# Game Loop
while True:

    # Event Listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_intro:
                pipe_list.clear()
                game_intro = False

            if event.key == pygame.K_SPACE and not game_over:
                bird_movement = 0
                bird_movement -= 4.75

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipe_list.clear()
                bird_rect.center = (75, 226)
                bird_movement = 0
                score = 0

        if event.type == PIPE:
            pipe_list.extend(generate_pipe())

        if event.type == FLAP:
            if bird_state < 2:
                bird_state += 1
            else:
                bird_state = 0

            bird_surface, bird_rect = animation_bird()

    # Background
    bg_x_pos -= 0.25
    draw_bg()
    if bg_x_pos <= -288:
        bg_x_pos = 0

    if game_intro:
        screen.blit(game_intro_surface, game_intro_rect)

    else:

        if game_over:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)

        else:
            bird_movement += gravity
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_over = check_collision(pipe_list)

            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)

        score_display(game_over)

        if not game_over:
            score += 0.005
            pipe_speed = update_pipe_speed(score)

    # Floor
    floor_x_pos -= 0.75
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
