# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
orange = pygame.Color(255, 197, 148)
bright_orange = pygame.Color(255, 165, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
banner_height = 50
screen = pygame.display.set_mode((game.settings.width * 15, 
                                game.settings.height * 15 + banner_height))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')
tut_logo = pygame.image.load('images/snake.png')


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, size, color=black):
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None, parameter2=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter, parameter2)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def display_tut():
    tut_finish = False
    while not tut_finish:
        pygame.event.pump()

        screen.blit(tut_logo, (game.settings.width / 3 * 15,0-banner_height))
        message_display('WASD/arrows to move.', game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 20,
                            25, white)
        message_display('Eat different food to score point!', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 60,
                            25, white)
        message_display('But be careful...', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 120,
                            20, white)
        message_display('You grow larger as your points go up.', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 150,
                            20, white)
        message_display('You lose if you crash into yourself.', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 200,
                            20, white)
        message_display('In game, hold ESC to quit.', game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 260,
                            20, white)
        message_display('(Press ESC to return to menu)', game.settings.width / 2 * 15, 
                            game.settings.height * 15,
                            15, white)
        
        pygame.display.update()

        screen.fill(black)

        # escape key to return to menu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                tut_finish = True
    

def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, 
                        game.settings.height / 3 * 15 + banner_height,
                        50, white)
    time.sleep(1)


def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        message_display('Gluttonous', game.settings.width / 2 * 15, 
                        game.settings.height / 4 * 15 + banner_height, 50)

        button('Easy', 80, 180 + banner_height, 80, 40, blue, bright_blue, game_loop, 'human', 5)
        button('Medium', 175, 180 + banner_height, 80, 40, blue, bright_blue, game_loop, 'human', 8)
        button('Hard', 270, 180 + banner_height, 80, 40, blue, bright_blue, game_loop, 'human', 12)

        button('How to play', 145, 240 + banner_height, 140, 40, orange, bright_orange, display_tut)

        button('Quit', 175, 300 + banner_height, 80, 40, red, bright_red, quitgame)

        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps):
    game.restart_game()

    while not game.game_end():

        pygame.event.pump()

        move = human_move()

        game.do_move(move)

        screen.fill(black)

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                time = pygame.time.get_ticks()
                quit = True
                # quit if esc key held for 2secs
                while pygame.time.get_ticks()/1000 - time/1000 < 2 and quit:
                    message_display("Hold ESC to quit...", game.settings.width /2 * 15, 
                                game.settings.height * 15-40 + banner_height, 20, white)
                    pygame.display.flip()
                    for event2 in pygame.event.get():
                        if event2.type == pygame.KEYUP:
                            quit = False
                if quit:
                    pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
