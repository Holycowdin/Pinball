from .PinballComponent import PinballComponent
from Player import Ball
from Mixer import Mixer

import pygame
from pygame.math import Vector2


MAX_ROT_ANGLE = 70


class Flipper(PinballComponent):
    sound = Mixer.Sound.COLLISION

    def __init__(self, pos:Vector2, direction:int, mixer:Mixer):
        self.normalSprite = pygame.image.load("Assets/Sprites/Flipper/Flipper.png").convert_alpha()
        self.rotatedSprite = pygame.image.load("Assets/Sprites/Flipper/FlipperRotated.png").convert_alpha()
        #Spiegeln falls nötig
        if direction == 1:
            self.normalSprite = pygame.transform.flip(self.normalSprite, True, False)
            self.rotatedSprite = pygame.transform.flip(self.rotatedSprite, True, False)
        
        self.sprite = self.normalSprite

        super().__init__(pos)
        if self.mask.get_at(self.sprite.get_rect().topleft + Vector2(23, 23)):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
            self.pivotPoint = self.pos + Vector2(23, 23)    #14, 21
        else:   #Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
            self.pivotPoint = self.pos + Vector2(154, 23)   #177, 20

        self.originalSprite = self.sprite
        self.originalRect:pygame.Rect = self.rect
        self.isMoving = False
        self.movingForward = False
        self.rotationAngle = 0
        self.direction = direction

        self.mixer = mixer

    def collide(self, ball:Ball):
        """Handling der Kollision von Flipper und Ball"""
        #Wenn der Flipper sich gerade nach vorne bewegt, Ball werfen
        if self.movingForward == True and self.rotationAngle < MAX_ROT_ANGLE and self.rotationAngle > -MAX_ROT_ANGLE:
            self.throwBall(ball)
            return
        self.correctBallPosition(ball)
        if (self.rotationAngle >= MAX_ROT_ANGLE or 
            self.rotationAngle <= -MAX_ROT_ANGLE):
            #Flipper vollständig ausgelenkt
            collidingPixel = self.checkPixelCollision(ball.mask, ball.rect, returnPixel=True)
            if (collidingPixel and
                collidingPixel.y >= 70 and 
                collidingPixel.y <= 80):
                #Spieler trapt den Ball
                self.trapBall(ball)
                return
            #Ball herunterrutschen
            try:
                self.slopeVector.scale_to_length(ball.movementVector.length())
                ball.movementVector = self.slopeVector.rotate(MAX_ROT_ANGLE) * self.direction
            except ValueError:  #Nullvektor
                pass
            finally:
                return
        #Flipper bewegt sich nicht, Flipper nicht vollständig ausgelenkt
        #Ball herunterrutschen lassen
        vectorLength = ball.movementVector.length()
        try:
            self.slopeVector.scale_to_length(vectorLength)
            ball.movementVector = self.slopeVector.copy()
        except ValueError:  #Nullvektor
            pass

    def trapBall(self, ball:Ball):
        if self.direction == 1:
            ball.pos = Vector2(414,809)
        else:
            ball.pos = Vector2(822,809.6)
        
        ball.movementVector = Vector2(0,0)

    def throwBall(self, ball:Ball):
        """Wirft den Ball"""
        #Distanz von überlappendem Pixel zu Spitze des Flippers
        overlappingPixel = self.rect.topleft + self.checkPixelCollision(ball.mask, ball.rect, returnPixel=True)
        if self.direction == 1:
            distance = self.rect.right - overlappingPixel.x
        else:
            distance = overlappingPixel.x - self.rect.left
        distanceWeight = distance/self.rect.width
        if distanceWeight < 0 or distanceWeight > 1:
            return
        #Richtung des Movementvektors
        slingVector = self.slopeVector.rotate(self.direction * pygame.math.lerp(15, MAX_ROT_ANGLE, distanceWeight))
        slingVector.y *= -1
        movementVector = slingVector
        #Länge des Movementvektors
        movementVector.scale_to_length(pygame.math.lerp(ball.MAX_SPEED, 15, distanceWeight))

        ball.movementVector = movementVector

        self.mixer.playSound(Flipper.sound)

    def startMoving(self):
        """Setzt Variablen zum Start der Bewegung"""
        self.isMoving = True
        self.movingForward = True

    def move(self):
        """Rotiert den Ball; wenn self.direction = 1: linker Flipper, wenn self.direction = -1: rechter Flipper"""
        self.sprite = self.normalSprite
        #rotationAngle verändern
        if self.movingForward:
            self.rotationAngle += 8 * self.direction
        else:
            self.rotationAngle -= 5 * self.direction

        if self.rotationAngle * self.direction >= MAX_ROT_ANGLE:
            #rotationAngle korrigieren, falls zu weit
            self.rotationAngle = MAX_ROT_ANGLE * self.direction
            self.movingForward = False
            #rotierten Sprite speichern
            self.sprite = self.rotatedSprite
        elif self.rotationAngle * self.direction <= 0:
            #rotationAngle korrigieren
            self.rotationAngle = 0
            self.isMoving = False

        offset = self.originalRect.center - self.pivotPoint
        if self.sprite != self.rotatedSprite:
            self.sprite = pygame.transform.rotate(self.originalSprite, self.rotationAngle)
            offset.rotate_ip(-self.rotationAngle)
        else:
            offset.rotate_ip(-self.rotationAngle + (2 * self.direction))
        rotated_rect = self.sprite.get_rect()
        rotated_rect.center = self.pivotPoint + offset
        self.rect = rotated_rect
        self.mask = pygame.mask.from_surface(self.sprite)