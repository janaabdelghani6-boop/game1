import pygame

pygame.init()
W = 1280
H = 720
WHT, BLU, RED, BLK, GOLD = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (255, 215, 0)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Maze")
level_over = False
exit_open = False
is_ready = False


def get_sprite(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image.convert_alpha()


def get_player_sprite(sheet, frame, row, width, height, scale, color):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (frame * width, row * height, width, height))
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    image.set_colorkey(color)
    return image.convert_alpha()


class Wall:
    def __init__(self, x, y, w, h, color=GOLD):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False

    def draw(self, screen, frames, frame_index):
        if not self.collected:
            screen.blit(frames[frame_index], (
                self.rect.centerx - frames[frame_index].get_width() // 2,
                self.rect.centery - frames[frame_index].get_height() // 2
            ))


class Checkpoint:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, BLU, self.rect)


class Player:
    def __init__(self, x, y, all_frames, all_soul_frames):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.last_safe = self.rect.copy()
        self.last_checkpoint = pygame.Rect(x, y, 25, 25)
        self.is_dead = False
        self.all_frames = all_frames
        self.all_soul_frames = all_soul_frames
        self.Player_frame = 0
        self.Soul_frame = 0
        self.timer = 0
        self.soul_row = 0
        self.score = 0

    def update(self, soul_rec, walls, outer_walls, coins, checkpoints, dt):
        if not self.is_dead:
            wall_rects = [w.rect for w in walls]
            outer_rects = [w.rect for w in outer_walls]
            cp_rects = [c.rect for c in checkpoints]

            if self.rect.collidelist(wall_rects) != -1:
                self.rect = self.last_checkpoint.copy()
                self.is_dead = True
            else:
                new_pos = soul_rec.copy()

                if new_pos.collidelist(outer_rects) == -1 and new_pos.collidelist(wall_rects) == -1:
                    self.rect = new_pos
                    self.last_safe = self.rect.copy()
                else:
                    self.rect = self.last_safe.copy()
                    pygame.mouse.set_pos((self.last_safe.centerx, self.last_safe.centery))




                for coin in coins:
                    if not coin.collected and coin.rect.colliderect(self.rect):
                        coin.collected = True
                        self.score += 20

                index = self.rect.collidelist(cp_rects)
                if index != -1:
                    self.last_checkpoint.center = checkpoints[index].rect.center

        # this runs regardless — freezes body at checkpoint when dead
        if self.is_dead:
            self.rect = pygame.Rect(self.last_checkpoint.x, self.last_checkpoint.y, 25, 25)
            if soul_rec.colliderect(self.rect):
                self.is_dead = False

        self.timer += dt
        if self.timer > 100:
            self.Player_frame = (self.Player_frame + 1) % 6
            self.Soul_frame = (self.Soul_frame + 1) % 4
            self.timer = 0

    def update_direction(self, mouse_x, mouse_y, prev_mouse_x, prev_mouse_y):
        if mouse_x > prev_mouse_x:
            self.soul_row = 2
        elif mouse_x < prev_mouse_x:
            self.soul_row = 1
        elif mouse_y > prev_mouse_y:
            self.soul_row = 0
        elif mouse_y < prev_mouse_y:
            self.soul_row = 3

        if mouse_x == prev_mouse_x and mouse_y == prev_mouse_y:
            self.current_frame = 2
        else:
            self.current_frame = self.Player_frame

    def draw(self, screen, soul_rec):
        if self.is_dead:
            screen.blit(self.all_frames[self.soul_row][2], (
                self.rect.centerx - self.all_frames[self.soul_row][2].get_width() // 2,
                self.rect.centery - self.all_frames[self.soul_row][2].get_height() // 2
            ))
            screen.blit(self.all_soul_frames[self.soul_row][self.current_frame], (
                soul_rec.centerx - self.all_soul_frames[self.soul_row][self.current_frame].get_width() // 2,
                soul_rec.centery - self.all_soul_frames[self.soul_row][self.current_frame].get_height() // 2
            ))
        else:
            screen.blit(self.all_frames[self.soul_row][self.current_frame], (
                self.rect.centerx - self.all_frames[self.soul_row][self.current_frame].get_width() // 2,
                self.rect.centery - self.all_frames[self.soul_row][self.current_frame].get_height() // 2
            ))


# load sprites
Player_Sprite = pygame.image.load('player.png').convert_alpha()
all_player_frames = []
for row in range(4):
    row_frames = []
    for i in range(6):
        row_frames.append(get_player_sprite(Player_Sprite, i, row, 137, 137, 0.4, BLK))
    all_player_frames.append(row_frames)

