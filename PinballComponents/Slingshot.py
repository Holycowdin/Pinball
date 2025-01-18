from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


class Slingshot(PinballComponent):
    """variant=1: Schräge von links oben nach rechts unten; variant=2: Schräge von recht oben nach links unten"""
    def __init__(self, pos:Vector2, variant:int):
        self.normalSprite = pygame.image.load("Assets/Sprites/Slingshot/Slingshot.png").convert_alpha()
        self.glowingSprite = pygame.image.load("Assets/Sprites/Slingshot/SlingshotGlowing.png").convert_alpha()

        if variant == 2:
            #Sprites spiegeln
            self.normalSprite = pygame.transform.flip(self.normalSprite, True, False)
            self.glowingSprite = pygame.transform.flip(self.glowingSprite, True, False)
        self.sprite = self.normalSprite

        super().__init__(pos)

        if variant == 1:
            self.slingVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:
            self.slingVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
        self.slingVector.y *= -1

        self.time = 125 #Wie lange Slingshot nach Kollision leuchtet
        self.timerEvent = pygame.USEREVENT+3 + variant

    def collide(self, ball:Ball):
        """Handling der Kollision von Slingshot und Ball"""
        movementVector = self.slingVector

        movementVector.scale_to_length(14)
        ball.movementVector = movementVector

        self.sprite = self.glowingSprite
        self.setTimer()

    def setTimer(self):
        pygame.time.set_timer(self.timerEvent, self.time)

    def stopTimer(self):
        self.sprite = self.normalSprite
        pygame.time.set_timer(self.timerEvent, 0)