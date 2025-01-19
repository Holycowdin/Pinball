from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2

from enum import Enum, auto


class Slope(PinballComponent):
    class Variant(Enum):
        NORMAL_LEFT = auto()
        NORMAL_RIGHT = auto()
        EDGE_LEFT = auto()
        EDGE_RIGHT = auto()

    def __init__(self, pos:Vector2, variant:Variant):
        if (variant == Slope.Variant.NORMAL_LEFT) or (variant == Slope.Variant.NORMAL_RIGHT):
            self.sprite = pygame.image.load("Assets/Sprites/Slope.png").convert_alpha()
        else:
            self.sprite = pygame.image.load("Assets/Masks/EdgeSlope.png").convert_alpha()
        
        if (variant == Slope.Variant.NORMAL_LEFT) or (variant == Slope.Variant.EDGE_RIGHT):
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        super().__init__(pos)
        
        if (variant == Slope.Variant.NORMAL_LEFT) or (variant == Slope.Variant.EDGE_LEFT):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   #Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)

        if (variant == Slope.Variant.EDGE_LEFT) or (variant == Slope.Variant.EDGE_RIGHT):
            self.sprite = pygame.Surface(Vector2(0,0))  #Surface löschen, da sowieso angezeigt wird

    def collide(self, ball:Ball):
        """Handling der Kollision von Slope und Ball"""
        ball.correctPosition()
        vectorLength = ball.movementVector.length()
        try:
            self.slopeVector.scale_to_length(vectorLength)
            ball.movementVector = self.slopeVector.copy()
        except ValueError:  #Nullvektor
            pass