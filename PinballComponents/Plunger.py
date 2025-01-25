from .PinballComponent import PinballComponent
from Player import Ball
from Mixer import Mixer

import pygame
from pygame import Rect
from pygame.math import Vector2


MAX_OFFSET = 64


class Plunger(PinballComponent):
    def __init__(self, pos:Vector2, mixer:Mixer):
        self.sprite = pygame.image.load("Assets/Sprites/Plunger.png").convert_alpha()
        super().__init__(pos)
        self.borderRect = self.rect.copy()
        self.isMoving = False
        self.isMovingBack = False
        self.movementFactor = 1  # positiv heißt Plunger bewegt sich nach unten, negativ heißt Plunger bewegt sich nach oben

        self.mixer = mixer

    def collide(self, ball:Ball):
        """Handling der Kollision von Plunger und Ball"""
        ball.pos.y = self.pos.y - ball.rect.height//2+1
        ball.rect.center = ball.pos
        ball.movementVector = Vector2(0,-ball.acceleration.y)

    def throwBall(self):
        """Wirft den Ball"""
        self.isMoving = False
        self.ball.pos.y = self.borderRect.top - self.ball.rect.height//2
        self.ball.rect.center = self.ball.pos
        movementVector = Vector2(0, -1)
        movementVector.scale_to_length(self.throwSpeed)
        self.ball.movementVector = movementVector

        self.mixer.playSound(Mixer.Sound.COLLISION)
        
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
        #Maximale Auslenkung
        if self.rect.top >= (self.pos.y + MAX_OFFSET):
            self.rect.top = self.pos.y + MAX_OFFSET
            return
        #Nicht wieder ganz oben
        if not (self.rect.top <= self.pos.y):
            return
        #Plunger wieder ganz oben
        self.rect.top = self.pos.y
        self.isMoving = False
        if self.checkRectCollision(self.ball):
                self.throwBall()

    def checkRectCollision(self, ballRect:Rect) -> bool:
        """Prüft Kollision der Rects von Ball und Komponente"""
        if self.borderRect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect):
        """Keine Pixel-Kollision notwendig"""
        return True