#soul sprite
Soul_sprite = pygame.image.load('Soul.png').convert_alpha()
all_soul_frames = []
for row in range(4):
    row_frames = []
    for i in range(4):
        frame = get_player_sprite(Soul_sprite, i, row, 64, 64, 0.4, BLK)
        row_frames.append(frame)
    all_soul_frames.append(row_frames)

Coin_Sprite = pygame.image.load('coin.png').convert_alpha()
coin_frames = []
for i in range(5):
    coin_frames.append(get_sprite(Coin_Sprite, i, 64, 64, .85, BLK))
coin_frame = 0
coin_timer = 0

# create objects
walls = [
    Wall(175, 540, 155, 5), Wall(445, 450, 5, 265), Wall(265, 450, 180, 5),
    Wall(175, 330, 670, 5), Wall(595, 330, 5, 290), Wall(845, 270, 5, 230),
    Wall(715, 465, 5, 260), Wall(845, 590, 5, 135), Wall(1025, 550, 250, 5),
    Wall(1025, 410, 5, 235), Wall(1025, 410, 80, 5), Wall(1105, 410, 5, 85),
    Wall(935, 290, 5, 190), Wall(935, 290, 255, 5), Wall(1190, 290, 5, 205),
    Wall(805, 200, 470, 5), Wall(805, 70, 5, 130), Wall(625, 70, 180, 5),
    Wall(710, 175, 5, 155), Wall(625, 70, 5, 115), Wall(445, 180, 180, 5),
    Wall(505, 60, 5, 120), Wall(445, 120, 5, 60), Wall(332, 5, 5, 250),
    Wall(175, 120, 85, 5), Wall(255, 70, 5, 50), Wall(255, 250, 270, 5),
    Wall(335, 57, 70, 5), Wall(570, 113, 55, 5), Wall(895, 5, 5, 120),
    Wall(895, 120, 290, 5), Wall(1180, 70, 5, 50), Wall(1080, 5, 5, 65),
    Wall(995, 65, 5, 55),
]

outer_walls = [
    Wall(175, 0, 1100, 5), Wall(175, 0, 5, 545), Wall(175, 645, 5, 70),
    Wall(1275, 0, 5, 720), Wall(175, 715, 1100, 5),
]

coins = [
    Coin(210, 80), Coin(1055, 450), Coin(930, 80),
    Coin(585, 145), Coin(1050, 580),
]

checkpoints = [
    Checkpoint(845, 500, 5, 90), Checkpoint(845, 205, 5, 85),
    Checkpoint(595, 620, 5, 95), Checkpoint(525, 250, 5, 80),
    Checkpoint(805, 5, 5, 65),
]

exit_wall = Wall(175, 400, 5, 100)
out_rect = Wall(75, 400, 25, 100)


player = Player(100, 595, all_player_frames, all_soul_frames)

# ui
label_font = pygame.font.SysFont("comicsansms", 20)
label_surface = label_font.render("Time", True, WHT)
timer_font = pygame.font.SysFont("comicsansms", 35)
be_ready_lable = label_font.render("Please go to the start point", True, WHT)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
prev_mouse_x, prev_mouse_y = 0, 0

running = True
while running:
    screen.fill(BLK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    soul_rec = pygame.Rect(mouse_x - 12, mouse_y - 12, 25, 25)

    # coin animation
    coin_timer += dt
    if coin_timer > 100:
        coin_frame = (coin_frame + 1) % 5
        coin_timer = 0

    # update
    player.update(soul_rec, walls, outer_walls, coins, checkpoints, dt)
    player.update_direction(mouse_x, mouse_y, prev_mouse_x, prev_mouse_y)

    # clock
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = f"{elapsed // 60:02}:{elapsed % 60:02}"
    score_label = label_font.render("Score: " + str(player.score), True, WHT)
    time_surface = timer_font.render(time_text, True, WHT)

    # draw
    for coin in coins:
        coin.draw(screen, coin_frames, coin_frame)

    for wall in walls:
        wall.draw(screen)

    for wall in outer_walls:
        wall.draw(screen)

    # for cp in checkpoints:
    #     cp.draw(screen)

    player.draw(screen, soul_rec)

    screen.blit(label_surface, (10, 3))
    screen.blit(time_surface, (15, 50))
    screen.blit(score_label, (5, 150))

    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y
    pygame.display.update()

pygame.quit()