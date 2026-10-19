import pygame
from player import Player
from Wall import Wall
from Soul import soul
from check_point import Checkpoint
from coins import Coin
from Hand_Tracker import init_blade, tick_blade, blade_current_pos, shutdown_hand_tracker
import math

pygame.init()
pygame.mixer.init()

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


flag_sprite = pygame.image.load('flag animation.png').convert_alpha()

        
# load sprites
Player_Sprite = pygame.image.load('player.png').convert_alpha()
all_player_frames = []
for row in range(4):
    row_frames = []
    for i in range(6):
        row_frames.append(get_player_sprite(Player_Sprite, i, row, 137, 137, 0.4, BLK))
    all_player_frames.append(row_frames)

Soul_Sprite = pygame.image.load('Soul.png').convert_alpha()
all_soul_frames = []
for row in range(4):
    row_frames = []
    for i in range(4):
        frame = get_player_sprite(Soul_Sprite, i, row, 64, 64, 1, BLK)
        row_frames.append(frame)
    all_soul_frames.append(row_frames)


#coin sprite loading
Coin_Sprite = pygame.image.load('coin.png').convert_alpha()
coin_frames = []
for i in range(5):
    coin_frames.append(get_sprite(Coin_Sprite, i, 64, 64, .85, BLK))
coin_frame = 0
coin_timer = 0

#flags sprite
flag_frames = []
for i in range(5):
    flag_frames.append(get_sprite(flag_sprite,i,60,60,.7,BLK))



# create objects
walls = [
    Wall(175, 540, 155, 5), Wall(445, 450, 5, 265), Wall(265, 450, 180, 5),
    Wall(175, 330, 670, 5), Wall(595, 330, 5, 290), Wall(845, 285, 5, 215),
    Wall(715, 465, 5, 260), Wall(845, 590, 5, 135), Wall(1025, 550, 250, 5),
    Wall(1025, 390, 5, 235), Wall(1025, 390, 80, 5), Wall(1105, 390, 5, 85),
    Wall(935, 290, 5, 190), Wall(935, 290, 255, 5), Wall(1190, 290, 5, 205),
    Wall(805, 200, 470, 5), Wall(805, 70, 5, 130), Wall(625, 70, 180, 5),
    Wall(710, 175, 5, 155), Wall(625, 70, 5, 115), Wall(445, 180, 180, 5),
    Wall(500, 75, 5, 105), Wall(445, 120, 5, 60), Wall(332, 5, 5, 250),
    Wall(175, 120, 85, 5), Wall(255, 70, 5, 50), Wall(255, 250, 270, 5),
    Wall(335, 57, 70, 5), Wall(570, 100, 55, 5), Wall(895, 5, 5, 130),
    Wall(895, 130, 290, 5), Wall(1180, 80, 5, 50), Wall(1080, 5, 5, 65),
    Wall(995, 75, 5, 55),
]

outer_walls = [
    Wall(175, 0, 1100, 5), Wall(175, 0, 5, 400), Wall(175, 645, 5, 70),
    Wall(1275, 0, 5, 720), Wall(175, 715, 1100, 5), Wall(175, 500, 5, 220),
]

exit_wall = Wall(175, 400, 5, 100)

out_rect = Wall(75, 400, 25, 100)

coins = [
    Coin(210, 80), Coin(1055, 450), Coin(930, 80),
    Coin(585, 145), Coin(1050, 580),
]

checkpoints = [
    Checkpoint(858, 518, 5, 100), Checkpoint(858, 216, 5, 95),
    Checkpoint(605, 640, 5, 105), Checkpoint(535, 263, 5, 90),
    Checkpoint(815, 12, 5, 75),
]

player = Player(250, 625, all_player_frames)
soul = soul(500, 625, all_soul_frames)


# ui
label_font = pygame.font.SysFont("comicsansms", 30)
label_surface = label_font.render("Time", True, WHT)
timer_font = pygame.font.SysFont("comicsansms", 30)
be_ready_lable = label_font.render("Please go to the start point", True, WHT)

win_font = pygame.font.SysFont("impact", 80)
win_surface = win_font.render("YOU WIN!", True, GOLD)

clock = pygame.time.Clock()
prev_mouse_x, prev_mouse_y = 0, 0
init_blade(W // 2, H // 2)
cal_min_x, cal_max_x = float(W) * 0.35, float(W) * 0.65
cal_min_y, cal_max_y = float(H) * 0.25, float(H) * 0.75
smooth_x, smooth_y = float(W) / 2.0, float(H) / 2.0

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class OneEuroFilter2D:
    # Smooths jitter when slow, stays responsive when fast.
    def __init__(self, x0, y0, min_cutoff=1.2, beta=0.015, d_cutoff=1.0):
        self.x = float(x0)
        self.y = float(y0)
        self.dx = 0.0
        self.dy = 0.0
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)

    def _alpha(self, cutoff, dt_s):
        cutoff = max(1e-6, float(cutoff))
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / max(1e-6, dt_s))

    def step(self, x, y, dt_s):
        x = float(x)
        y = float(y)

        ad = self._alpha(self.d_cutoff, dt_s)
        dx = (x - self.x) / max(1e-6, dt_s)
        dy = (y - self.y) / max(1e-6, dt_s)
        self.dx = (1.0 - ad) * self.dx + ad * dx
        self.dy = (1.0 - ad) * self.dy + ad * dy

        speed = math.hypot(self.dx, self.dy)
        cutoff = self.min_cutoff + self.beta * speed
        a = self._alpha(cutoff, dt_s)
        self.x = (1.0 - a) * self.x + a * x
        self.y = (1.0 - a) * self.y + a * y
        return self.x, self.y

