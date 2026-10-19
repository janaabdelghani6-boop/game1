import pygame
class soul:
    def __init__(self, x, y, all_frames):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.all_frames = all_frames
        self.frame = 0
        self.timer = 0
        self.row = 0
        self.current_frame = 2

    def update(self, mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt):
        self.rect = pygame.Rect(mouse_x - 12, mouse_y - 12, 25, 25)

        if mouse_x > prev_mouse_x:
            self.row = 2
        elif mouse_x < prev_mouse_x:
            self.row = 1
        elif mouse_y > prev_mouse_y:
            self.row = 0
        elif mouse_y < prev_mouse_y:
            self.row = 3

        if mouse_x == prev_mouse_x and mouse_y == prev_mouse_y:
            self.current_frame = 2
        else:
            self.current_frame = self.frame

        self.timer += dt
        if self.timer > 100:
            self.frame = (self.frame + 1) % 4  # 4 columns
            self.timer = 0

    def draw(self, screen):
        img = self.all_frames[self.row][self.current_frame]
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))