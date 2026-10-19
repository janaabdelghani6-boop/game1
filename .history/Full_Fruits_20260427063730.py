import random
import pygame

class Fruits():
    def __init__(self):
        self.x = random.uniform(300, 700)
        self.y = 772 # window height
        self.velocityX = random.uniform(-10, 10)
        self.velocityY = random.uniform(-50, -40) # must be negative
        self.gravity = 2
        self.isSpawned = True
        self.isSliced = False # Displays the fruit when it's sliced
        self.spawnSound = pygame.mixer.Sound("audios/show_up.mp3")

    def randomFruitSelection(FFM, bombAppeared):
        if not bombAppeared and random.random() < 0.2:  # 20% chance for bomb to appear
            fruitType = "bomb"
            bombAppeared = True # no 2 bombs appear consecutively
        else:
            fruitType = random.choice([f for f in FFM.keys() if f != "bomb"])
            bombAppeared = False
        return FFM[fruitType](fruitType), bombAppeared
    
    def movement(self):
        self.x += self.velocityX
        self.y += self.velocityY
        self.velocityY += self.gravity

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))

class Bombs(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.radius = 40
        self.hitboxType = "circular"
        self.finished = False
        self.center = (self.x + 42, self.y + 78)
        self.burningSound = pygame.mixer.Sound("audios/burning_fuse.mp3")
        self.explosionSound = pygame.mixer.Sound("audios/explosion.mp3")
        self.burningSound.play()
        self.sprite = pygame.image.load('Fruits_Photo/bomb.png').convert_alpha()
        self.explosionSprite =  pygame.image.load('Fruits_Photo/explosion.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))
        self.spriteDimensions() # to be called once
        self.spriteIndex = 0

    def spriteDimensions(self): # creating a list for each sprite
        self.explosions = []
        # (x, y, width, height)
        spritesData = [
            (0, 0, 110, 170),
            (110, 0, 120, 170),
            (230, 0, 170, 170),
            (400, 0, 200, 170),
            
            (0, 170, 200, 170),
            (200, 170, 170, 170),
            (370, 170, 150, 170),
            (520, 170, 100, 170)
            ]
        for (x, y, w, h) in spritesData:
            frame = self.explosionSprite.subsurface((x, y, w, h))
            self.explosions.append(frame)

    def explosion(self, window):
        if self.spriteIndex == 0:
            self.explosionSound.play()
        if self.spriteIndex >= len(self.explosions):
            self.finished = True
            return
        currentSprite = self.explosions[self.spriteIndex]
        rect = currentSprite.get_rect(center=self.center)
        window.blit(currentSprite, rect)
        self.spriteIndex += 1
        
    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 42, self.y + 78)

class Apples(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.radius = 45
        self.hitboxType = "circular"
        self.center = (self.x + 60, self.y + 65)
        self.sprite = pygame.image.load('Fruits_Photo/apple.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))
    
    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 65) # update circle (hitbox) position

class Coconuts(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.radius = 60
        self.hitboxType = "circular"
        self.center = (self.x + 60, self.y + 60)
        self.sprite = pygame.image.load('Fruits_Photo/coconut.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (120, 120))

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 60) # update circle (hitbox) position

class Pineapples(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.width = 80
        self.height = 120
        self.hitboxType = "rectangular"
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height)
        self.sprite = pygame.image.load('Fruits_Photo/pineapple.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height) # update rect (hitbox) position

class Oranges(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.radius = 55
        self.hitboxType = "circular"
        self.center = (self.x + 75, self.y + 75)
        self.sprite = pygame.image.load('Fruits_Photo/orange.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 75, self.y + 75) # update circle (hitbox) position

class Lemons(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.radius = 40
        self.hitboxType = "circular"
        self.center = (self.x + 53, self.y + 53)
        self.sprite = pygame.image.load('Fruits_Photo/lemon.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 53, self.y + 53) # update circle (hitbox) position

class Pears(Fruits):
    def __init__(self, fruitType):
        super().__init__()
        self.type = fruitType
        self.width = 80
        self.height = 100
        self.hitboxType = "rectangular"
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height)
        self.sprite = pygame.image.load('Fruits_Photo/pear.png').convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (140, 140))
        
    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height) # update rect (hitbox) position