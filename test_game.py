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
        self.snake = self.testGame.snake
        self.strawberry = self.testGame.strawberry

    # settings CLASS
    def test_settings(self):
        settings = game.Settings()
        self.assertTrue(settings.width==28)
        self.assertTrue(settings.height==28)
        self.assertTrue(settings.rect_len==15)

    # Game CLASS
    def test_constructor(self):
        # create a class automatically create settings, snake, strawberry
        self.assertIsNotNone(self.testGame.snake)
        self.assertIsNotNone(self.testGame.settings)
        self.assertIsNotNone(self.testGame.strawberry)
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

        
    # snake CLASS
    def test_constructor_snake(self):
        # all sprites set
        self.assertIsNotNone(self.snake.image_up)  
        self.assertIsNotNone(self.snake.image_down)  
        self.assertIsNotNone(self.snake.image_left)  
        self.assertIsNotNone(self.snake.image_right)  
        self.assertIsNotNone(self.snake.tail_up)
        self.assertIsNotNone(self.snake.tail_down)
        self.assertIsNotNone(self.snake.tail_left)
        self.assertIsNotNone(self.snake.tail_right) 
        self.assertIsNotNone(self.snake.image_body)
        # snake initial facing "right"
        self.assertEqual("right", self.snake.facing)
    
    def test_snake_initialize(self):
        self.snake.initialize()
        self.snake.score = 0
        self.assertEqual([6,6], self.snake.position)
        self.assertEqual([[6,6],[5,6],[4,6]], self.snake.segments)
        self.assertEqual(0, self.snake.score)

    def test_blit(self):
        pygame.init()
        screen = pygame.display.set_mode((self.testGame.settings.width * 15, 
                                self.testGame.settings.height * 15))
        # some cannot check condition because purely screen display
        # blit (OK if no exception)
        self.assertTrue(self.testGame.settings.rect_len==15)
        self.snake.blit(self.testGame.settings.rect_len, screen)
        # blit body (OK if no exception)
        self.snake.blit_body(0, 0, screen)
        # blit head (OK if no exception)
        self.snake.facing = "up"
        self.snake.blit_head(0, 0, screen)
        self.snake.facing = "down"
        self.snake.blit_head(0, 0, screen)
        self.snake.facing = "left"
        self.snake.blit_head(0, 0, screen)
        self.snake.facing = "right"
        self.snake.blit_head(0, 0, screen)

        # blit tail
        # right
        self.snake.segments = [[7, 6], [6, 6], [5, 6]]
        self.assertEqual([1,0], self.snake.blit_tail(0, 0, screen))
        # up
        self.snake.segments = [[5, 5], [6, 5], [6, 6]]
        self.assertEqual([0,-1], self.snake.blit_tail(0, 0, screen))
        # down
        self.snake.segments = [[6, 8], [6, 7], [6, 6], [6, 5]]
        self.assertEqual([0,1], self.snake.blit_tail(0, 0, screen))
        # left
        self.snake.segments = [[5, 5], [5, 6], [6, 6]]
        self.assertEqual([-1,0], self.snake.blit_tail(0, 0, screen))

    def test_update(self):
        self.snake.position = [5,5]
        # right
        self.snake.facing = "right"
        self.snake.update()
        self.assertEqual([6,5], self.snake.position)
        # left
        self.snake.facing = "left"
        self.snake.update()
        self.assertEqual([5,5], self.snake.position)
        # up
        self.snake.facing = "up"
        self.snake.update()
        self.assertEqual([5,4], self.snake.position)
        # down
        self.snake.facing = "down"
        self.snake.update()
        self.assertEqual([5,5], self.snake.position)
        
    # Strawberry CLASS
    def test_constructor_strawberry(self):
        self.assertEqual(self.strawberry.settings, self.testGame.settings)
        self.assertTrue(int(self.strawberry.style) >= 1 and int(self.strawberry.style) <= 8)
        self.assertIsNotNone(self.strawberry.image)
    
    def test_random_pos(self):
        self.snake.segments = [[5, 5], [5, 6], [6, 6]]
        self.strawberry.position = [5,6]
        self.strawberry.random_pos(self.snake)

        self.assertTrue(self.strawberry.settings.width==28)
        self.assertTrue(self.strawberry.settings.height==28)
        # x, y position within inner square (9 block away from wall)
        self.assertTrue(self.strawberry.position[0] >= 9 and self.strawberry.position[0] <= 19)
        self.assertTrue(self.strawberry.position[1] >= 9 and self.strawberry.position[1] <= 19)

    def test_blit_strawberry(self):
        pygame.init()
        screen = pygame.display.set_mode((self.testGame.settings.width * 15, 
                                self.testGame.settings.height * 15))
        self.strawberry.position = [1,2]
        self.assertTrue(self.strawberry.settings.rect_len==15)

        result = self.strawberry.blit(screen)
        self.assertEqual([15,30], result)
    
    def test_initialize_strawberry(self):
        self.strawberry.initialize()
        self.assertEqual([15,10], self.strawberry.position)



    
