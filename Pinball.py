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
        """Bewegt den Ball"""
        self.pos += self.movementVector
        if (self.movementVector.x > 0) and (self.movementVector.x > self.acceleration.x):
            self.movementVector.x -= self.acceleration.x
        elif (self.movementVector.x < 0) and (self.movementVector.x < self.acceleration.x):
            self.movementVector.x += self.acceleration.x
        else:
            self.movementVector.x = 0

        self.rect.center = self.pos
        self.movementVector.y += self.acceleration.y


class PinballComponent():
    """Klasse für alle Pinball-Komponenten, außer Ball"""
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())

    def checkRectCollision(self, ballRect: Rect) -> bool:
        """Prüft Kollision der Rects von Ball und Komponente"""
        if self.rect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect) -> bool:
        """Prüft pixelgenaue Kollision für Ball und Komponente; nur gecallt, wenn Rects kollidieren"""
        if ballMask.overlap(self.mask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top)):
            return True

    def collide(self, ball:Ball):
        raise NotImplementedError


class Bumper(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)

    def collide(self, ball:Ball):
        """Handling der Kollision von Bumper und Ball"""
        movementVector = ball.pos - Vector2(self.rect.center)
        movementVector.scale_to_length(14)
        ball.movementVector = movementVector


class Slope(PinballComponent):
    def __init__(self, sprite, pos):
        super().__init__(sprite, pos)
        if self.mask.get_at(self.sprite.get_rect().topleft):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   ##Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)

    def collide(self, ball:Ball):
        """Handling der Kollision von Slope und Ball"""
        vectorLength = ball.movementVector.length()
        self.slopeVector.scale_to_length(vectorLength)
        ball.movementVector = self.slopeVector.copy()


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True
        #Sprites laden
        ballSprite = pygame.image.load("Assets/Sprites/Ball.png").convert_alpha()
        bumperSprite = pygame.image.load("Assets/Sprites/Bumper.png").convert_alpha()
        slopeSprite = pygame.image.load("Assets/Sprites/Line.png").convert_alpha()
        slopeSprite = pygame.transform.flip(slopeSprite, True, False)
        #Ball und Komponenten erstellen
        self.ball = Ball(ballSprite, Vector2(700, 800))
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(bumperSprite, Vector2(50, 600))
        )
        self.slopes:list[Slope] = []
        self.slopes.append(
            Slope(slopeSprite, Vector2(900, 0))
        )

        self.components:tuple[PinballComponent] = tuple(self.bumpers + self.slopes)


    def render(self):
        """Rendert den gesamten Bildschirm, einschließlich Objekte"""
        self.window.fill(LIGHT_GREY)
        #Ball rendern
        self.window.blit(self.ball.sprite, self.ball.rect)
        #Bumper rendern
        for bumper in self.bumpers:
            self.window.blit(bumper.sprite, bumper.rect)
        #Slopes rendern
        for slope in self.slopes:
            self.window.blit(slope.sprite, slope.rect)

        pygame.display.update()

    def userInput(self):
        """Handling vom User-Input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return

    def moveBall(self):
        """Callt Methode für Bewegung von Ball"""
        self.ball.move()

    def checkCollisions(self):
        """Prüft Kollision zwischen Ball und anderen Komponenten"""
        for component in self.components:
            if not component.checkRectCollision(self.ball.rect):
                continue
            if not component.checkPixelCollision(self.ball.mask, self.ball.rect):
                continue
            component.collide(self.ball)


    def run(self):
        """Game-Loop"""
        while self.isRunning == True:
            self.render()
            self.checkCollisions()
            self.moveBall()
            self.userInput()
            self.clock.tick(60)


main = Main()
main.run()