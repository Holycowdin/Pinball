from .PinballComponent import PinballComponent
from Player import Ball
from Mixer import Mixer

import pygame
from pygame.math import Vector2

from enum import Enum, auto


class Wall(PinballComponent):
    class Type(Enum):
        HORIZONTAL = auto()
        VERTICAL = auto()
        CURVED = auto()

    def __init__(self, pos:Vector2, sprite:pygame.Surface, type:Type):
        self.sprite = sprite
        super().__init__(pos)
        self.sprite = pygame.Surface(Vector2(0,0))
        
        self.type = type
        self.sound = Mixer.Sound.COLLISION

    def collide(self, ball:Ball):
        if not ball.isOnField:
            return
        ball.movementVector *= 0.9

        if self.type == Wall.Type.VERTICAL:
            #Position korrigieren
            while self.checkAllOverlappingPixels(ball.mask, ball.rect) > 1:
                ball.pos -= ball.movementVector.normalize()
                ball.rect.center = ball.pos
            #Abprallen lassen
            ball.movementVector.x *= -1

        elif self.type == Wall.Type.HORIZONTAL:
            #Position korrigieren
            ball.pos.move_towards_ip(Vector2(ball.pos.x, self.rect.bottom + ball.rect.height//2), ball.rect.height)
            #Abprallen lassen
            ball.movementVector.y *= -1

        elif self.type == Wall.Type.CURVED:
            #Position korrigieren
            while self.checkAllOverlappingPixels(ball.mask, ball.rect) > 1:
                ball.pos -= ball.movementVector.normalize()
                ball.rect.center = ball.pos
            #Abprallen lassen
            reflectionVector = -ball.movementVector.copy()
            reflectionVector.y *= -1
            ball.movementVector.reflect_ip(reflectionVector)
            ball.movementVector *= -1