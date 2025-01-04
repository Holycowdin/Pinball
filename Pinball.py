import pygame
from pygame import Rect
from pygame.math import Vector2


WINDOW_WIDTH = 64*20
WINDOW_HEIGHT = 64*15

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREY = (180,180,180)



class PinballComponent():
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())


class Bumper(PinballComponent):
    def __init__(self, sprite, pos):
        super().__init__(sprite, pos)
        
 

class Ball():
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)

        self.movementVector = Vector2(-7, -7)
        self.acceleration = 0.1

    def move(self):
        self.pos += self.movementVector
        self.movementVector.y += self.acceleration

        self.rect.center = self.pos


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True
        #Sprites laden
        ballSprite = pygame.image.load("Assets/Sprites/Ball.png").convert_alpha()
        bumperSprite = pygame.image.load("Assets/Sprites/Bumper.png").convert_alpha()

        self.ball = Ball(ballSprite, Vector2(700, 800))
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(bumperSprite, Vector2(50, 300))
        )

    def render(self):
        self.window.fill(LIGHT_GREY)

        self.window.blit(self.ball.sprite, self.ball.rect)
        for i, bumper in enumerate(self.bumpers):
            self.window.blit(self.bumpers[i].sprite, bumper.rect)

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
                
    def moveBall(self):
        self.ball.move()

    
    def run(self):
        while self.isRunning == True:
            self.render()
            self.userInput()
            self.moveBall()
            self.clock.tick(60)


main = Main()
main.run()