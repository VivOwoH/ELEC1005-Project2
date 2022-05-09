from typing_extensions import assert_type
import pygame
import unittest
import game

# run test in terminal
# python -m unittest test.py
# python -m unittest discover
# coverage run -m unittest discover
# coverage report

class test(unittest.TestCase):

    def setUp(self) -> None:
        self.testGame = game.Game()

    # Game CLASS
    def test_constructor(self):
        self.assertTrue(self.testGame.settings.width==28)
        self.assertTrue(self.testGame.settings.height==28)
        self.assertTrue(len(self.testGame.move_dict)==4)
    
    def test_restart(self):
        self.testGame.restart_game()
        # snake initialize
        self.assertEqual([6,6], self.testGame.snake.position)
        self.assertEqual([[6,6],[5,6],[4,6]], self.testGame.snake.segments)
        self.assertEqual(0, self.testGame.snake.score)
        # strawberry initialize
        self.assertEqual([15,10], self.testGame.strawberry.position)
        
    def test_direction_to_int(self):
        # test "right"==3, and vice versa
        self.assertEqual("right", self.testGame.move_dict[3])
        self.assertEqual(3, self.testGame.direction_to_int("right"))
        # test "left"==2, and vice versa
        self.assertEqual("left", self.testGame.move_dict[2])
        self.assertEqual(2, self.testGame.direction_to_int("left"))
        # test "up"==0, and vice versa
        self.assertEqual("up", self.testGame.move_dict[0])
        self.assertEqual(0, self.testGame.direction_to_int("up"))
        # test "down"==1, and vice versa
        self.assertEqual("down", self.testGame.move_dict[1])
        self.assertEqual(1, self.testGame.direction_to_int("down"))
    
    def test_do_move(self):
        # test change direction 
        # change right, face left (do nothing)
        self.testGame.snake.facing = "left"
        self.testGame.do_move(3)
        self.assertEqual("left", self.testGame.snake.facing)
        # change right, face up/down (change)
        self.testGame.snake.facing = "up"
        self.testGame.do_move(3)
        self.assertEqual("right", self.testGame.snake.facing)

        # change left, face right (do nothing)
        self.testGame.snake.facing = "right"
        self.testGame.do_move(2)
        self.assertEqual("right", self.testGame.snake.facing)
        # change left, face up/down (change)
        self.testGame.snake.facing = "down"
        self.testGame.do_move(2)
        self.assertEqual("left", self.testGame.snake.facing)

        # change up, face down (do nothing)
        self.testGame.snake.facing = "down"
        self.testGame.do_move(0)
        self.assertEqual("down", self.testGame.snake.facing)
        # change up, face left/right (change)
        self.testGame.snake.facing = "left"
        self.testGame.do_move(0)
        self.assertEqual("up", self.testGame.snake.facing)

        # change down, face up (do nothing)
        self.testGame.snake.facing = "up"
        self.testGame.do_move(1)
        self.assertEqual("up", self.testGame.snake.facing)
        # change down, face left/right (change)
        self.testGame.snake.facing = "right"
        self.testGame.do_move(1)
        self.assertEqual("down", self.testGame.snake.facing)

    def test_wraparound(self):
        # play area 28 x 28 (0:27 x 0:27)
        # right wall
        self.testGame.snake.position = [28,0]
        self.testGame.check_wraparound()
        self.assertEqual([0,0], self.testGame.snake.position)
        # left wall
        self.testGame.snake.position = [-1,0]
        self.testGame.check_wraparound()
        self.assertEqual([27,0], self.testGame.snake.position)
        # top wall
        self.testGame.snake.position = [0,-1]
        self.testGame.check_wraparound()
        self.assertEqual([0,27], self.testGame.snake.position)
        # down wall
        self.testGame.snake.position = [0,28]
        self.testGame.check_wraparound()
        self.assertEqual([0,0], self.testGame.snake.position)

    def test_gameEndCondition(self):
        self.assertFalse(self.testGame.game_end())
        # game end only if snake crash
        self.testGame.snake.segments = [[6 - i, 6] for i in range(4)]
        self.testGame.snake.segments[0] = [3,6] # crash to tail
        self.assertTrue(self.testGame.game_end())

    def test_blit_score(self):
        pygame.init()
        white = pygame.Color(255, 255, 255)
        screen = pygame.display.set_mode((self.testGame.settings.width * 15, 
                                self.testGame.settings.height * 15))
        text = self.testGame.blit_score(white, screen)
        self.assertEqual("Score: 0", text)

        

