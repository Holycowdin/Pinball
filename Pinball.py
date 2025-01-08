import pygame
from pygame import Rect
import pygame.gfxdraw
from pygame.math import Vector2

WINDOW_WIDTH = 64*20
WINDOW_HEIGHT = 64*15

BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GREY = (180,180,180)


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
        self.slingVector = self.slopeVector.elementwise() * Vector2(1,-2.5)

        self.originalSprite = self.sprite
        self.originalRect = self.rect
        self.isMoving = False
        self.movingForward = False
        self.rotationAngle = 0
        self.direction = direction

    def collide(self, ball:Ball):
        """Handling der Kollision von Flipper und Ball"""
        if self.movingForward == True and self.rotationAngle < 70 and self.rotationAngle > -70:
            self.throwBall(ball)
            return
        self.correctBallPosition(ball)
        if self.rotationAngle >= 70 or self.rotationAngle <= -70:
            """#ball.pos.move_towards_ip(Vector2(ball.pos.x, self.pos.y -42), 200)
            ball.movementVector = Vector2(0,-0.1)"""
            try:
                self.slopeVector.scale_to_length(ball.movementVector.length())
                ball.movementVector = -self.slopeVector.rotate(70)
            except ValueError:
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
        movementVector = self.slingVector
        try:
            movementVector.scale_to_length(28)
            ball.movementVector = movementVector
        except ValueError:  #Nullvektor
            pass

    def startMoving(self):
        self.isMoving = True
        self.movingForward = True

    def move(self):
        """Rotiert den Ball; wenn self.direction = 1: linker Flipper, wenn self.direction = -1: rechter Flipper"""
        if self.movingForward:
            self.rotationAngle += 8 * self.direction
        else:
            self.rotationAngle -= 5 * self.direction
        if self.rotationAngle * self.direction >= 70:
            self.rotationAngle = 70 * self.direction
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


class Bumper(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)

    def collide(self, ball:Ball):
        """Handling der Kollision von Bumper und Ball"""
        movementVector = ball.pos - Vector2(self.rect.center)
        try:
            movementVector.scale_to_length(14)
            ball.movementVector = movementVector
        except ValueError:  #Nullvektor
            pass


class Slope(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)
        if self.mask.get_at(self.sprite.get_rect().topleft):    #Schräge geht von oben links nach unten rechts
            self.slopeVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   #Schräge geht von oben rechts nach unten links
            self.slopeVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)

    def collide(self, ball:Ball):
        """Handling der Kollision von Slope und Ball"""
        vectorLength = ball.movementVector.length()
        try:
            self.slopeVector.scale_to_length(vectorLength)
            ball.movementVector = self.slopeVector.copy()
        except ValueError:  #Nullvektor
            pass


class Slingshot(PinballComponent):
    def __init__(self, sprite:pygame.Surface, pos:Vector2):
        super().__init__(sprite, pos)
        if self.mask.get_at(self.sprite.get_rect().topleft + Vector2(1,0)): #Schräge geht von oben links nach unten rechts
            self.slingVector = Vector2(self.rect.bottomright) - Vector2(self.rect.topleft)
        else:   #Schräge geht von oben rechts nach unten links
            self.slingVector = Vector2(self.rect.bottomleft) - Vector2(self.rect.topright)
        self.slingVector.y *= -1

    def collide(self, ball:Ball):
        """Handling der Kollision von Slingshot und Ball"""
        movementVector = self.slingVector
        try:
            movementVector.scale_to_length(14)
            ball.movementVector = movementVector
        except ValueError:  #Nullvektor
            pass


class Main():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(Vector2(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.isRunning = True
        #Sprites laden
        ballSprite = pygame.image.load("Assets/Sprites/Ball.png").convert_alpha()
        bumperSprite = pygame.image.load("Assets/Sprites/Bumper.png").convert_alpha()
        slopeSprite = pygame.image.load("Assets/Sprites/Line.png").convert_alpha()
        slopeSprite = pygame.transform.flip(slopeSprite, True, False)
        slingshotSprite = pygame.image.load("Assets/Sprites/Slingshot.png").convert_alpha()
        #slingshotSprite = pygame.transform.flip(slingshotSprite, True, False)
        flipperSprite = pygame.image.load("Assets/Sprites/Flipper.png").convert_alpha()
        flipperSprite = pygame.transform.rotate(flipperSprite, 35)
        flipperSprite = pygame.transform.flip(flipperSprite, True, False)
        #Ball erstellen
        self.ball = Ball(ballSprite, Vector2(700, 800)) #700, 800
        #Flipper erstellen
        self.flippers:list[Flipper] = []
        self.flippers.append(
            Flipper(flipperSprite, Vector2(300, 550), 1)
        )
        flipperSprite = pygame.transform.flip(flipperSprite, True, False)
        self.flippers.append(
            Flipper(flipperSprite, Vector2(800, 800), -1)   #300, 800
        )
        #Bumper erstellen
        self.bumpers:list[Bumper] = []
        self.bumpers.append(
            Bumper(bumperSprite, Vector2(650, 50))  #50, 600
        )
        #Slopes erstellen
        self.slopes:list[Slope] = []
        self.slopes.append(
            Slope(slopeSprite, Vector2(970, 510))   #980, 530
        )
        #Slingshots erstellen
        self.slingshots:list[Slingshot] = []
        self.slingshots.append(
            Slingshot(slingshotSprite, Vector2(600, 750))
        )

        self.components:tuple[PinballComponent] = tuple(self.flippers + self.bumpers + self.slopes + self.slingshots)


    def render(self):
        """Rendert den gesamten Bildschirm, einschließlich Objekte"""
        self.window.fill(LIGHT_GREY)
        #Ball rendern
        self.window.blit(self.ball.sprite, self.ball.rect)
        #Komponenten rendern
        for component in self.components:
            self.window.blit(component.sprite, component.rect)
        #self.window.blit(self.flippers[1].mask.to_surface(), self.flippers[1].rect)
        #self.window.blit(self.ball.sprite, self.ball.rect)

        pygame.display.update()

    def userInput(self):
        """Handling vom User-Input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.flippers[0].startMoving()
        if keys[pygame.K_d]:
            self.flippers[1].startMoving()
        

    def moveObjects(self):
        """Callt Methode für Bewegung von Ball und Flipper"""
        self.ball.move()
        for flipper in self.flippers:
            if flipper.isMoving == True:
                flipper.move()

    def checkCollisions(self):
        """Prüft Kollision zwischen Ball und anderen Komponenten"""
        for component in self.components:
            if not component.checkRectCollision(self.ball.rect):
                continue
            if not component.checkPixelCollision(self.ball.mask, self.ball.rect):
                continue
            component.collide(self.ball)


    def run(self):
        """Game-Loop"""
        while self.isRunning == True:
            self.render()
            self.checkCollisions()
            self.moveObjects()
            self.userInput()
            self.clock.tick(60)


main = Main()
main.run()



#Ball sollte man trappen können - aktuell zittert der Ball herum; wenn Flippertaste schnell losgelassen und wieder gedrückt wird, fällt Ball halb durch Flipper
#Ball sollte stärker weggeworfen werden, wenn Ball weiter vorne
#Slingshot funktioniert von allen Seiten, später eigene Maske für Schräge und andere zwei Seiten