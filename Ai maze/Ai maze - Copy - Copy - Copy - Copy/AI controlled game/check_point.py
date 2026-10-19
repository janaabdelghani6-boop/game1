import pygame

class Checkpoint:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.frame = 0
        self.timer = 0
        
    def update(self, dt):
        self.timer += dt
        if self.timer > 100:
            self.frame = (self.frame + 1) % 5
            self.timer = 0

    def draw(self, screen, frames):
        img = frames[self.frame]
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))