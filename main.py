from Player import Ball, Player
from PinballComponents import PinballComponent, Flipper, Bumper, Slingshot, Slope, StationaryTarget, DropTarget, Plunger, Curve

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
        #Ball erstellen
        self.ball = Ball(Vector2(1200 + 14, 700)) #700, 800
        #Flipper erstellen
        self.flippers:list[Flipper] = []
        self.flippers.append(
            Flipper(Vector2(300, 550), 1)
        )
        self.flippers.append(
            Flipper(Vector2(800, 800), -1)   #300, 800
        )
        #Bumper erstellen
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(Vector2(650, 250), variant=1)
        )
        #Slopes erstellen
        self.slopes:list[Slope] = []
        self.slopes.append(
            Slope(Vector2(970, 510))   #980, 530
        )
        #Slingshots erstellen
        self.slingshots:list[Slingshot] = []
        self.slingshots.append(
            Slingshot(Vector2(600, 700), variant=1)
        )
        #Stationäre Targets erstellen
        self.stationaryTargets:list[StationaryTarget] = []
        self.stationaryTargets.append(
            StationaryTarget(Vector2(550, 400), index=len(self.stationaryTargets)+1)
        )
        #Drop Targets erstellen
        self.dropTargets:list[DropTarget] = []
        self.dropTargets.append(
            DropTarget(Vector2(1200, 400), variant=1)
        )
        self.dropTargets.append(
            DropTarget(Vector2(1200, 500), variant=2)
        )
        self.dropTargets.append(
            DropTarget(Vector2(1200, 600), variant=3)
        )
        #Plunger erstellen
        self.plungers:list[Plunger] = []
        self.plungers.append(
            Plunger(Vector2(1200, 800))
        )
        #Kurven erstellen
        self.curves:list[Curve] = []
        self.curves.append(
            Curve(Vector2(WINDOW_WIDTH - Curve.sprite.get_width(), 30))
        )
        self.components:tuple[PinballComponent] = tuple(self.flippers + self.bumpers + self.slopes + self.slingshots 
                                                        + self.stationaryTargets + self.dropTargets 
                                                        + self.plungers + self.curves)
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
        for flipper in self.flippers:
            pygame.gfxdraw.pixel(self.window, int(flipper.pivotPoint.x), int(flipper.pivotPoint.y), (0,255,0))

        pygame.display.update()

    def handleEvents(self):
        """Handling der Events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return
            #Animation von Bumper und Slingshot stoppen
            for component in tuple(self.bumpers + self.slingshots + self.stationaryTargets):
                if event.type == component.timerEvent:
                    component.stopTimer()
                    break
            for dropTarget in self.dropTargets:
                if event.type == dropTarget.timerEvent:
                    self.player.multiplier = 1
                    dropTarget.stopTimer()
                    break

    def handlePressedKeys(self):
        """Handling der gedrückten Tasten"""
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
            if component.__class__ == DropTarget:
                self.checkDropTargets()

    def checkDropTargets(self):
        for dropTarget in self.dropTargets:
            if dropTarget.onField == True:  #Wenn ein Drop Target noch nicht getroffen wurde
                return
        for dropTarget in self.dropTargets:
            self.player.multiplier = 2
            dropTarget.startTimer()


    def run(self):
        """Game-Loop"""
        while self.isRunning == True:
            self.render()
            self.checkCollisions()
            self.moveObjects()
            self.handleEvents()
            self.handlePressedKeys()
            self.clock.tick(60)


main = Main()
main.run()


#Punkteanzahl für alle Komponenten
#Ball sollte man trappen können - aktuell zittert der Ball herum; wenn Flippertaste schnell losgelassen und wieder gedrückt wird, fällt Ball halb durch Flipper
#Slingshot funktioniert von allen Seiten, später eigene Maske für Schräge und andere zwei Seiten
#Ball kann auf Target stuck werden -> viele Punkte. Liegt daran, dass self.correctBallPosition gecallt wird und der Ball wieder über Target ist.
#                                                   Lässt sich vermutlich vermeiden, indem mehrere Masken benutzt werden. Keine Punkte, wenn Ball von oben kommt
#                                                   Bzw. vielleicht auch gar nicht möglich durch Begrenzung von Spielfeld