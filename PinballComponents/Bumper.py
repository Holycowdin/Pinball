from .PinballComponent import PinballComponent
from Player import Ball

import pygame
from pygame.math import Vector2


class Bumper(PinballComponent):
    """Varianten gehen von 1 bis 3"""
    points = 20

    def __init__(self, pos:Vector2, variant:int):
        self.normalSprite = pygame.image.load(f"Assets/Sprites/Bumper/Bumper{variant}.png").convert_alpha()
        self.glowingSprite = pygame.image.load(f"Assets/Sprites/Bumper/Bumper{variant}Glowing.png").convert_alpha()
        self.sprite = self.normalSprite

        self.time = 125 #Wie lange der Bumper nach Kollision leuchtet
        self.timerEvent = pygame.USEREVENT + variant

        super().__init__(pos)

    def collide(self, ball:Ball):
        """Handling der Kollision von Bumper und Ball"""
        movementVector = ball.pos - Vector2(self.rect.center)
        movementVector.scale_to_length(14)
        ball.movementVector = movementVector

        self.sprite = self.glowingSprite
        self.setTimer()

    def setTimer(self):
        pygame.time.set_timer(self.timerEvent, self.time)

    def stopTimer(self):
        self.sprite = self.normalSprite
        pygame.time.set_timer(self.timerEvent, 0)