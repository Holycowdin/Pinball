from .PinballComponent import PinballComponent
from Player import Ball
from Mixer import Mixer

import pygame
from pygame.math import Vector2


class StationaryTarget(PinballComponent):
    """Spieler bekommt Punkte, wenn er Target trifft"""
    points = 50
    sound = Mixer.Sound.STATIONARY_TARGET

    def __init__(self, pos:Vector2, variant:int, index:int):
        self.normalSprite = pygame.image.load("Assets/Sprites/StationaryTarget/StationaryTarget.png").convert_alpha()
        self.glowingSprite = pygame.image.load("Assets/Sprites/StationaryTarget/StationaryTargetGlowing.png").convert_alpha()
        if variant == 2:
            self.normalSprite = pygame.transform.flip(self.normalSprite, True, False)
            self.glowingSprite = pygame.transform.flip(self.glowingSprite, True, False)
        self.sprite = self.normalSprite

        super().__init__(pos)

        self.time = 200   #Zeit, bis das Target nicht mehr leuchtet nach Treffer
        self.timerEvent = pygame.NUMEVENTS - index

    def collide(self, ball:Ball):
        """Handling der Kollision von Target und Ball"""
        speed = ball.movementVector.length()
        speed *= 0.9
        movementVector = ball.pos - Vector2(self.rect.center)
        movementVector.scale_to_length(speed)
        ball.movementVector = movementVector

        self.sprite = self.glowingSprite
        self.startTimer()

    def startTimer(self):
        pygame.time.set_timer(self.timerEvent, self.time)

    def stopTimer(self):
        self.sprite = self.normalSprite
        pygame.time.set_timer(self.timerEvent, 0)

class DropTarget(PinballComponent):
    """Wenn alle 3 Targets getroffen: Targets verschwinden, Multiplikator für Punkte"""
    points = 50
    sound = Mixer.Sound.DROP_TARGET

    def __init__(self, pos:Vector2, variant:int):
        self.normalSprite = pygame.image.load(f"Assets/Sprites/DropTarget/DropTarget{variant}.png").convert_alpha()
        self.sprite = self.normalSprite
        super().__init__(pos)

        self.time = 10 * 1000   #Zeit, bis das Target wieder sichtbar ist nach Treffer
        self.timerEvent = pygame.USEREVENT+5 + variant

        self.onField = True

    def collide(self, ball:Ball):
        self.sprite = pygame.Surface(Vector2(0,0))
        self.createMask()
        self.onField = False

    def createMask(self):
        self.mask = pygame.mask.from_surface(self.sprite)

    def startTimer(self):
        pygame.time.set_timer(self.timerEvent, self.time)

    def stopTimer(self):
        self.sprite = self.normalSprite
        self.onField = True
        self.createMask()
        pygame.time.set_timer(self.timerEvent, 0)

