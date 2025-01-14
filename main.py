from Ball import Ball
from PinballComponents import PinballComponent, Flipper, Bumper, Slingshot, Slope

import pygame
import pygame.gfxdraw
from pygame.math import Vector2


WINDOW_WIDTH = 64*20
WINDOW_HEIGHT = 64*15

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREY = (180,180,180)


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
        slingshotSprite = pygame.image.load("Assets/Sprites/Slingshot.png").convert_alpha()
        #slingshotSprite = pygame.transform.flip(slingshotSprite, True, False)
        flipperSprite = pygame.image.load("Assets/Sprites/Flipper.png").convert_alpha()
        flipperSprite = pygame.transform.rotate(flipperSprite, 35)
        flipperSprite = pygame.transform.flip(flipperSprite, True, False)
        #Ball erstellen
        self.ball = Ball(ballSprite, Vector2(700, 800)) #700, 800
        #Flipper erstellen
        self.flippers:list[Flipper] = []
        self.flippers.append(
            Flipper(flipperSprite, Vector2(300, 550), 1)
        )
        flipperSprite = pygame.transform.flip(flipperSprite, True, False)
        self.flippers.append(
            Flipper(flipperSprite, Vector2(800, 800), -1)   #300, 800
        )
        #Bumper erstellen
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(bumperSprite, Vector2(650, 50))  #50, 600
        )
        #Slopes erstellen
        self.slopes:list[Slope] = []
        self.slopes.append(
            Slope(slopeSprite, Vector2(970, 510))   #980, 530
        )
        #Slingshots erstellen
        self.slingshots:list[Slingshot] = []
        self.slingshots.append(
            Slingshot(slingshotSprite, Vector2(600, 750))
        )

        self.components:tuple[PinballComponent] = tuple(self.flippers + self.bumpers + self.slopes + self.slingshots)


    def render(self):
        """Rendert den gesamten Bildschirm, einschließlich Objekte"""
        self.window.fill(LIGHT_GREY)
        #Ball rendern
        self.window.blit(self.ball.sprite, self.ball.rect)
        #Komponenten rendern
        for component in self.components:
            self.window.blit(component.sprite, component.rect)
        #self.window.blit(self.flippers[1].mask.to_surface(), self.flippers[1].rect)
        #self.window.blit(self.ball.sprite, self.ball.rect)

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.flippers[0].startMoving()
        if keys[pygame.K_d]:
            self.flippers[1].startMoving()
        

    def moveObjects(self):
        """Callt Methode für Bewegung von Ball und Flipper"""
        self.ball.move()
        for flipper in self.flippers:
            if flipper.isMoving == True:
                flipper.move()

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
            self.moveObjects()
            self.userInput()
            self.clock.tick(60)


main = Main()
main.run()



#Ball sollte man trappen können - aktuell zittert der Ball herum; wenn Flippertaste schnell losgelassen und wieder gedrückt wird, fällt Ball halb durch Flipper
#Slingshot funktioniert von allen Seiten, später eigene Maske für Schräge und andere zwei Seiten