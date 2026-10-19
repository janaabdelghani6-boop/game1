import pygame
class Score:
    def __init__(self):
        self.score = 0
        self.comboCount = 1
        self.lastSliceTime = 0
        self.comboStartTime = 0
        self.comboDuration = 1000
        self.comboText = None
        self.soundFlag = False
        self.font = pygame.font.SysFont("comicsansms", 40, True)  # system font name, size, bold
        self.comboSound = pygame.mixer.Sound("audios/combo.mp3")
        self.combo = pygame.font.Font("fonts/combo-font/GokartBubble-XGlLG.otf", 40) # downloaded font

    def updateScore(self, currentTime, x, y):
        if currentTime - self.lastSliceTime < 600: # 600ms = 0.6s
            self.comboCount += 1
            self.soundFlag = True
        else:
            self.comboCount = 1
        self.lastSliceTime = currentTime
        
        if self.comboCount > 2:
            self.score += self.comboCount * 10
            self.comboText = self.combo.render(f"COMBO X{self.comboCount}", True, (255, 0, 255))
            self.comboTextRect = self.comboText.get_rect(center = (x, y - 100))
            self.comboStartTime = currentTime
        self.score += 10

    def drawScore(self, window, score, x, y):
        text = f"Score: {score}"
        scoreSurface = self.font.render(text, True, (255, 255, 0))
        scoreTextRect = scoreSurface.get_rect(center=(x, y))
        window.blit(scoreSurface, scoreTextRect)

    def drawCombo(self, window, currentTime):
        if self.comboText:
            if currentTime - self.comboStartTime < self.comboDuration: # combo text will be displayed for 1 sec
                if self.soundFlag:
                    self.comboSound.play()
                    self.soundFlag = False

                window.blit(self.comboText, self.comboTextRect)
            else:
                self.comboText = None