from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


MAX_OFFSET = 64


class Plunger(PinballComponent):
    def __init__(self, sprite:pygame.sprite, pos:Vector2):
        super().__init__(sprite, pos)
        self.isMoving = False
        self.hasThrown = False
        self.movementFactor = 1  # positiv heißt Plunger bewegt sich nach unten, negativ heißt Plunger bewegt sich nach oben

    def collide(self, ball:Ball):
        """Handling der Kollision von Plunger und Ball"""
        ball.movementVector = Vector2(0,0)

    def throwBall(self):
        """Wirft den Ball"""
        self.isMoving = False
        self.correctBallPosition(self.ball)
        
        movementVector = Vector2(0, -1)
        movementVector.scale_to_length(self.throwSpeed)
        self.ball.movementVector = movementVector

    def startMoving(self, ball:Ball):
        """Startet Bewegung für Plunger"""
        """if self.hasThrown:
            return"""
        self.ball = ball
        self.isMoving = True

    def moveBack(self):
        """Startet die Bewegung zurück"""
        self.hasThrown = True
        self.throwSpeed = pygame.math.lerp(1, 25, (self.rect.top - self.pos.y)/MAX_OFFSET)
        self.movementFactor = -30

    def move(self):
        """Bewegt den Plunger"""
        self.rect.move_ip(0, 1 * self.movementFactor)
        if self.rect.top >= (self.pos.y + MAX_OFFSET):
            self.rect.top = self.pos.y + MAX_OFFSET
        if self.rect.top <= self.pos.y:
            self.rect.top = self.pos.y
            self.throwBall()
        self.correctBallPosition(self.ball)
        