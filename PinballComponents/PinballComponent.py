from Player import Ball

import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class PinballComponent():
    """Klasse für alle Pinball-Komponenten, außer Ball"""
    points:int = 0

    def __init__(self, pos:Vector2):
        self.sprite:pygame.Surface
        self.mask = pygame.mask.from_surface(self.sprite)
        self.pos = pos
        self.rect = Rect(self.pos, self.sprite.get_size())

    def checkRectCollision(self, ballRect: Rect) -> bool:
        """Prüft Kollision der Rects von Ball und Komponente"""
        if self.rect.colliderect(ballRect):
            return True

    def checkPixelCollision(self, ballMask:pygame.Mask, ballRect:Rect, returnPixel=False) -> bool | Vector2:
        """Prüft pixelgenaue Kollision für Ball und Komponente; nur gecallt, wenn Rects kollidieren"""
        #self.overlappingPixel = ballMask.overlap(self.mask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top))
        overlappingPixel = self.mask.overlap(ballMask, Vector2(ballRect.topleft) - Vector2(self.rect.topleft))
        if overlappingPixel:
            if not returnPixel:
                return True
            return Vector2(overlappingPixel)

    def correctBallPosition(self, ball:Ball):
        """Korrigiert die Ballposition, sodass der Ball nicht in Komponente steckt"""
        while self.checkAllOverlappingPixels(ball.mask, ball.rect) > 1:
            ball.correctPosition()

    def checkAllOverlappingPixels(self, ballMask:pygame.Mask, ballRect:Rect) -> int:
        """Gibt Anzahl überlappender Pixel aus"""
        overlappingPixelCount = ballMask.overlap_area(self.mask, (self.rect.left - ballRect.left, self.rect.top - ballRect.top))
        return overlappingPixelCount

    def collide(self, ball:Ball):
        raise NotImplementedError