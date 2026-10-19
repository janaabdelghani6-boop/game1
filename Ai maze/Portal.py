import pygame

WHT, BLU, RED, BLK, GOLD = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (255, 215, 0)

class portal:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.frame = 0
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer > 100:
            self.frame = (self.frame + 1) % 8
            self.timer = 0

    def draw(self, screen, frames, flip=False):
        img = frames[self.frame].copy()
        if flip:
            img = pygame.transform.flip(img, True, False)  # flip horizontally
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))