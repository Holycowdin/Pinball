from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2

class Curve(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)