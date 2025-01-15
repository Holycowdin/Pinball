from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


class Target(PinballComponent):
    points = 50

    """Spieler bekommt Punkte, wenn er Target trifft"""
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)

    def collide(self, ball:Ball):
        """Handling der Kollision von Target und Ball"""
        self.correctBallPosition(ball)
        ball.movementVector.x *= -1