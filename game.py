# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np

import game


class Settings:
    def __init__(self):
        self.width = 28
        self.height = 28
        self.rect_len = 15
        self.banner_height = 50

class Snake:
    def __init__(self, settings):
        self.image_up = pygame.image.load('images/head_up.bmp')
        self.image_down = pygame.image.load('images/head_down.bmp')
        self.image_left = pygame.image.load('images/head_left.bmp')
        self.image_right = pygame.image.load('images/head_right.bmp')

        self.tail_up = pygame.image.load('images/tail_up.bmp')
        self.tail_down = pygame.image.load('images/tail_down.bmp')
        self.tail_left = pygame.image.load('images/tail_left.bmp')
        self.tail_right = pygame.image.load('images/tail_right.bmp')
            
        self.image_body = pygame.image.load('images/body.bmp')

        self.settings = settings
        self.facing = "right"
        self.initialize()

    def initialize(self):
        self.facing = "right"
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)] # start with 3 part (include head)
        self.score = 0

    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))  
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))  
        else:
            screen.blit(self.image_right, (x, y))  
            
    def blit_tail(self, x, y, screen):
        # second last - last segment
        # e.g. right [6,6] - [5,6] -> [1,0]
        #      up [6,5] - [6,6] -> [0,-1]
        #      down [6,6] - [6,5] -> [0,1]
        #      left [5,6] - [6,6] -> [-1,0]
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        
        if tail_direction == [0, -1] or tail_direction == [0, 27]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1] or tail_direction == [0, -27]:
            screen.blit(self.tail_down, (x, y))  
        elif tail_direction == [-1, 0] or tail_direction == [27, 0]:
            screen.blit(self.tail_left, (x, y))  
        else:
            screen.blit(self.tail_right, (x, y))  

        return tail_direction
    
    def blit(self, rect_len, screen):
        banner = self.settings.banner_height
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len+banner, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len+banner, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len+banner, screen)                
            
    
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')
        self.exist = True
        self.initialize()
        
    def random_pos(self, snake):
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load('images/food' + str(self.style) + '.bmp')
        
        # limit the strawberries inside a inner square (9 block away from wall)
        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)

        self.exist = True
        
        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        if self.exist:
            x = self.position[0] * self.settings.rect_len
            y = self.position[1] * self.settings.rect_len + self.settings.banner_height
            screen.blit(self.image, [x,y])
            return [x,y]

    def set_exists(self, exist: bool):
        self.exist = exist
   
    def initialize(self): #starting position
        self.position = [15, 10]


class PowerBerry():
    def __init__(self, settings):
        self.settings = settings
        self.style = str(random.randint(1, 3))
        self.image = pygame.image.load('images/power' + str(self.style) + '.bmp')
        self.exist = True
        self.initialize(self.style)


    def random_pos(self, snake):
        self.style = str(random.randint(1, 3))
        self.image = pygame.image.load('images/power' + str(self.style) + '.bmp')
        self.exist = True

        # limit the strawberries inside a inner square (9 block away from wall)
        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)

        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        if self.exist:
            x = self.position[0] * self.settings.rect_len
            y = self.position[1] * self.settings.rect_len + self.settings.banner_height
            screen.blit(self.image, [x, y])
            return [x, y]

    def remove(self):
        self.position = [-1,-1]
        self.exist = False

    def initialize(self, type):  # starting position TODO spawn timer
        self.position = [20, 15]
        self.berry_type = type



class Game:
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake(self.settings)
        self.strawberry = Strawberry(self.settings)
        self.powerberry = PowerBerry(self.settings)
        self.lives = 3
        self.strawberry_ls = [None] * 784
        self.power_active = {
            "1": False,
            "2": False,
            "3": False,
        }

        for i in range(784):
            s = Strawberry(self.settings)
            s.set_exists(False)
            s.position = [i % 28, i // 28]
            self.strawberry_ls[i] = s

        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

    # uncomment if new implementation need to use states
    
    # def current_state(self):         
    #     state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
    #     expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
    #     for position in self.snake.segments:
    #         state[position[1], position[0], 0] = 1
        
    #     state[:, :, 1] = -0.5        

    #     state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
    #     for d in expand:
    #         state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
    #     return state
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        self.check_wraparound()
        # insert segments AFTER check wraparound
        self.snake.segments.insert(0, list(self.snake.position))  # automatically inserts a snake length

        if self.snake.position == self.strawberry.position: # snake eating strawberry
            pygame.mixer.Sound.play(pygame.mixer.Sound('./sound/eat.mp3'))
            # star object +2, TODO:has timer of 5s

            if self.power_active["1"]:
                self.snake.score += 1

            if self.strawberry.style == '3':
                self.snake.score += 1
            self.strawberry.random_pos(self.snake)

            reward = 1
            self.snake.score += 1

        elif self.snake.position == self.powerberry.position and self.powerberry.exist: # snake eating power berry
            pygame.mixer.Sound.play(pygame.mixer.Sound('./sound/PowerUp.mp3'))
            self.power_active[str(self.powerberry.style)] = True

            if self.power_active["1"]:
                self.snake.score += 1
                second_berry = False
                for x in self.strawberry_ls:
                    if x != None and x.exist:
                        second_berry = True
                if self.strawberry.style == '3' or second_berry:
                    self.snake.score += 2

            elif self.powerberry.style == "2":
                for i in range(783):
                    s = Strawberry(self.settings)
                    s.set_exists(False)
                    s.position = [i % 28, i // 28]
                    self.strawberry_ls[i] = s

                for s in self.strawberry_ls:
                    s.set_exists(True)

            elif self.powerberry.style == "3":
                self.snake.segments.pop()  # need to pop snake segments twice because it automatically adds 1 length
                self.snake.segments.pop()

            self.powerberry.remove()
            reward = 0

        else:
            self.snake.segments.pop()
            reward = 0

        for index, s in enumerate(self.strawberry_ls):
            if s != None and s.exist and self.snake.position == s.position:
                self.snake.score += 1
                s.set_exists(False)
                s.position = [-1, -1]

        if self.game_end():
            return -1
        return reward
    
    def check_wraparound(self):
        # right wall
        if self.snake.position[0] >= self.settings.width:
            self.snake.position[0] -= self.settings.width
        # left wall
        if self.snake.position[0] < 0:
            self.snake.position[0] += self.settings.width
        # bottom wall
        if self.snake.position[1] >= self.settings.height:
            self.snake.position[1] -= self.settings.height
        # top wall
        if self.snake.position[1] < 0:
            self.snake.position[1] += self.settings.height

    def game_end(self):
        end = False
        if self.lives == 0:
            end = True
            return end
        elif self.snake.segments[0] in self.snake.segments[1:]:
            self.lives -= 0.5  # to account from the frame rate of the game
            if self.lives - int(self.lives) == 0:  # only play sound when it's a whole number
                pygame.mixer.Sound.play(pygame.mixer.Sound('./sound/crash.wav'))
        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        score_text = 'Score: ' + str(self.snake.score)
        text = font.render(score_text, True, color)
        screen.blit(text, (0, 0))
        return score_text # test only

    def blit_life(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        score_text = 'Lives: ' + str(int(self.lives))
        text = font.render(score_text, True, color)
        screen.blit(text, (100, 0))
        return score_text


