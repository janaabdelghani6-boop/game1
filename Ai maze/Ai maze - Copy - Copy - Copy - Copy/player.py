import pygame
W = 1280
H = 720
WHT, BLU, RED, BLK, GOLD = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (255, 215, 0)
class Player:
    def __init__(self, x, y, all_frames):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.last_safe = self.rect.copy()
        self.last_checkpoint = pygame.Rect(230, 640, 25, 25)
        self.is_dead = False
        self.all_frames = all_frames
        self.frame = 0
        self.timer = 0
        self.row = 0
        self.body_row = 0
        self.current_frame = 2
        self.score = 0

    def update(self, soul_rect, walls, outer_walls, coins, checkpoints, exit_wall, traps, dt):
        if not self.is_dead:
            wall_rects = [w.rect for w in walls]
            outer_rects = [w.rect for w in outer_walls]
            cp_rects = [c.rect for c in checkpoints]

            speed = 7
            dx = soul_rect.centerx - self.rect.centerx
            dy = soul_rect.centery - self.rect.centery

            dist = max(1, (dx**2 + dy**2) ** 0.5)
            step_x = int(dx / dist * min(speed, dist))
            step_y = int(dy / dist * min(speed, dist))

            self.rect.x += step_x
            if (self.rect.collidelist(wall_rects) != -1 or
                self.rect.collidelist(outer_rects) != -1 or
                (self.rect.colliderect(exit_wall.rect) and self.score < 100)):
                self.rect.x -= step_x

            self.rect.y += step_y
            if (self.rect.collidelist(wall_rects) != -1 or
                self.rect.collidelist(outer_rects) != -1 or
                (self.rect.colliderect(exit_wall.rect) and self.score < 100)):
                self.rect.y -= step_y

            if self.rect.collidelist(traps) != -1:
                self.rect = self.last_checkpoint.copy()
                self.is_dead = True
            else:
                self.last_safe = self.rect.copy()

        # Coins
        for coin in coins:
            if not coin.collected and coin.rect.colliderect(self.rect):
                coin.collected = True
                self.score += 20
                coin.coin_sound.play()

        # Checkpoints
        index = self.rect.collidelist(cp_rects)
        if index != -1:
            self.last_checkpoint.center = checkpoints[index].rect.center

        if self.is_dead:
            self.rect = pygame.Rect(self.last_checkpoint.x, self.last_checkpoint.y, 25, 25)
            if soul_rect.colliderect(self.rect):
                self.is_dead = False

        self.timer += dt
        if self.timer > 100:
            self.frame = (self.frame + 1) % 6
            self.timer = 0

    def update_direction(self, mouse_x, mouse_y, prev_mouse_x, prev_mouse_y):
        if mouse_x > prev_mouse_x:
            self.row = 2
        elif mouse_x < prev_mouse_x:
            self.row = 1
        elif mouse_y > prev_mouse_y:
            self.row = 0
        elif mouse_y < prev_mouse_y:
            self.row = 3

        if not self.is_dead:
            self.body_row = self.row

        if mouse_x == prev_mouse_x and mouse_y == prev_mouse_y:
            self.current_frame = 2
        else:
            self.current_frame = self.frame

    def draw(self, screen):
        img = self.all_frames[self.body_row][self.current_frame]
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))

        if self.is_dead:
            font = pygame.font.SysFont("comicsansms", 30)
            line1 = font.render("YOU ARE DEAD!", True, RED)
            line2 = font.render("Please return to your body", True, WHT)
            screen.blit(line1, (W // 2 - line1.get_width() // 2, H // 2 - 40))
            screen.blit(line2, (W // 2 - line2.get_width() // 2, H // 2))
