from .PinballComponent import PinballComponent
from Ball import Ball

import pygame
from pygame.math import Vector2


class Slingshot(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)
        if self.mask.get_at(self.sprite.get_rect().topleft + Vector2(1,0)): #Schräge geht von oben links nach unten rechts
            self.slingVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   #Schräge geht von oben rechts nach unten links
            self.slingVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
        self.slingVector.y *= -1

    def collide(self, ball:Ball):
        """Handling der Kollision von Slingshot und Ball"""
        movementVector = self.slingVector
        try:
            movementVector.scale_to_length(14)
            ball.movementVector = movementVector
        except ValueError:  #Nullvektor
            pass
