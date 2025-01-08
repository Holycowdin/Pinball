from .PinballComponent import PinballComponent
from Ball import Ball

import pygame
from pygame.math import Vector2


class Bumper(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)

    def collide(self, ball:Ball):
        """Handling der Kollision von Bumper und Ball"""
        movementVector = ball.pos - Vector2(self.rect.center)
        try:
            movementVector.scale_to_length(14)
            ball.movementVector = movementVector
        except ValueError:  #Nullvektor
            pass