from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


class Curve(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)
        self.speed = 0

    def collide(self, ball:Ball):
        """Handling der Kollision von Kurve und Ball"""
        if self.speed == 0: #Wenn Kugel noch nicht durchgefahren ist
            if ball.movementVector.length() <= 10:  #Wenn Kugel zu langsam
                #Wieder nach unten bewegen
                ball.movementVector = Vector2(0,1)
                return
            #Wenn nicht zu langsam, Geschwindigkeit speichern
            self.speed = ball.movementVector.length()
            print(self.speed)

        for i in range(int(self.speed)):
            collision = self.checkPixelCollision(ball.mask, ball.rect, returnPixel=True)
            if collision:
                #Kugel von Kurve wegbewegen
                movementVector = (self.rect.topleft + collision) - ball.pos
                movementVector.normalize_ip()
                ball.pos -= movementVector
                #Kurve weiterbewegen
                movementVector.rotate_ip(-45)
                ball.movementVector = movementVector
                if collision.x <= 6:    #Magische Zahl; letzte x-Koordinate, bei der der Ball kollidiert
                    ball.movementVector.x = - self.speed/2
                    return
            ball.move()