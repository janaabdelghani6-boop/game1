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

    def draw(self, screen, frames, is_current=False):
        img = frames[self.frame].copy()
        
        if is_current:
            # Replace red pixels with green
            arr = pygame.surfarray.pixels3d(img)
            # Find pixels where red is high, green and blue are low (the red flag parts)
            red_mask = (arr[:,:,0] > 100) & (arr[:,:,1] < 100) & (arr[:,:,2] < 100)
            arr[:,:,0][red_mask] = 0    # remove red
            arr[:,:,1][red_mask] = 150  # add green
            arr[:,:,2][red_mask] = 0    # keep blue low
            del arr  # unlock surface
        
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))