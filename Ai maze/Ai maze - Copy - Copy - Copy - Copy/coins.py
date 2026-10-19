import pygame



class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False
        self.coin_sound = pygame.mixer.Sound('coin_sound.mp3')

    def draw(self, screen, frames, frame_index):
        if not self.collected:
            screen.blit(frames[frame_index], (
                self.rect.centerx - frames[frame_index].get_width() // 2,
                self.rect.centery - frames[frame_index].get_height() // 2
            ))