pointer_filter = OneEuroFilter2D(W / 2, H / 2)
start_time = None  # start when the first frame is displayed
timer_started = False
elapsed = 0

running = True
while running:
    screen.fill(BLK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if level_over:
                level_over = False
            print(f"Mouse clicked at: x={x}, y={y}")

    dt = clock.tick(60)
    dt_s = dt / 1000.0
    tick_blade(W, H)
    raw_x, raw_y = blade_current_pos()

    # Auto-calibration (slowly adapts to user's reachable range)
    cal_min_x = min(cal_min_x, float(raw_x))
    cal_max_x = max(cal_max_x, float(raw_x))
    cal_min_y = min(cal_min_y, float(raw_y))
    cal_max_y = max(cal_max_y, float(raw_y))

    span_x = max(50.0, cal_max_x - cal_min_x)
    span_y = max(50.0, cal_max_y - cal_min_y)
    nx = (float(raw_x) - cal_min_x) / span_x
    ny = (float(raw_y) - cal_min_y) / span_y
    nx = _clamp(nx, 0.0, 1.0)
    ny = _clamp(ny, 0.0, 1.0)

    mapped_x = nx * float(W)
    y_gain = 1.15
    mapped_y = (ny * float(H) - float(H) / 2.0) * y_gain + float(H) / 2.0
    mapped_y = _clamp(mapped_y, 0.0, float(H))

    # Smooth pointer without making it feel heavy
    smooth_x, smooth_y = pointer_filter.step(mapped_x, mapped_y, dt_s)

    # Small deadzone to kill pixel jitter (in screen pixels)
    dx = smooth_x - float(prev_mouse_x)
    dy = smooth_y - float(prev_mouse_y)
    deadzone_px = 4.0
    if (dx * dx + dy * dy) < (deadzone_px * deadzone_px):
        mouse_x, mouse_y = prev_mouse_x, prev_mouse_y
    else:
        mouse_x, mouse_y = int(smooth_x), int(smooth_y)
    soul_rec = pygame.Rect(mouse_x - 12, mouse_y - 12, 25, 25)

    # coin animation
    coin_timer += dt
    if coin_timer > 100:
        coin_frame = (coin_frame + 1) % 5
        coin_timer = 0

    #flag animation
    for cp in checkpoints:
        cp.update(dt)

    # update
    soul.update(mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt)

    if soul.rect.colliderect(player.rect):
        player.is_dead = False
        is_ready = True




    if not player.is_dead and is_ready:
        traps = []
        player.update(soul.rect, walls, outer_walls, coins, checkpoints, exit_wall, traps, dt)        player.update_direction(mouse_x, mouse_y, prev_mouse_x, prev_mouse_y)

    # clock
    if not level_over:
        if start_time is not None:
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
    time_text = f"{elapsed // 60:02}:{elapsed % 60:02}"
    score_label = label_font.render("Score: " + str(player.score), True, WHT)
    time_surface = timer_font.render(time_text, True, WHT)

    

    # if soul.rect.colliderect(player.rect) and not(is_ready):
    #     is_ready = True






    



    # drawing
    if not level_over:
        for coin in coins:
            coin.draw(screen, coin_frames, coin_frame)

        for wall in walls:
            wall.draw(screen)

        for wall in outer_walls:
            wall.draw(screen)

        for cp in checkpoints:
            cp.draw(screen, flag_frames)
        
        player.draw(screen)

        if player.is_dead:
            soul.draw(screen)

        screen.blit(label_surface, (10, 3))
        screen.blit(time_surface, (15, 50))
        screen.blit(score_label, (5, 120))


    if level_over:
        screen.blit(win_surface, (W // 2 - win_surface.get_width() // 2, H // 2 - win_surface.get_height() // 2))


    if player.rect.colliderect(out_rect):
        level_over=True
        print("GG")
        


    if not is_ready:
        screen.blit(be_ready_lable, (500,200))
        pygame.draw.circle(screen, (0, 200, 255), (int(mouse_x), int(mouse_y)), 14, 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(mouse_x), int(mouse_y)), 4, 0)


    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y
    if not exit_open:
        exit_wall.draw(screen)

    if player.score == 100:
        exit_open = True
    else:
        exit_wall.draw(screen)
    
    pygame.display.update()
    if not timer_started:
        start_time = pygame.time.get_ticks()
        timer_started = True

pygame.quit()
shutdown_hand_tracker() 

