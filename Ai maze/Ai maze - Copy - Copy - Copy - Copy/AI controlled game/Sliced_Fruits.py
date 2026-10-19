import random
import pygame

class SlicedLeftFruits():
    def __init__(self, x, y):
        self.leftX = x
        self.leftY = y
        self.leftVelocityX = random.uniform(-10, 0)
        self.leftVelocityY = 0
        self.gravity = 2

    def movementSliced(self):
        self.leftX += self.leftVelocityX
        self.leftY += self.leftVelocityY
        self.leftVelocityY += self.gravity

class SlicedLeftApples(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/appleLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (80, 90))

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

class SlicedLeftCoconuts(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/coconutLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (70, 100))

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

class SlicedLeftPineapples(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/pineappleLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (85, 110))

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

class SlicedLeftOranges(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/orangeLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (80, 120))
        
    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

class SlicedLeftLemons(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/lemonLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (60, 90))

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

class SlicedLeftPears(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = pygame.image.load('Fruits_Photo/pearLeft.png')
        self.leftSprite = pygame.transform.scale(self.leftSprite, (90, 100))

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))

################################################################################################

class SlicedRightFruits():
    def __init__(self, x, y):
        self.rightX = x + 100
        self.rightY = y
        self.rightVelocityX = random.uniform(0, 10)
        self.rightVelocityY = 0
        self.gravity = 2
    
    def movementSliced(self):
        self.rightX += self.rightVelocityX
        self.rightY += self.rightVelocityY
        self.rightVelocityY += self.gravity

class SlicedRightApples(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/appleRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (80, 90))

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))

class SlicedRightCoconuts(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/coconutRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (70, 100))
    
    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))

class SlicedRightPineapples(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/pineappleRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (85, 110))

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))

class SlicedRightOranges(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/orangeRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (80, 120))

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))

class SlicedRightLemons(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/lemonRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 90))

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))

class SlicedRightPears(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = pygame.image.load('Fruits_Photo/pearRight.png')
        self.rightSprite = pygame.transform.scale(self.rightSprite, (90, 100))

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))