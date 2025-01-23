from .PinballComponent import PinballComponent
from Player import Ball
from Mixer import Mixer

import pygame
from pygame.math import Vector2

from enum import IntEnum


class Slingshot(PinballComponent):
    """variant=1: Schräge von links oben nach rechts unten; variant=2: Schräge von recht oben nach links unten"""
    points = 15

    class Variant(IntEnum):
        LEFT = 1
        RIGHT = 2

    def __init__(self, pos:Vector2, variant:Variant, mixer:Mixer):
        self.normalSprite = pygame.image.load("Assets/Sprites/Slingshot/Slingshot.png").convert_alpha()
        self.glowingSprite = pygame.image.load("Assets/Sprites/Slingshot/SlingshotGlowing.png").convert_alpha()

        if variant == Slingshot.Variant.RIGHT:
            #Sprites spiegeln
            self.normalSprite = pygame.transform.flip(self.normalSprite, True, False)
            self.glowingSprite = pygame.transform.flip(self.glowingSprite, True, False)

        self.sprite = self.normalSprite
        super().__init__(pos)

        if variant == Slingshot.Variant.LEFT:
            self.slingVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:
            self.slingVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
        self.slingVector.y *= -1

        self.time = 125 #Wie lange Slingshot nach Kollision leuchtet
        self.timerEvent = pygame.USEREVENT+3 + variant
        self.variant = variant

        self.mixer = mixer

    def collide(self, ball:Ball):
        """Handling der Kollision von Slingshot und Ball"""
        if self.variant == Slingshot.Variant.LEFT:
            if ball.pos.x <= self.rect.left:
                ball.pos.move_towards_ip(Vector2(self.rect.left - ball.rect.width//2, ball.pos.y), ball.rect.height)
                ball.movementVector.x *= -1
                self.mixer.playSound(Mixer.Sound.COLLISION)
                return
        elif self.variant == Slingshot.Variant.RIGHT:
            if ball.pos.x >= self.rect.right:
                ball.pos.move_towards_ip(Vector2(self.rect.right + ball.rect.width//2, ball.pos.y), ball.rect.height)
                ball.movementVector.x *= -1
                self.mixer.playSound(Mixer.Sound.COLLISION)
                return
        
        movementVector = self.slingVector.copy()
        movementVector.scale_to_length(ball.MAX_SPEED-5)
        ball.movementVector = movementVector

        self.sprite = self.glowingSprite
        self.setTimer()
        self.mixer.playSound(Mixer.Sound.SLINGSHOT)

    def setTimer(self):
        pygame.time.set_timer(self.timerEvent, self.time)

    def stopTimer(self):
        self.sprite = self.normalSprite
        pygame.time.set_timer(self.timerEvent, 0)