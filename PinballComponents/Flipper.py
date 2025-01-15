from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


MAX_ROT_ANGLE = 70


class Flipper(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2, direction:int):
        super().__init__(sprite, pos)
        # self.mask = pygame.mask.from_threshold(self.sprite, (255,255,255), (0,0,0,255))
        if self.mask.get_at(self.sprite.get_rect().topleft + Vector2(14,21)):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
            self.pivotPoint = self.pos + Vector2(14, 21)
        else:   #Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
            self.pivotPoint = self.pos + Vector2(177, 20)
        #self.slingVector = self.slopeVector.elementwise() * Vector2(1,-2.5)

        self.originalSprite = self.sprite
        self.originalRect = self.rect
        self.isMoving = False
        self.movingForward = False
        self.rotationAngle = 0
        self.direction = direction

    def collide(self, ball:Ball):
        """Handling der Kollision von Flipper und Ball"""
        #Wenn der Flipper sich gerade nach vorne bewegt, Ball werfen
        if self.movingForward == True and self.rotationAngle < MAX_ROT_ANGLE and self.rotationAngle > -MAX_ROT_ANGLE:
            self.throwBall(ball)
            return
        #Wenn Flipper ganz oben, Ball herunterrutschen
        self.correctBallPosition(ball)
        if self.rotationAngle >= MAX_ROT_ANGLE or self.rotationAngle <= -MAX_ROT_ANGLE:
            """#ball.pos.move_towards_ip(Vector2(ball.pos.x, self.pos.y -42), 200)
            ball.movementVector = Vector2(0,-0.1)"""
            try:
                self.slopeVector.scale_to_length(ball.movementVector.length())
                ball.movementVector = -self.slopeVector.rotate(MAX_ROT_ANGLE)
            except ValueError:  #Nullvektor
                pass
            #ball.movementVector = Vector2(0,0)
            return
        vectorLength = ball.movementVector.length()
        try:
            self.slopeVector.scale_to_length(vectorLength)
            ball.movementVector = self.slopeVector.copy()
        except ValueError:  #Nullvektor
            pass

    def throwBall(self, ball:Ball):
        """Wirft den Ball"""
        #Distanz von überlappendem Pixel zu Spitze des Flippers
        overlappingPixel = self.rect.topleft + self.checkPixelCollision(ball.mask, ball.rect, returnPixel=True)
        if self.direction == 1:
            distance = self.rect.right - overlappingPixel.x
        else:
            distance = overlappingPixel.x - self.rect.left
        #Richtung des Movementvektors
        slingVector = self.slopeVector.rotate(self.direction * pygame.math.lerp(15, MAX_ROT_ANGLE, distance/200))
        slingVector.y *= -1
        movementVector = slingVector
        #Länge des Movementvektors
        movementVector.scale_to_length(pygame.math.lerp(30, 15, distance/200))

        ball.movementVector = movementVector


    def startMoving(self):
        """Setzt Variablen zum Start der Bewegung"""
        self.isMoving = True
        self.movingForward = True

    def move(self):
        """Rotiert den Ball; wenn self.direction = 1: linker Flipper, wenn self.direction = -1: rechter Flipper"""
        if self.movingForward:
            self.rotationAngle += 8 * self.direction
        else:
            self.rotationAngle -= 5 * self.direction
        if self.rotationAngle * self.direction >= MAX_ROT_ANGLE:
            self.rotationAngle = MAX_ROT_ANGLE * self.direction
            self.movingForward = False
        elif self.rotationAngle * self.direction <= 0:
            self.rotationAngle = 0
            self.isMoving = False

        offset = self.originalRect.center - self.pivotPoint
        offset.rotate_ip(-self.rotationAngle)
        self.sprite = pygame.transform.rotate(self.originalSprite, self.rotationAngle)
        rotated_rect = self.sprite.get_rect()
        rotated_rect.center = self.pivotPoint + offset
        self.rect = rotated_rect
        self.mask = pygame.mask.from_surface(self.sprite)