import pygame
import Score
class GameOver:
    def __init__(self, windowWidth, windowHeight):
        self.gameOver = False
        self.restartLoadingFlag = False
        self.exitLoadingFlag = False 
        self.restart = False
        self.exit = False
        self.playSound = False
        self.font = pygame.font.Font("fonts/game-over-font/JunkyStyleDripDrip-G3PnA.ttf", 40)

        # restart and exit button
        self.restartText = self.font.render("restart", True, (255, 255, 255))
        self.exitText = self.font.render("exit", True, (255, 255, 255))
        
        self.restartRect = pygame.Rect(0, 0, 200, 60)
        self.exitRect = pygame.Rect(0, 0, 200, 60)
        self.restartRect.center = (windowWidth//2, windowHeight//2 + 200)
        self.exitRect.center = (windowWidth//2, windowHeight//2 + 300)
        self.restartTextRect = self.restartText.get_rect(center = self.restartRect.center)
        self.exitTextRect = self.exitText.get_rect(center = self.exitRect.center)
        
        self.restartLoadingBar = pygame.Rect(0, 0, 0, 60)
        self.exitLoadingBar = pygame.Rect(0, 0, 0, 60)
        self.restartLoadingBar.topleft = self.restartRect.topleft
        self.exitLoadingBar.topleft = self.exitRect.topleft

        # game over surface
        self.overlay = pygame.Surface((windowWidth, windowHeight))
        self.overlay.set_alpha(150)  # transparency (0-255)
        self.overlay.fill((0, 0, 0))

    def gameOverType(self, type, windowWidth, windowHeight):
        if type == "time's up":
            self.gameOverText = self.font.render("TIME'S UP", True, (0, 255, 0))
            self.sprite = pygame.image.load("Fruits_Photo/screamingCat.png").convert_alpha()
            self.sound = pygame.mixer.Sound("audios/times_up.mp3")

        else:
            self.gameOverText = self.font.render("GAME OVER", True, (255, 0, 0))
            self.sprite = pygame.image.load("Fruits_Photo/disappointingCat.png").convert_alpha()
            self.sound = pygame.mixer.Sound("audios/game_over.mp3")

        self.gameOverTextRect = self.gameOverText.get_rect(center=(windowWidth//2, windowHeight//2 - 300))
        self.sprite = pygame.transform.scale(self.sprite, (300, 300))
        self.spriteRect = self.sprite.get_rect(center=(windowWidth//2, windowHeight//2 - 100))

    def buttonTrigger(self):
        """Restart"""
        if self.restartLoadingFlag:
            if self.restartLoadingBar < self.restartRect:
                self.restartLoadingBar.width += 5
            else:
                self.restart = True
            
        if not self.restartLoadingFlag and self.restartLoadingBar.width > 0: 
            self.restartLoadingBar.width -= 5

        """Exit"""
        if self.exitLoadingFlag:
            if self.exitLoadingBar < self.exitRect:
                self.exitLoadingBar.width += 5
            else:
                self.exit = True

        if not self.exitLoadingFlag and self.exitLoadingBar.width > 0:  
            self.exitLoadingBar.width -= 5

    def display(self, window, windowWidth, windowHeight, score):
        window.blit(self.overlay, (0, 0)) # drawing screen

        # drawing restart and exit
        pygame.draw.rect(window, (0, 0, 255), self.restartLoadingBar)
        pygame.draw.rect(window, (0, 0, 255), self.exitLoadingBar)
        pygame.draw.rect(window, (255, 255, 255), self.restartRect, 4)
        pygame.draw.rect(window, (255, 255, 255), self.exitRect, 4)

        # drawing restart and exit text
        window.blit(self.restartText, self.restartTextRect)
        window.blit(self.exitText, self.exitTextRect)

        Score.Score.drawScore(self, window, score, windowWidth//2 + 200, windowHeight//2 + 100)
        Score.Score.drawHighScore(self, window, windowWidth//2 - 200, windowHeight//2 + 100)
        window.blit(self.gameOverText, self.gameOverTextRect) # TIME'S UP or GAME OVER
        window.blit(self.sprite, self.spriteRect)