import random
import pygame

# يُضبط من Main عند تغيير حجم الشاشة
FLOOR_Y = 772

class Fruits():
    def __init__(self):
        self.x = random.uniform(300, 700)
        self.y = FLOOR_Y
        self.velocityX = random.uniform(-10, 10)
        self.velocityY = random.uniform(-50, -35)
        self.gravity = 2
        self.isSliced = False # Displays the fruit when it's sliced

    def randomFruitSelection(FFM):
        fruit_type = random.choice(list(FFM.keys()))
        fruit_class = FFM[fruit_type]
        return fruit_class(fruit_type)
    
    def movement(self):
        self.x += self.velocityX
        self.y += self.velocityY
        self.velocityY += self.gravity

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

class Apples(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 45
        self.hitboxType = "circular"
        self.center = (self.x + 60, self.y + 65)
        self.sprite = pygame.image.load('Fruits_Photo/apple.png')
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))
    
    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 65) # update circle (hitbox) position

class Coconuts(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 60
        self.hitboxType = "circular"
        self.center = (self.x + 60, self.y + 60)
        self.sprite = pygame.image.load('Fruits_Photo/coconut.png')
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 60) # update circle (hitbox) position

class Pineapples(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.width = 80
        self.height = 120
        self.hitboxType = "rectangular"
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height)
        self.sprite = pygame.image.load('Fruits_Photo/pineapple.png')
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height) # update rect (hitbox) position

class Oranges(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 55
        self.hitboxType = "circular"
        self.center = (self.x + 75, self.y + 75)
        self.sprite = pygame.image.load('Fruits_Photo/orange.png')
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 75, self.y + 75) # update circle (hitbox) position

class Lemons(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 40
        self.hitboxType = "circular"
        self.center = (self.x + 53, self.y + 53)
        self.sprite = pygame.image.load('Fruits_Photo/lemon.png')
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 53, self.y + 53) # update circle (hitbox) position

class Pears(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.width = 80
        self.height = 100
        self.hitboxType = "rectangular"
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height)
        self.sprite = pygame.image.load('Fruits_Photo/pear.png')
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height) # update rect (hitbox) position