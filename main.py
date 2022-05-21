# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import shelve
import random
import os
import sys
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
    """Create a text object. 

    Args:
        text (string): Text string to be rendered.
        font (Font): Text font (specified size and style).
        color (Color, optional): Text color. Defaults to black.

    Returns:
        Surface: source Surface with rendered texts.
        Rect: destination Rect specifying where the text should be.
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, size, color=black):
    """Display a text message on screen.

    Args:
        text (string): Message string to be displayed.
        x (int): x-coordinate of the message.
        y (int): y-coordinate of the message.
        size (int): Text size.
        color (Color, optional): Text color. Defaults to black.
    """
    large_text = pygame.font.SysFont('comicsansms', size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def button(msg, x, y, w, h, inactive_color, active_color, action=None, 
                                    parameter=None, parameter2=None):
    """Create a button object.

    Args:
        msg (string): Text string within the button.
        x (int): x-coordinate of the button.
        y (int): y-coordinate of the button.
        w (int): Width of the button.
        h (int): Height of the button.
        inactive_color (Color): Inactive button color.
        active_color (Color): Active button color.
        action (function, optional): A function associated to the button. Defaults to None.
        parameter (any, optional): The first parameter for the associated function. 
                                    Defaults to None.
        parameter2 (any, optional): The second parameter for the associated function. 
                                    Defaults to None.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter and parameter2 != None:
                action(parameter, parameter2)
            elif parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def display_tut():
    """Display tutorial page on screen."""
    tut_finish = False
    while not tut_finish:
        pygame.event.pump()

        multiplier_img = pygame.image.load('images/power1.bmp')
        frenzy_img = pygame.image.load('images/power2.bmp')
        double_img = pygame.image.load('images/power3.bmp')
        shorter_img = pygame.image.load('images/power4.bmp')

        screen.blit(tut_logo, (game.settings.width / 3 * 15,0-banner_height))
        
        message_display('WASD/arrows to move.', game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 20,
                            25, white)
        message_display('Eat different food to score point.', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 60,
                            25, white)
        message_display('Normal food = 1 point, Stars = 2 points', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 110,
                            20, white)
        message_display('List of Power-up:', 
                            game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 150,
                            20, white)
        screen.blit(multiplier_img, [game.settings.width / 2 * 15 - 100, 
                                    game.settings.height / 5 * 15 + 175])
        message_display('Normal food now gain x2 points', 
                            game.settings.width / 2 * 15 + 50, 
                            game.settings.height / 5 * 15 + 180,
                            15, white)
        screen.blit(frenzy_img, [game.settings.width / 2 * 15 - 100, 
                                    game.settings.height / 5 * 15 + 200])
        message_display('Frenzy mode', 
                            game.settings.width / 2 * 15 + 50, 
                            game.settings.height / 5 * 15 + 205,
                            15, white)
        screen.blit(double_img, [game.settings.width / 2 * 15 - 100, 
                                    game.settings.height / 5 * 15 + 225])
        message_display('Double spawn', 
                            game.settings.width / 2 * 15 + 50, 
                            game.settings.height / 5 * 15 + 230,
                            15, white)
        screen.blit(shorter_img, [game.settings.width / 2 * 15 - 100, 
                                    game.settings.height / 5 * 15 + 250])
        message_display('Snake lose 1 length', 
                            game.settings.width / 2 * 15 + 50, 
                            game.settings.height / 5 * 15 + 255,
                            15, white)
        message_display('In game, hold ESC to quit.', game.settings.width / 2 * 15, 
                            game.settings.height / 5 * 15 + 300,
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
                quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                tut_finish = True
    

def quitgame():
    """Quit game and close the program."""
    pygame.quit()
    quit()


def crash(fps):
    """UI feedback when the snake crashes into itself which ends the current game.

    Args:
        fps (int): The fps of the current game. Used when the user wants to  
                    restart the game in the same fps (i.e.same difficulty).
    """
    pygame.mixer.Sound.play(crash_sound)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_display('crashed', game.settings.width / 2 * 15, 
                            game.settings.height / 3 * 15 + banner_height,
                            50, white)
        button('Restart', 60, 350 + banner_height, 80, 40, green, bright_green, game_loop, 'human', fps)
        button('Return to Menu', 210, 350 + banner_height, 160, 40, orange, bright_orange, initial_interface)

        pygame.display.update()

def display_input_box(fps):
    """Display the input box for signing-in player name.

    Args:
        fps (int): The user's choice of fps (i.e.game difficulty).
    """
    input_box = pygame.Rect(game.settings.width / 4 * 15,
                            game.settings.height * 15 / 2 + banner_height,
                             140, 32)
    color_inactive = blue
    color_active = red
    color = color_inactive
    active = False
    name = ''
    # input box code reference from:
    # https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    while True:
        screen.fill(white)
        message_display('Gluttonous', game.settings.width / 2 * 15,
                        game.settings.height / 5 * 15 + banner_height, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # user clicked on input box
                if input_box.collidepoint(event.pos):
                    active = not active # toggle active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        d = shelve.open('score.txt', flag='w')
                        d['username'] = name
                        d.close()
                        name = ''
                        game_loop('human', fps)
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        # Render the current text.
        font = pygame.font.SysFont('comicsansms', 20)
        txt_surface = font.render(name, True, black)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit text and input_box rect
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        message_display('Enter player name:', game.settings.width / 2 * 15,
                game.settings.height * 15 / 2 + banner_height - 30, 20)

        # update
        pygame.display.flip()
        pygame.time.Clock().tick(15)


def initial_interface():
    """Initial Main Menu interface."""
    score1 = 0
    score2 = 0
    score3 = 0
    name1 = ''
    name2 = ''
    name3 = ''
    try:
        d = shelve.open('score.txt', flag='r')
        score1 = d['score1']
        name1 = d['name1']
        score2 = d['score2']
        name2 = d['name2']
        score3 = d['score3']
        name3 = d['name3']
        d.close()
    except KeyError:
        pass

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        message_display('Gluttonous', game.settings.width / 2 * 15, 
                        game.settings.height / 5 * 15 + banner_height, 50)

        # score board
        message_display('Score Board', game.settings.width / 2 * 15,
                        game.settings.height / 3 * 15 + banner_height, 25)
        pygame.draw.aaline(screen, black, (50,game.settings.height / 2.5 * 15 + banner_height),
                        (game.settings.width*15-50, game.settings.height / 2.5 * 15 + banner_height))

        if score1==0 and score2==0 and score3==0:
            message_display('No records', game.settings.width / 2 * 15,
                        game.settings.height / 2 * 15 + banner_height, 20)
        else:
            if score1 != 0:
                message_display('{} | {}'.format(name1, score1), game.settings.width / 2 * 15,
                        game.settings.height / 2.2 * 15 + banner_height, 18)
            if score2 != 0:
                message_display('{} | {}'.format(name2, score2), game.settings.width / 2 * 15,
                        game.settings.height / 2.2 * 15 + banner_height + 30, 18)
            if score3 != 0:
                message_display('{} | {}'.format(name3, score3), game.settings.width / 2 * 15,
                        game.settings.height / 2.2 * 15 + banner_height + 60, 18)

        # menu options
        button('Easy', 80, 270 + banner_height, 80, 40, blue, bright_blue, display_input_box, 5)
        button('Medium', 175, 270 + banner_height, 80, 40, blue, bright_blue, display_input_box, 8)
        button('Hard', 270, 270 + banner_height, 80, 40, blue, bright_blue, display_input_box, 12)

        button('How to play', 80, 325 + banner_height, 140, 40, orange, bright_orange, display_tut)

        button('Quit', 270, 325 + banner_height, 80, 40, red, bright_red, quitgame)

        pygame.display.update()
        pygame.time.Clock().tick(15)

def game_loop(player, fps):
    """Starts a new game.

    Args:
        player (string): 'human'.
        fps (_type_): The user's choice of fps (i.e.game difficulty).
    """
    game.restart_game()
    power_spawn = False
    power_spawn_time = 0

    while not game.game_end():
        current_time = pygame.time.get_ticks()
        pygame.event.pump()

        move = human_move()

        game.do_move(move)

        screen.fill(black)

        if game.power_active["2"]:
            for i in game.strawberry_ls:
                i.blit(screen)
        elif game.power_active["3"]:
            for j in game.strawberry_ls:
                if j.exist:
                    j.blit(screen)

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)


        if current_time - power_spawn_time >= 20000:
            game.powerberry.random_pos(game.snake)
            power_spawn_time = current_time
            for type in game.power_active.keys():
                game.power_active[type] = False
        elif current_time - power_spawn_time >= 6000:
            for s in game.strawberry_ls:
                s.position = [-1, -1]

            if game.powerberry.exist:
                game.powerberry.remove()

        game.powerberry.blit(screen)



        game.blit_score(white, screen)
        pygame.draw.aaline(screen, white, (0, banner_height), (game.settings.width * 15, banner_height))

        pygame.display.flip()

        fpsClock.tick(fps)

    # save score here
    d = shelve.open('score.txt', flag='w')
    if 'score1' not in d:
        d['score1'] = game.snake.score
        d['name1'] = d['username']
    elif 'score2' not in d:
        if game.snake.score > d['score1']:
            d['score2'] = d['score1']
            d['name2'] = d['name1']
            d['score1'] = game.snake.score
            d['name1'] = d['username']
        else:
            d['score2'] = game.snake.score
            d['name2'] = d['username']
    elif 'score3' not in d:
        if game.snake.score > d['score1']:
            d['score3'] = d['score2']
            d['name3'] = d['name2']
            d['score2'] = d['score1']
            d['name2'] = d['name1']
            d['score1'] = game.snake.score
            d['name1'] = d['username']
        elif game.snake.score > d['score2']:
            d['score3'] = d['score2']
            d['name3'] = d['name2']
            d['score2'] = game.snake.score
            d['name2'] = d['username']
        else:
            d['score3'] = game.snake.score
            d['name3'] = d['username']
    else:
        if game.snake.score >= d['score1']:
            d['score3'] = d['score2']
            d['name3'] = d['name2']
            d['score2'] = d['score1']
            d['name2'] = d['name1']
            d['score1'] = game.snake.score
            d['name1'] = d['username']
        elif game.snake.score >= d['score2']:
            d['score3'] = d['score2']
            d['name3'] = d['name2']
            d['score2'] = game.snake.score
            d['name2'] = d['username']
        elif game.snake.score >= d['score3']:
            d['score3'] = game.snake.score
            d['name3'] = d['username']
    d.close()
    crash(fps)


def human_move():
    """Listen to the user's key inputs and give corresponding in-game feedback.

    Returns:
        int: The integer key indicating the snake's current direction.
             If a key is pressed, it should be the user's latest input.
                        0 : 'up',
                        1 : 'down',
                        2 : 'left',
                        3 : 'right'  
    """
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

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
                gamequit = True
                # quit if esc key held for 2secs
                while pygame.time.get_ticks()/1000 - time/1000 < 2 and gamequit:
                    message_display("Hold ESC to quit...", game.settings.width /2 * 15, 
                                game.settings.height * 15-40 + banner_height, 20, white)
                    pygame.display.flip()
                    for event2 in pygame.event.get():
                        if event2.type == pygame.KEYUP:
                            gamequit = False
                if gamequit:
                    pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
