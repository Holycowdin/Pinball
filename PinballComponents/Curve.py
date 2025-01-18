from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2
import pygame.gfxdraw


WHITE = (255,255,255)
BLACK = (0,0,0)


class Curve(PinballComponent):
    sprite = pygame.Surface(Vector2(300, 300))
    sprite.fill(WHITE)
    sprite.set_colorkey(WHITE)
    pygame.gfxdraw.bezier(sprite, (Vector2(0,0), Vector2(260,40), Vector2(260,300)), 1000, BLACK)
    
    def __init__(self, pos:Vector2):
        self.sprite = Curve.sprite
        self.sprite = self.sprite.convert()
        super().__init__(pos)
        
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
                    ball.isOnField = True
                    return
            ball.move()