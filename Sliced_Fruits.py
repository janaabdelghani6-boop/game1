import random
import pygame

class SlicedFruits():
    def __init__(self, x, y):
        self.leftX = x
        self.rightX = x + 100
        self.y = y
        self.leftVelocityX = random.uniform(-10, 0)
        self.rightVelocityX = random.uniform(0, 10)
        self.velocityY = 0
        self.gravity = 2
        self.startTime = pygame.time.get_ticks()

    def movementSliced(self):
        self.leftX += self.leftVelocityX
        self.rightX += self.rightVelocityX
        self.y += self.velocityY
        self.velocityY += self.gravity
        self.endTime = pygame.time.get_ticks()

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.y))
        window.blit(self.rightSprite, (self.rightX, self.y))

class SlicedApples(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/appleLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (80, 90))
        
        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/appleRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (80, 90))

class SlicedCoconuts(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/coconutLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (70, 100))
        
        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/coconutRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (70, 100))

class SlicedPineapples(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)

        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/pineappleLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (85, 110))

        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/pineappleRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (85, 110))

class SlicedOranges(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)

        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/orangeLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (80, 120))

        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/orangeRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (80, 120))

class SlicedLemons(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)

        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/lemonLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (60, 90))

        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/lemonRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 90))

class SlicedPears(SlicedFruits):
    def __init__(self, x, y):
        super().__init__(x, y)

        # left sprite and scale
        self.leftSprite = pygame.image.load('Fruits_Photo/pearLeft.png').convert_alpha()
        self.leftSprite = pygame.transform.scale(self.leftSprite, (90, 100))

        # right sprite and scale
        self.rightSprite = pygame.image.load('Fruits_Photo/pearRight.png').convert_alpha()
        self.rightSprite = pygame.transform.scale(self.rightSprite, (90, 100))