from Ball import Ball

import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class PinballComponent():
    """Klasse für alle Pinball-Komponenten, außer Ball"""
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        self.sprite = sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.pos = pos
        self.rect = Rect(self.pos, sprite.get_size())

    def checkRectCollision(self, ballRect: Rect) -> bool:
        """Prüft Kollision der Rects von Ball und Komponente"""
        if self.rect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect) -> bool:
        """Prüft pixelgenaue Kollision für Ball und Komponente; nur gecallt, wenn Rects kollidieren"""
        self.overlappingPixel = ballMask.overlap(self.mask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top))
        if self.overlappingPixel:
            return True

    def correctBallPosition(self, ball:Ball):
        while self.checkAllCollidingPixels(ball.mask, ball.rect) > 1:
            ball.correctPosition()

    def checkAllCollidingPixels(self, ballMask:pygame.Mask, ballRect:Rect) -> bool:
        self.overlappingPixelCount = ballMask.overlap_area(self.mask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top))
        return self.overlappingPixelCount

    def collide(self, ball:Ball):
        raise NotImplementedError