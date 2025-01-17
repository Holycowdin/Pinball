from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame import Rect
from pygame.math import Vector2


MAX_OFFSET = 64


class Plunger(PinballComponent):
    def __init__(self, sprite:pygame.sprite, pos:Vector2):
        super().__init__(sprite, pos)
        self.borderRect = self.rect.copy()
        self.isMoving = False
        self.isMovingBack = False
        self.movementFactor = 1  # positiv heißt Plunger bewegt sich nach unten, negativ heißt Plunger bewegt sich nach oben

    def collide(self, ball:Ball):
        """Handling der Kollision von Plunger und Ball"""
        ball.pos.y = self.pos.y - ball.rect.height//2+1
        ball.rect.center = ball.pos
        ball.movementVector = Vector2(0,-ball.acceleration.y)

    def throwBall(self):
        """Wirft den Ball"""
        self.isMoving = False
        self.correctBallPosition(self.ball)
        print(self.throwSpeed)
        movementVector = Vector2(0, -1)
        movementVector.scale_to_length(self.throwSpeed)
        self.ball.movementVector = movementVector
        
    def startMoving(self, ball:Ball):
        """Startet Bewegung für Plunger"""
        if self.isMoving:
            return
        self.ball = ball
        self.isMoving = True
        self.isMovingBack = False
        self.movementFactor = 1

    def moveBack(self):
        """Startet die Bewegung zurück"""
        self.throwSpeed = pygame.math.lerp(1, 25, (self.rect.top - self.pos.y)/MAX_OFFSET)
        self.movementFactor = -30
        self.isMovingBack = True

    def move(self):
        """Bewegt den Plunger"""
        self.rect.move_ip(0, 1 * self.movementFactor)
        if self.rect.top >= (self.pos.y + MAX_OFFSET):
            self.rect.top = self.pos.y + MAX_OFFSET
        if self.rect.top <= self.pos.y:
            self.rect.top = self.pos.y
            self.isMoving = False
            if self.checkPixelCollision(self.ball.mask, self.ball.rect, plungerCollision=True):
                self.throwBall()
        self.correctBallPosition(self.ball)

    def checkRectCollision(self, ballRect:Rect) -> bool:
        """Prüft Kollision der Rects von Ball und Komponente"""
        if self.borderRect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect, plungerCollision=False):
        if not plungerCollision:
            return True
        self.overlappingPixel = self.mask.overlap(ballMask, (ballRect.left - self.rect.left, ballRect.top - self.rect.top))
        if self.overlappingPixel:
            return True