import pygame
from pygame.math import Vector2
from pygame.rect import Rect

class Ball():
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)

        self.movementVector = Vector2(7, -7)
        self.acceleration = Vector2(0.02, 0.1)

    def move(self):
        """Bewegt den Ball"""
        self.pos += self.movementVector
        self.accelerate(1)

        self.rect.center = self.pos

    def accelerate(self, accelerationSign = 1):
        if (self.movementVector.x > 0) and (self.movementVector.x > self.acceleration.x):
            self.movementVector.x -= self.acceleration.x * accelerationSign 
        elif (self.movementVector.x < 0) and (self.movementVector.x < self.acceleration.x):
            self.movementVector.x += self.acceleration.x * accelerationSign
        else:
            self.movementVector.x = 0
        self.movementVector.y += self.acceleration.y * accelerationSign
        

    def correctPosition(self):
        self.pos += Vector2(0,-1)
        #self.pos.move_towards_ip(self.pos + Vector2(0,-self.rect.height/2), 1)
        self.rect.center = self.pos
        #self.movementVector = Vector2(0,0)
        self.accelerate(-1)
        #self.movementVector -= self.acceleration