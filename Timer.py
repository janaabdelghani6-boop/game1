import pygame
class Timer:
    def __init__(self):
        self.timer = 60
        self.timeLeft = 60
        self.font = pygame.font.SysFont("comicsansms", 40, True) # font name, size, bold

    def updateTimer(self, elapsedTime):
        self.timeLeft = self.timer - elapsedTime
        
        if self.timeLeft < 0: # avoiding negative timer value
             self.timeLeft = 0

    def drawTimer(self, window):
        minutes = self.timeLeft // 60
        seconds = self.timeLeft % 60
        timeText = f"Timer: {minutes:02d}:{seconds:02d}" 
        timerSurface = self.font.render(timeText, True, (0, 255, 0))
        timerTextRect = timerSurface.get_rect(center=(150, 40))
        window.blit(timerSurface, timerTextRect)