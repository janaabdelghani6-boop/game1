import pygame


class GameOver:
    def __init__(self, windowWidth, windowHeight):
        self.gameOver = False

        # game over text
        self.font = pygame.font.SysFont("Arial", 40, True)
        self.gameOverText = self.font.render("GAME OVER", True, (255, 0, 0))
        self.gameOverTextRect = self.gameOverText.get_rect(center=(windowWidth//2, windowHeight//2 - 300))
        # self.scoreText = self.font.render(f"Score: {Score.Score}", True, (255, 255, 0))
        # self.scoreTextRect = self.scoreText.get_rect(center=(windowWidth//2, windowHeight//2 + 200))

        # game over surface
        self.overlay = pygame.Surface((windowWidth, windowHeight))
        self.overlay.set_alpha(150)  # transparency (0-255)
        self.overlay.fill((0, 0, 0))

        # game over sprite (image)
        self.sprite = pygame.image.load("Fruits_Photo/disappointingCat.png")
        self.sprite = pygame.transform.scale(self.sprite, (300, 300))
        self.spriteRect = self.sprite.get_rect(center=(windowWidth//2, windowHeight//2 - 100))

    def display(self, window, windowWidth, windowHeight, score):
        window.blit(self.overlay, (0, 0))
        window.blit(self.gameOverText, self.gameOverTextRect)
        score.drawScoreCentered(window, windowWidth // 2, windowHeight // 2 + 200)
        window.blit(self.sprite, self.spriteRect)