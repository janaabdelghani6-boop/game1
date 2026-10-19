import random
import pygame

# ── Image cache ───────────────────────────────────────────────────────────────
_cache: dict = {}

def _img(path: str, w: int, h: int) -> pygame.Surface:
    key = (path, w, h)
    if key not in _cache:
        _cache[key] = pygame.transform.scale(pygame.image.load(path), (w, h))
    return _cache[key]


# ── Left halves ───────────────────────────────────────────────────────────────

class SlicedLeftFruits:
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
        self.leftSprite = _img('Fruits_Photo/appleLeft.png', 80, 90)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


class SlicedLeftCoconuts(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = _img('Fruits_Photo/coconutLeft.png', 70, 100)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


class SlicedLeftPineapples(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = _img('Fruits_Photo/pineappleLeft.png', 85, 110)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


class SlicedLeftOranges(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = _img('Fruits_Photo/orangeLeft.png', 80, 120)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


class SlicedLeftLemons(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = _img('Fruits_Photo/lemonLeft.png', 60, 90)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


class SlicedLeftPears(SlicedLeftFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.leftSprite = _img('Fruits_Photo/pearLeft.png', 90, 100)

    def drawSliced(self, window):
        window.blit(self.leftSprite, (self.leftX, self.leftY))


# ── Right halves ──────────────────────────────────────────────────────────────

class SlicedRightFruits:
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
        self.rightSprite = _img('Fruits_Photo/appleRight.png', 80, 90)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))


class SlicedRightCoconuts(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = _img('Fruits_Photo/coconutRight.png', 70, 100)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))


class SlicedRightPineapples(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = _img('Fruits_Photo/pineappleRight.png', 85, 110)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))


class SlicedRightOranges(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = _img('Fruits_Photo/orangeRight.png', 80, 120)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))


class SlicedRightLemons(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = _img('Fruits_Photo/lemonRight.png', 60, 90)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))


class SlicedRightPears(SlicedRightFruits):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rightSprite = _img('Fruits_Photo/pearRight.png', 90, 100)

    def drawSliced(self, window):
        window.blit(self.rightSprite, (self.rightX, self.rightY))