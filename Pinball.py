import pygame
from pygame import Rect, Mask
from pygame.math import Vector2


WINDOW_WIDTH = 64*20
WINDOW_HEIGHT = 64*15

BLACK = (0,0,0)
WHITE = (255,255,255)



class PinballComponent():
    def __init__(self):
        pass


class Bumper(PinballComponent):
    def __init__(self):
        super().__init__()
 

class Ball():
    def __init__(self):
        pass


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True

    def render(self):
        self.window.fill(BLACK)

        pygame.display.update()
    
    def userInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return

    
    def run(self):
        while self.isRunning == True:
            self.render()
            self.userInput()


main = Main()
main.run()