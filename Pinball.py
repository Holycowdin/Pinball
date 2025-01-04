import pygame
from pygame import Rect
from pygame.math import Vector2


WINDOW_WIDTH = 64*20
WINDOW_HEIGHT = 64*15

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREY = (180,180,180)


class Ball():
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)

        self.movementVector = Vector2(-7, -7)
        self.acceleration = Vector2(0.02, 0.1)

    def move(self):
        self.pos += self.movementVector
        self.movementVector.y += self.acceleration.y
        if (self.movementVector.x > 0) and (self.movementVector.x > self.acceleration.x):
            self.movementVector.x -= self.acceleration.x
        elif (self.movementVector.x < 0) and (self.movementVector.x < self.acceleration.x):
            self.movementVector.x += self.acceleration.x
        else:
            self.movementVector.x = 0

        self.rect.center = self.pos


class PinballComponent():
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())

    def checkRectCollision(self, ballRect: Rect) -> bool:
        if self.rect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect):
        if self.mask.overlap(ballMask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top)):
            return True

    def collide(self):
        raise NotImplementedError


class Bumper(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)

    def collide(self, ball:Ball):
        movementVector = ball.pos - Vector2(self.rect.center)
        movementVector.scale_to_length(14)
        ball.movementVector = movementVector


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True
        #Sprites laden
        ballSprite = pygame.image.load("Assets/Sprites/Ball.png").convert_alpha()
        bumperSprite = pygame.image.load("Assets/Sprites/Bumper.png").convert_alpha()
        #Ball und Komponenten erstellen
        self.ball = Ball(ballSprite, Vector2(700, 800))
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(bumperSprite, Vector2(50, 600))
        )


    def render(self):
        self.window.fill(LIGHT_GREY)
        #Ball rendern
        self.window.blit(self.ball.sprite, self.ball.rect)
        #Bumper rendern
        for bumper in self.bumpers:
            self.window.blit(bumper.sprite, bumper.rect)

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

    def checkCollisions(self):
        for bumper in self.bumpers:
            if not bumper.checkRectCollision(self.ball.rect):
                continue
            if not bumper.checkPixelCollision(self.ball.mask, self.ball.rect):
                continue
            bumper.collide(self.ball)


    def run(self):
        while self.isRunning == True:
            self.render()
            self.checkCollisions()
            self.userInput()
            self.moveBall()
            self.clock.tick(60)


main = Main()
main.run()