import pygame
class FullHearts:
    def __init__(self, i):
        self.x = 950 - i * 60
        self.sprite = pygame.image.load('Fruits_Photo/full heart.png')
        self.sprite = pygame.transform.scale(self.sprite, (70, 70))
    
    def draw(self, window):
        window.blit(self.sprite, (self.x, 10))