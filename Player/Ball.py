import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class Ball():
    MAX_SPEED = 25

    def __init__(self, pos:Vector2):
        self.sprite = pygame.image.load("Assets/Sprites/Ball.png").convert_alpha()

        self.pos = pos
        self.rect = Rect(self.pos, self.sprite.get_size())
        self.mask = pygame.mask.from_surface(self.sprite)

        self.movementVector = Vector2(0, 3)
        self.acceleration = Vector2(0.02, 0.1)
        self.isOnField = False
        self.fieldCoordinates = Vector2(0,0)

    def move(self):
        """Bewegt den Ball"""
        if not self.isOnField:
            if self.rect.right <= self.fieldCoordinates.x:
                self.isOnField = True
        self.pos += self.movementVector
        self.accelerate(1)

        self.rect.center = self.pos

    def accelerate(self, accelerationSign = 1):
        """Beschleunigt den Ball positiv oder negativ, je nach accelerationSign"""
        if (self.movementVector.x > 0 and 
            self.movementVector.x > self.acceleration.x):
            #Ball bewegt sich nach rechts, negative Beschleunigung
            self.movementVector.x -= self.acceleration.x * accelerationSign 
        elif (self.movementVector.x < 0 
                and self.movementVector.x < self.acceleration.x):
            #Ball bewegt sich nach links, negative Beschleunigung
            self.movementVector.x += self.acceleration.x * accelerationSign
        else:
            #Negative Beschleunigung soll Ball nicht wieder in andere Richtung lenken
            self.movementVector.x = 0
        self.movementVector.y += self.acceleration.y * accelerationSign

        #Movement-Speed cappen
        if self.movementVector.length() > Ball.MAX_SPEED:
            self.movementVector.scale_to_length(Ball.MAX_SPEED)        

    def correctPosition(self):
        self.pos += Vector2(0,-1)
        self.rect.center = self.pos
        self.accelerate(-1)
