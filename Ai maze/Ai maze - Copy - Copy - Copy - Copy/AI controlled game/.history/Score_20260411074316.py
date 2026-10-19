import pygame
class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 40, True)  # font name, size, bold

    def updateScore(self):
        self.score += 10

    def drawScore(self, window, x, y):
        text = f"Score: {self.score}"
        scoreSurface = self.font.render(text, True, (255, 255, 0))
        window.blit(scoreSurface, (x, y))

    def drawScoreCentered(self, window, center_x, center_y):
        text = f"Score: {self.score}"
        scoreSurface = self.font.render(text, True, (255, 255, 0))
        rect = scoreSurface.get_rect(center=(int(center_x), int(center_y)))
        window.blit(scoreSurface, rect)