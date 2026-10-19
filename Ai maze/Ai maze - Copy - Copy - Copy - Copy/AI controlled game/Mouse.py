import pygame

class Mouse():
    def __init__(self):
        self.previousPos = pygame.mouse.get_pos() 

    def mouseTracking(self):
        self.currentPos = pygame.mouse.get_pos()
        self.dx = self.currentPos[0] - self.previousPos[0]
        self.dy = self.currentPos[1] - self.previousPos[1]
        self.speed = ((self.dx ** 2 + self.dy ** 2) ** 0.5) # calculating speed of the swipe
        self.previousPos = self.currentPos

    def draw(self, window):
        pygame.draw.circle(window, (0, 0, 255), self.currentPos, 10)
