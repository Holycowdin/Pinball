from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


class Slope(PinballComponent):
    def __init__(self, pos:Vector2):
        self.sprite = pygame.image.load("Assets/Sprites/Line.png").convert_alpha()
        self.sprite = pygame.transform.flip(self.sprite, True, False)
        super().__init__(pos)
        
        if self.mask.get_at(self.sprite.get_rect().topleft):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   #Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)

    def collide(self, ball:Ball):
        """Handling der Kollision von Slope und Ball"""
        vectorLength = ball.movementVector.length()
        try:
            self.slopeVector.scale_to_length(vectorLength)
            ball.movementVector = self.slopeVector.copy()
        except ValueError:  #Nullvektor
            pass