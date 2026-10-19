import random
import pygame

FLOOR_Y = 772

# ── Image cache: كل صورة بتتحمل مرة واحدة بس ──────────────────────────────
_cache: dict = {}

def _img(path: str, w: int, h: int) -> pygame.Surface:
    key = (path, w, h)
    if key not in _cache:
        surf = pygame.image.load(path)
        surf = pygame.transform.scale(surf, (w, h))
        _cache[key] = surf
    return _cache[key]


class Fruits:
    def __init__(self):
        self.x = random.uniform(300, 700)
        self.y = FLOOR_Y
        self.velocityX = random.uniform(-10, 10)
        self.velocityY = random.uniform(-50, -35)
        self.gravity = 2
        self.isSliced = False

    def randomFruitSelection(FFM):
        fruit_type = random.choice(list(FFM.keys()))
        return FFM[fruit_type](fruit_type)

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
        self.sprite = _img('Fruits_Photo/apple.png', 120, 120)
        self.center = (self.x + 60, self.y + 65)

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 65)


class Coconuts(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 60
        self.hitboxType = "circular"
        self.sprite = _img('Fruits_Photo/coconut.png', 120, 120)
        self.center = (self.x + 60, self.y + 60)

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 60, self.y + 60)


class Pineapples(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.width = 80
        self.height = 120
        self.hitboxType = "rectangular"
        self.sprite = _img('Fruits_Photo/pineapple.png', 140, 140)
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height)

    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 30, self.y + 20, self.width, self.height)


class Oranges(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 55
        self.hitboxType = "circular"
        self.sprite = _img('Fruits_Photo/orange.png', 140, 140)
        self.center = (self.x + 75, self.y + 75)

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 75, self.y + 75)


class Lemons(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.radius = 40
        self.hitboxType = "circular"
        self.sprite = _img('Fruits_Photo/lemon.png', 100, 100)
        self.center = (self.x + 53, self.y + 53)

    def draw(self, window):
        super().draw(window)
        self.center = (self.x + 53, self.y + 53)


class Pears(Fruits):
    def __init__(self, fruit_type):
        super().__init__()
        self.type = fruit_type
        self.width = 80
        self.height = 100
        self.hitboxType = "rectangular"
        self.sprite = _img('Fruits_Photo/pear.png', 140, 140)
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height)

    def draw(self, window):
        super().draw(window)
        self.rect = pygame.Rect(self.x + 35, self.y + 30, self.width, self.height)