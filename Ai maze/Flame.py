import pygame

class Flame:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.frame = 0
        self.timer = 0
        self.active = True

    def update(self, mouse_x, mouse_y, dt):
        self.rect.center = (mouse_x, mouse_y)
        self.timer += dt
        if self.timer > 100:
            self.frame = (self.frame + 1) % 8
            self.timer = 0

    def draw(self, screen, frames):
        if self.active:
            img = frames[self.frame]
            screen.blit(img, (
                self.rect.centerx - img.get_width() // 2,
                self.rect.centery - img.get_height() // 2
            ))