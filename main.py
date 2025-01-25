from Player import Ball, Player
from PinballComponents import PinballComponent, Flipper, Bumper, Slingshot, Slope, StationaryTarget, DropTarget, Plunger, Curve, Wall
from Mixer import Mixer

import pygame
from pygame.math import Vector2


WINDOW_WIDTH = 1322
WINDOW_HEIGHT = 64*15 + 32

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREY = (180,180,180)


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Magic Pinball")
        pygame.display.set_icon(pygame.image.load("Assets/Sprites/Ball.png").convert_alpha())
        
        self.clock = pygame.time.Clock()
        self.isRunning = True
        #Sound-Mixer initialisieren
        self.mixer = Mixer()
        #Font intialisieren
        self.font = pygame.font.SysFont("Arial", 40)
        #Hintergrund laden
        self.backgroundImage = pygame.image.load("Assets/Sprites/Background.png").convert()
        #Ball erstellen
        self.ball = Ball(Vector2(1247, 700))
        #Flipper erstellen
        self.flippers:list[Flipper] = []
        self.flippers.append(
            Flipper(Vector2(390, 850), direction=1, mixer=self.mixer)
        )
        self.flippers.append(
            Flipper(Vector2(self.flippers[0].rect.right + 100, self.flippers[0].rect.top), direction=-1, mixer=self.mixer)
        )
        #Bumper erstellen
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(Vector2(self.flippers[0].rect.right + 50-40, 150), variant=1)
        )
        self.bumpers.append(
            Bumper(Vector2(self.bumpers[0].rect.centerx - 60-80, self.bumpers[0].rect.centery + 60+40), variant=2)
        )
        self.bumpers.append(
            Bumper(Vector2(self.bumpers[0].rect.centerx + 60, self.bumpers[1].rect.top), variant=3)
        )
        #Slopes erstellen
        self.slopes:list[Slope] = []
        self.slopes.append(
            Slope(Vector2(self.flippers[0].rect.left-250 + 15+8, self.flippers[0].rect.top - 146-3), Slope.Variant.NORMAL_LEFT)
        )
        self.slopes.append(
            Slope(Vector2(self.flippers[1].rect.right-15-8, self.slopes[0].rect.top), Slope.Variant.NORMAL_RIGHT)   #self.flippers[1].rect.right-10, self.flippers[1].rect.top - 146 + 5
        )
        self.slopes.append(
            Slope(Vector2(33, 748), Slope.Variant.EDGE_LEFT)
        )
        self.slopes.append(
            Slope(Vector2(916, self.slopes[-1].rect.top), Slope.Variant.EDGE_RIGHT)
        )
        #Slingshots erstellen
        self.slingshots:list[Slingshot] = []
        self.slingshots.append(
            Slingshot(Vector2(self.flippers[0].rect.left - 120, self.flippers[0].rect.top - 400), Slingshot.Variant.LEFT, self.mixer)
        )
        self.slingshots.append(
            Slingshot(Vector2(self.flippers[1].rect.right, self.slingshots[0].rect.top), Slingshot.Variant.RIGHT, self.mixer)
        )
        #Stationäre Targets erstellen
        self.stationaryTargets:list[StationaryTarget] = []
        self.stationaryTargets.append(
            StationaryTarget(Vector2(self.slopes[0].rect.left, self.bumpers[0].rect.bottom-50), variant=1, index=len(self.stationaryTargets)+1)
        )
        self.stationaryTargets.append(
            StationaryTarget(Vector2(self.slopes[1].rect.right-50, self.bumpers[1].rect.top), variant=2, index=len(self.stationaryTargets)+1)
        )
        #Drop Targets erstellen
        self.dropTargets:list[DropTarget] = []
        self.dropTargets.append(
            DropTarget(Vector2(self.stationaryTargets[0].rect.left - 75, self.stationaryTargets[0].rect.top - 75), variant=1)
        )
        self.dropTargets.append(
            DropTarget(Vector2(self.slopes[1].rect.right - 120//2 - 51/2, self.slopes[1].rect.top - 60), variant=2)
        )
        self.dropTargets.append(
            DropTarget(Vector2(
                                self.bumpers[0].rect.centerx - 51/2, 
                                2*self.bumpers[0].rect.bottom + self.bumpers[0].rect.height - self.bumpers[1].rect.top), 
                        variant=3)
        )
        #Plunger erstellen
        self.plungers:list[Plunger] = []
        self.plungers.append(
            Plunger(Vector2(self.ball.rect.left-20, 802), self.mixer)
        )
        #Kurven erstellen
        self.curves:list[Curve] = []
        self.curves.append(
            Curve(Vector2(923, 34))
        )
        #Wände erstellen
        self.walls:list[Wall] = []
        self.walls.append(
            Wall(Vector2(0,0), pygame.image.load("Assets/Masks/Walls/LeftBorder.png").convert_alpha(), Wall.Type.VERTICAL)
        )
        self.walls.append(
            Wall(Vector2(0,0), pygame.image.load("Assets/Masks/Walls/UpperBorder.png").convert_alpha(), Wall.Type.HORIZONTAL)
        )
        self.walls.append(
            Wall(self.curves[0].rect.topleft, pygame.image.load("Assets/Masks/Walls/StartingWall.png").convert_alpha(), Wall.Type.VERTICAL)
        )
        self.walls.append(
            Wall(Vector2(self.curves[0].rect.left, 100), pygame.image.load("Assets/Masks/Walls/CurvedWall.png").convert_alpha(), Wall.Type.CURVED)
        )
        self.walls.append(
            Wall(self.walls[-1].rect.bottomright - Vector2(3, 0), pygame.image.load("Assets/Masks/Walls/RightBorder.png").convert_alpha(), Wall.Type.VERTICAL)
        )
        del self.walls[-1].sound
        self.components:tuple[PinballComponent] = tuple(self.flippers + self.bumpers + self.slopes + self.slingshots 
                                                        + self.stationaryTargets + self.dropTargets 
                                                        + self.plungers + self.curves + self.walls)
        #Spieler initialisieren
        self.player = Player()

        self.startGame()

    def startGame(self):
        self.ball.pos = Vector2(1247, 700)
        self.ball.rect.center = self.ball.pos
        self.ball.movementVector = Vector2(0,3)
        self.ball.isOnField = False
        
        self.player.resetScore()
        for dropTarget in self.dropTargets:
            dropTarget.stopTimer()

    def render(self):
        """Rendert den gesamten Bildschirm, einschließlich Objekte"""
        self.window.fill(BLACK)
        #Hintergrund rendern
        self.window.blit(self.backgroundImage, Vector2(0,0))
        #Komponenten rendern
        for component in self.components:
            self.window.blit(component.sprite, component.rect)
        #Ball rendern
        self.window.blit(self.ball.sprite, self.ball.rect)
        #Punktanzeige rendern
        scoreText = self.font.render(str(self.player.score), True, WHITE)
        self.window.blit(scoreText, Vector2(self.slopes[2].rect.right - scoreText.get_width() - 16, 
                                            WINDOW_HEIGHT - scoreText.get_height() - 10)
                                            )

        pygame.display.update()

    def handleEvents(self):
        """Handling der Events"""
        for event in pygame.event.get():
            #Programm beenden
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            elif event.type == pygame.KEYDOWN:
                #Programm beenden
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return
                #Musik stummschalten oder entstummen
                elif event.key == pygame.K_m:
                    print("m")
                    self.mixer.switchMusicVolume()
                elif event.key == pygame.K_F2:
                    self.startGame()
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
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.flippers[0].startMoving()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
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
            if flipper.isMoving:
                flipper.move()
        for plunger in self.plungers:
            if plunger.isMoving:
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
            self.playSound(component)
            if component.__class__ == DropTarget:
                self.checkDropTargets()

    def playSound(self, component:PinballComponent):
        """Callt playSound() beim Mixer"""
        if component.__class__ in (Bumper, StationaryTarget, DropTarget, Wall):
            try:
                self.mixer.playSound(component.sound)
            except AttributeError:  #Kein Sound gespeichert
                pass

    def checkDropTargets(self):
        """Schaut, ob alle DropTargets eingesammelt wurden"""
        for dropTarget in self.dropTargets:
            if dropTarget.onField:  #Wenn ein Drop Target noch nicht getroffen wurde
                return
        for dropTarget in self.dropTargets:
            self.player.multiplier = 2
            dropTarget.startTimer()


    def run(self):
        """Game-Loop"""
        while self.isRunning:
            self.render()
            self.checkCollisions()
            self.moveObjects()
            self.handleEvents()
            self.handlePressedKeys()
            self.clock.tick(60)


main = Main()
main.run()


