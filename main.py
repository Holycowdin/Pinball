from Player import Ball, Player
from PinballComponents import PinballComponent, Flipper, Bumper, Slingshot, Slope, Target, Plunger, Curve

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
        #Font intialisieren
        self.font = pygame.font.SysFont("Arial", 32)
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
        targetSprite = pygame.image.load("Assets/Sprites/Target.png").convert_alpha()
        targetSprite = pygame.transform.smoothscale(targetSprite, Vector2(51,64))
        plungerSprite = pygame.image.load("Assets/Sprites/Plunger.png").convert_alpha()
        #Surface für Kurve erstellen - nur vorübergehend
        curveSurface = pygame.Surface(Vector2(300, 300))
        curveSurface.fill(WHITE)
        curveSurface.set_colorkey(WHITE)
        pygame.gfxdraw.bezier(curveSurface, (Vector2(0,0), Vector2(260,40), Vector2(260,300)), 1000, BLACK)
        #Ball erstellen
        self.ball = Ball(ballSprite, Vector2(1200 + 14, 700)) #700, 800
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
            Bumper(bumperSprite, Vector2(650, 250))  #50, 600
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
        #Targets erstellen
        self.targets:list[Target] = []
        self.targets.append(
            Target(targetSprite, Vector2(550, 400))
        )
        #Plunger erstellen
        self.plungers:list[Plunger] = []
        self.plungers.append(
            Plunger(plungerSprite, Vector2(1200, 800))
        )
        #Kurven erstellen
        self.curves:list[Curve] = []
        self.curves.append(
            Curve(curveSurface.convert(), Vector2(WINDOW_WIDTH - curveSurface.get_width(), 30))
        )
        self.components:tuple[PinballComponent] = tuple(self.flippers + self.bumpers + self.slopes + self.slingshots + self.targets + self.plungers + self.curves)
        #Spieler initialisieren
        self.player = Player()

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
        scoreText = self.font.render(str(self.player.score), True, BLACK)
        self.window.blit(scoreText, Vector2(1200, 900))

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
        if not self.ball.isOnField:
            if keys[pygame.K_SPACE]:
                self.plungers[0].startMoving(self.ball)
            elif self.plungers[0].isMoving and not self.plungers[0].isMovingBack:
                self.plungers[0].moveBack()

    def moveObjects(self):
        """Callt Methode für Bewegung von Ball und Flipper"""
        self.ball.move()
        for flipper in self.flippers:
            if flipper.isMoving == True:
                flipper.move()
        for plunger in self.plungers:
            if plunger.isMoving == True:
                plunger.move()

    def checkCollisions(self):
        """Prüft Kollision zwischen Ball und anderen Komponenten"""
        for component in self.components:
            if not component.checkRectCollision(self.ball.rect):
                continue
            if not component.checkPixelCollision(self.ball.mask, self.ball.rect):
                continue
            component.collide(self.ball)
            self.player.increaseScore(component.points)


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


#Punkteanzahl für alle Komponenten
#Ball sollte man trappen können - aktuell zittert der Ball herum; wenn Flippertaste schnell losgelassen und wieder gedrückt wird, fällt Ball halb durch Flipper
#Slingshot funktioniert von allen Seiten, später eigene Maske für Schräge und andere zwei Seiten
#Ball kann auf Target stuck werden -> viele Punkte. Liegt daran, dass self.correctBallPosition gecallt wird und der Ball wieder über Target ist.
#                                                   Lässt sich vermutlich vermeiden, indem mehrere Masken benutzt werden. Keine Punkte, wenn Ball von oben kommt
#                                                   Bzw. vielleicht auch gar nicht möglich durch Begrenzung von Spielfeld