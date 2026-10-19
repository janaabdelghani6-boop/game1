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
        self.is_teleporting = False
        self.level_2 = False
        self.entered_portal = -1
        self.teleport_cooldown = 0

    def update(self, soul_rect, walls, outer_walls, coins, checkpoints, exit_wall, traps, dt, portals = None):
        wall_rects = [w.rect for w in walls]
        outer_rects = [w.rect for w in outer_walls]
        cp_rects = [c.rect for c in checkpoints]

        if not self.is_dead and not self.is_teleporting:
           
            if not portals == None:
                self.level_2 = True
                tps = [tp.rect for tp in portals]
                

            speed = 7
            dx = soul_rect.centerx - self.rect.centerx
            dy = soul_rect.centery - self.rect.centery

            dist = max(1, (dx**2 + dy**2) ** 0.5)
            step_x = int(dx / dist * min(speed, dist))
            step_y = int(dy / dist * min(speed, dist))

            self.rect.x += step_x
            
            if not self.level_2 :
                    
                if (self.rect.collidelist(wall_rects) != -1 or
                    self.rect.collidelist(outer_rects) != -1 or
                    (self.rect.colliderect(exit_wall.rect) and self.score < 100)):
                    self.rect.x -= step_x

                self.rect.y += step_y
                if (self.rect.collidelist(wall_rects) != -1 or
                    self.rect.collidelist(outer_rects) != -1 or
                    (self.rect.colliderect(exit_wall.rect) and self.score < 100)):
                    self.rect.y -= step_y


            else:
                    
                    if (self.rect.collidelist(wall_rects) != -1 or
                        self.rect.collidelist(outer_rects) != -1 or
                        (self.rect.colliderect(exit_wall.rect) and self.score < 120)):
                        self.rect.x -= step_x

                    self.rect.y += step_y
                    if (self.rect.collidelist(wall_rects) != -1 or
                        self.rect.collidelist(outer_rects) != -1 or
                        (self.rect.colliderect(exit_wall.rect) and self.score < 120)):
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

        if portals and len(portals) == 2:
            if not self.is_teleporting:
                self.teleport_cooldown -= dt
                if self.rect.colliderect(portals[0].rect) and self.teleport_cooldown <= 0:
                    self.is_teleporting = True
                    self.entered_portal = 0
                    self.teleport_cooldown = 2000  
                elif self.rect.colliderect(portals[1].rect) and self.teleport_cooldown <= 0:
                    self.is_teleporting = True
                    self.entered_portal = 1
                    self.teleport_cooldown = 2000 
            else:
                exit_portal = 1 if self.entered_portal == 0 else 0
                if soul_rect.colliderect(portals[exit_portal].rect):
                    if exit_portal == 1:
                        self.rect.centerx = portals[exit_portal].rect.centerx - 30
                    else:
                        self.rect.centerx = portals[exit_portal].rect.centerx + 30
                    self.rect.centery = portals[exit_portal].rect.centery
                    self.is_teleporting = False
                    self.entered_portal = -1
                    self.teleport_cooldown = 2000
                                    
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

    def update_direction(self, soul_rect):
        dx = soul_rect.centerx - self.rect.centerx
        dy = soul_rect.centery - self.rect.centery

        if not self.is_dead:
            if abs(dx) > abs(dy):  
                if dx > 2:
                    self.row = 2   
                elif dx < -2:
                    self.row = 1   
            else:                  
                if dy > 2:
                    self.row = 0   
                elif dy < -2:
                    self.row = 3   

            self.body_row = self.row

        if abs(dx) < 2 and abs(dy) < 2:
            self.current_frame = 2  # idle frame
        else:
            self.current_frame = self.frame

    def draw(self, screen):
        img = self.all_frames[self.body_row][self.current_frame]
        screen.blit(img, (
            self.rect.centerx - img.get_width() // 2,
            self.rect.centery - img.get_height() // 2
        ))

        font = pygame.font.SysFont("comicsansms", 30)
        if self.is_dead:
            line1 = font.render("YOU ARE DEAD!", True, RED)
            line2 = font.render("Please return to your body", True, WHT)
            screen.blit(line1, (W // 2 - line1.get_width() // 2, H // 2 - 40))
            screen.blit(line2, (W // 2 - line2.get_width() // 2, H // 2))

        if self.is_teleporting:
            line2 = font.render("Please go to the portal", True, WHT)
            screen.blit(line2, (W // 2 - line2.get_width() // 2, H // 2))
