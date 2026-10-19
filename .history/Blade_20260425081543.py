import pygame
from Hand_Tracker import (
    init_blade,
    tick_blade,
    blade_current_pos,
    shutdown_hand_tracker
)

class Blade:
    def __init__(self, windowWidth, windowHeight):
        self.surface = pygame.Surface((windowWidth, windowHeight), pygame.SRCALPHA) # srcalpha supports transparency per pixel
        init_blade(windowWidth // 2, windowHeight // 2) # blade starts at center
        self.steps = 10
        self.sound = pygame.mixer.Sound("audios/slicing.mp3")
        self.bladePoints = []

    def circularCollision(p1, p2, cx, cy, r): # p1 ---> previous position, p2 ---> current position, (cx, cy) ---> circle's center, r ---> radius
        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1 # movement direction
        """
        x = p1[0] + t * dx 
        y = p1[1] + t * dy # distance to a point with same direction but different magnitude

        (x - cx) ** 2 + (y - cy) ** 2 = r ** 2
        (p1[0] + t*dx - cx)  ** 2 + (p1[1] + t*dy - cy) ** 2 = r ** 2, let fx = p1[0] - cx and fy = p1[1] - cy
        """
        fx = p1[0] - cx 
        fy = p1[1] - cy # distance between blade and center
        """
        (fx + t*dx) ** 2 + (fy + t*dy) ** 2 = r ** 2
        fx*fx + 2*fx*dx*t + t*dx*t*dx + fy*fy + 2*fy*dy*t + t*dy*t*dy = r*r
        (dx*dx + dy*dy) * t*t + 2*(fx*dx + fy*dy) * t + (fx*fx + fy*fy - r*r) = 0              ## circle equation
        """
        a = dx*dx + dy*dy # Quadratic coefficients
        b = 2*(fx*dx + fy*dy)
        c = (fx*fx + fy*fy - r*r)

        if a == 0: # a = 0 when p1 = p2 (no change in the position)
            return (fx*fx + fy*fy) <= r*r

        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return False # No intersection
    
        discriminant **= 0.5
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a) # getting points of intersection

        if (0 <= t1 <= 1) or (0 <= t2 <= 1):
            return True # intersection is within segment
        return False
    
    def update(self, windowWidth, windowHeight):
        tick_blade(windowWidth, windowHeight)
        raw = blade_current_pos()

        if not self.bladePoints:
            smooth = raw
        else:
            prev = self.bladePoints[-1]
            alpha = 0.4  # (0 = very smooth but laggy, 1 = raw)

            smooth = (prev[0] + (raw[0] - prev[0]) * alpha, prev[1] + (raw[1] - prev[1]) * alpha)

        self.bladePoints.append(smooth)

        # limit trail length
        if len(self.bladePoints) > 8:
            self.bladePoints.pop(0)

    def subpoints(self, p1, p2, t): # adding subpoints between points for smoother blade
        return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)

    def draw(self, window):
        smoothPoints = []
        self.surface.fill((0, 0, 0, 0)) # clear old surface

        for i in range(1, len(self.bladePoints)):
            for j in range(self.steps):
                t = j / self.steps
                smoothPoints.append(self.subpoints(self.bladePoints[i - 1], self.bladePoints[i], t))

        if len(smoothPoints) > 1: # divisor must be positive
            for j in range(1, len(smoothPoints)):
                ratio = j / (len(smoothPoints) - 1) # 0 < ratio <= 1
                fade = 255 * ratio # 0 < fade <= 255
                thickness = int((23 * ratio) + 2) # 2 < t <= 25
                pygame.draw.line(self.surface, (255, 255, 255, fade), smoothPoints[j - 1], smoothPoints[j], thickness)
        window.blit(self.surface, (0, 0))

    def terminate():
        shutdown_hand_tracker()