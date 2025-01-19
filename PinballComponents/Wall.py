from .PinballComponent import PinballComponent
from Player import Ball

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

    def collide(self, ball:Ball):
        if not ball.isOnField:
            return
        if self.type == Wall.Type.VERTICAL:
            ball.movementVector.x *= -1
        elif self.type == Wall.Type.HORIZONTAL:
            ball.pos.move_towards_ip(Vector2(ball.pos.x, self.rect.bottom + ball.rect.height//2), ball.rect.height)
            ball.movementVector.y *= -1
        elif self.type == Wall.Type.CURVED:
            ball.movementVector *= -1