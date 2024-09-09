import unittest
import time
import pygame
from Tween import Tween

class TweenTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        self.clock = pygame.time.Clock()

    def tearDown(self):
        pygame.quit()

    def test_tween_position(self):
        square = pygame.Rect(100, 100, 50, 50)
        tween = Tween(square, 2, tween_property='topleft', from_=square.topleft, to_=(200, 200))
        tween.start()

        while not tween.is_finished():
            self.clock.tick(60)
            tween.update()

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 0, 0), square)
            pygame.display.flip()

        self.assertEqual(square.topleft, (200, 200))

if __name__ == '__main__':
    unittest.main()