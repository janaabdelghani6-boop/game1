import pygame
class Timer:
    def __init__(self):
        self.timer = 60
        self.font = pygame.font.SysFont("Arial", 40, True) # font name, size, bold
        # self.start = pygame.time.get_ticks()

    def updateTimer(self, elapsedTime):
        self.timeLeft = self.timer - elapsedTime
        
        if self.timeLeft < 0: # avoiding negative timer value
             self.timeLeft = 0

    def drawTimer(self, window):
        minutes = self.timeLeft // 60
        seconds = self.timeLeft % 60
        timeText = f"Timer: {minutes:02d}:{seconds:02d}" 
        timerSurface = self.font.render(timeText, True, (0, 255, 0))
        window.blit(timerSurface, (20, 20))