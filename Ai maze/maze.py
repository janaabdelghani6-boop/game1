import pygame
import numpy as np
from Level_control import Levels
from player import Player
from Wall import Wall
from Soul import soul as SoulClass
from check_point import Checkpoint
from coins import Coin
from Hand_Tracker import init_blade, tick_blade, blade_current_pos, shutdown_hand_tracker, preload_hand_tracker
import math
from main_menu import Menu
from Portal import portal
from Flame import Flame

pygame.init()
pygame.mixer.init()



W = 1280
H = 720
WHT, BLU, RED, BLK, GOLD = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (255, 215, 0)
NAVY = (10, 10, 40)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Maze")

game_state = "menu" 

# region Helper functions
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
# endregion

# region Load sprites
flag_sprite = pygame.image.load('images/flag animation.png').convert_alpha()
Player_Sprite = pygame.image.load('images/player.png').convert_alpha()
all_player_frames = []
for row in range(4):
    row_frames = []
    for i in range(6):
        row_frames.append(get_player_sprite(Player_Sprite, i, row, 137, 137, 0.4, BLK))
    all_player_frames.append(row_frames)

Soul_Sprite = pygame.image.load('images/Soul.png').convert_alpha()
all_soul_frames = []
for row in range(4):
    row_frames = []
    for i in range(4):
        frame = get_player_sprite(Soul_Sprite, i, row, 64, 64, 1, BLK)
        row_frames.append(frame)
    all_soul_frames.append(row_frames)



Coin_Sprite = pygame.image.load('images/coin.png').convert_alpha()
coin_frames = []
for i in range(5):
    coin_frames.append(get_sprite(Coin_Sprite, i, 64, 64, .85, BLK))
coin_frame = 0
coin_timer = 0



flag_frames = []
for i in range(5):
    flag_frames.append(get_sprite(flag_sprite, i, 60, 60, .7, BLK))



portal_sprite = pygame.image.load("images/Gportal.png").convert_alpha()
portal_frames = []
for row in range(3):
    row_frames = []
    for frame in range(8):
        row_frames.append(get_player_sprite(portal_sprite, frame, row, 64, 64, 2, BLK))
    portal_frames.append(row_frames)
portal_timer = 0
portal_frame_delay = 80
PORTAL_FRAMES_PER_ROW = 8




flame_sprite = pygame.image.load("images/flame_image.png").convert_alpha()
pixels = pygame.surfarray.pixels3d(flame_sprite)
alpha = pygame.surfarray.pixels_alpha(flame_sprite)
mask = (pixels[:,:,0] < 30) & (pixels[:,:,1] < 30) & (pixels[:,:,2] < 60)
alpha[mask] = 0

pixels[:,:,2] = np.clip(pixels[:,:,0].astype(int), 0, 255)  
pixels[:,:,1] = pixels[:,:,1] // 3  
del pixels, alpha

flame_w = flame_sprite.get_width() // 8
flame_h = flame_sprite.get_height()

flame_frames = []
for i in range(8):
    flame_frames.append(get_sprite(flame_sprite, i, flame_w, flame_h, .4, BLK))

P_portal = pygame.image.load("images/Purple Portal Sprite Sheet.png")

tp_frames = []

for i in range(8):
    tp_frames.append(get_player_sprite(P_portal, i, 0, 64, 64, 1.5, BLK))
# endregion

# region Static level objects (never reset)
outer_walls1 = [
    Wall(175, 0, 1100, 5), Wall(175, 0, 5, 400 ), Wall(175, 645, 5, 70),
    Wall(1275, 0, 5, 720), Wall(175, 715, 1100, 5), Wall(175, 500, 5, 220),
]

outer_walls2 = [
    Wall(175, 0, 1100, 5),    # top
    Wall(175, 0, 5, 615),     # left top piece
    # Wall(175, 500, 5, 220),   # left bottom piece  
    Wall(1275, 0, 5, 720),    # right
    Wall(175, 715, 1100, 5),  # bottom
]



exit_wall2 = Wall(175, 615, 5, 100)

exit_wall = Wall(175, 400, 5, 100)

out_rect = Wall(75, 400, 25, 100)
out_rect2 = Wall(75, 615, 25, 100)
# endregion

# region Levels

# endregion

# region Init game state
level = Levels()
menu = Menu()
flame = Flame()
player, soul, coins, walls, traps, checkpoints, level_over, exit_open, is_ready, portal_state, portal_frame = level.level_reset(2,all_player_frames,all_soul_frames)
# player, soul, coins, walls, traps, checkpoints, level_over, exit_open, is_ready, portal_state, portal_frame = level.level_reset(1,all_player_frames,all_soul_frames)
# endregion

# Start camera loading in background immediately
preload_hand_tracker()
init_blade(W // 2, H // 2)

portals = [portal(1185, 50, 5, 50),portal(300, 100, 5, 50)]

# Show intro while camera loads in background
# level.level_intro(screen)
# level.intro = False

# region UI
label_font = pygame.font.SysFont("comicsansms", 30)
label_surface = label_font.render("Time", True, WHT)
timer_font = pygame.font.SysFont("comicsansms", 30)
be_ready_lable = label_font.render("Please go to the start point", True, WHT)
win_font = pygame.font.SysFont("impact", 150)
win_surface = win_font.render("YOU WIN!", True, GOLD)
# endregion

# region Hand tracking setup
clock = pygame.time.Clock()
prev_mouse_x, prev_mouse_y = 0, 0
init_blade(W // 2, H // 2)
cal_min_x, cal_max_x = float(W) * 0.35, float(W) * 0.65
cal_min_y, cal_max_y = float(H) * 0.25, float(H) * 0.75
smooth_x, smooth_y = float(W) / 2.0, float(H) / 2.0

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

class OneEuroFilter2D:
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
        x, y = float(x), float(y)
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

pointer_filter = OneEuroFilter2D(W / 2, H / 2, min_cutoff=2.5, beta=0.008)
start_time = None
timer_started = False
elapsed = 0
# endregion

# region Game loop
running = True
while running:
    screen.fill(BLK)
    
    # region Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            print(f"Mouse clicked at: x={x}, y={y}")
            if level_over and portal_state == "win":
                player, soul, coins, walls, traps, checkpoints, level_over, exit_open, is_ready, portal_state, portal_frame = level.level_reset(1,all_player_frames,all_soul_frames)
                start_time = pygame.time.get_ticks()
                elapsed = 0
    # endregion

    # region Hand tracking
    dt = clock.tick(60)
    dt_s = dt / 1000.0
    tick_blade(W, H)
    raw_x, raw_y = blade_current_pos()

    cal_min_x = min(cal_min_x, float(raw_x))
    cal_max_x = max(cal_max_x, float(raw_x))
    cal_min_y = min(cal_min_y, float(raw_y))
    cal_max_y = max(cal_max_y, float(raw_y))

    span_x = max(50.0, cal_max_x - cal_min_x)
    span_y = max(50.0, cal_max_y - cal_min_y)
    nx = _clamp((float(raw_x) - cal_min_x) / span_x, 0.0, 1.0)
    ny = _clamp((float(raw_y) - cal_min_y) / span_y, 0.0, 1.0)

    mapped_x = nx * float(W)
    mapped_y = _clamp((ny * float(H) - float(H) / 2.0) * 1.15 + float(H) / 2.0, 0.0, float(H))

    smooth_x, smooth_y = pointer_filter.step(mapped_x, mapped_y, dt_s)

    ddx = smooth_x - float(prev_mouse_x)
    ddy = smooth_y - float(prev_mouse_y)
    if (ddx * ddx + ddy * ddy) < (12.0 * 12.0):
        mouse_x, mouse_y = prev_mouse_x, prev_mouse_y
    else:
        mouse_x, mouse_y = int(smooth_x), int(smooth_y)
    # endregion
    
    if game_state== "menu":
       game_state = menu.main_select(screen, mouse_x, mouse_y, dt)
       if game_state == "Level_select":
           level.level_intro(screen)
           menu.reset_holds()
           level.intro = False
           

    elif game_state== "Level_select" :
        game_state = menu.Level_select(screen, mouse_x, mouse_y, dt, level.intro)
        if game_state in ("Level1","Level2"):
            menu.reset_holds()  
            start_time = pygame.time.get_ticks()
            timer_started = True
    
    elif game_state == "Level1_set":
        player, soul, coins, walls, traps, checkpoints, level_over, exit_open, is_ready, portal_state, portal_frame = level.level_reset(1,all_player_frames,all_soul_frames)
        game_state = "Level1"
        start_time = pygame.time.get_ticks()
        elapsed = 0

    elif game_state == "Level1":
        
        # region Animations
        coin_timer += dt
        if coin_timer > 100:
            coin_frame = (coin_frame + 1) % 5
            coin_timer = 0

        for cp in checkpoints:
            cp.update(dt)



        portal_timer += dt
        if portal_timer > portal_frame_delay:
            portal_timer = 0
            if portal_state == "intro":
                portal_frame += 1
                if portal_frame >= PORTAL_FRAMES_PER_ROW:
                    portal_frame = 0
                    portal_state = "idle"
            elif portal_state == "idle":
                portal_frame = (portal_frame + 1) % PORTAL_FRAMES_PER_ROW
                if player.rect.colliderect(out_rect.rect):
                    portal_frame = 0
                    portal_state = "absorb"
            elif portal_state == "absorb":
                portal_frame += 1
                if portal_frame >= PORTAL_FRAMES_PER_ROW:
                    portal_frame = PORTAL_FRAMES_PER_ROW - 1
                    portal_state = "win"
                    level_over = True
        # endregion

        # region Update
        is_ready , player.is_dead = level.level_update(level_over,is_ready,player,soul,walls, outer_walls1,
                            coins, checkpoints, exit_wall, traps,mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt)

        if not level_over and start_time is not None :
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
        score_label = label_font.render("Score: " + str(player.score), True, WHT)
        time_text = f"{elapsed // 60:02}:{elapsed % 60:02}"
        time_surface = timer_font.render(time_text, True, WHT)
        # endregion


        exit_open, portal_state, portal_frame, game_state = level.level_draw(
        screen=screen,
        level_over=level_over,
        coins=coins,
        coin_frames=coin_frames,
        coin_frame=coin_frame,
        walls=walls,
        outer_walls=outer_walls1,
        traps=traps,
        checkpoints=checkpoints,
        player=player,
        flag_frames=flag_frames,
        soul=soul,
        label_surface=label_surface,
        time_surface=time_surface,
        score_label=score_label,
        out_rect=out_rect,
        portal_frames=portal_frames,
        PORTAL_FRAMES_PER_ROW=PORTAL_FRAMES_PER_ROW,
        win_surface=win_surface,
        is_ready=is_ready,
        be_ready_lable=be_ready_lable,
        mouse_x=mouse_x,
        mouse_y=mouse_y,
        exit_wall=exit_wall,
        portal_state=portal_state,
        portal_frame=portal_frame,
        exit_open=exit_open,
        dt=dt,
        game_state=game_state
        )


    elif game_state == "Level2_set":
        player, soul, coins, walls, traps, checkpoints, level_over, exit_open, is_ready, portal_state, portal_frame = level.level_reset(2,all_player_frames,all_soul_frames)
        game_state = "Level2"
        start_time = pygame.time.get_ticks()
        elapsed = 0


    elif game_state == "Level2":
         # region Animations
        coin_timer += dt
        if coin_timer > 100:
            coin_frame = (coin_frame + 1) % 5
            coin_timer = 0

        for cp in checkpoints:
            cp.update(dt)


        for tp in portals:
            tp.update(dt)


        portal_timer += dt
        if portal_timer > portal_frame_delay:
            portal_timer = 0
            if portal_state == "intro":
                portal_frame += 1
                if portal_frame >= PORTAL_FRAMES_PER_ROW:
                    portal_frame = 0
                    portal_state = "idle"
            elif portal_state == "idle":
                portal_frame = (portal_frame + 1) % PORTAL_FRAMES_PER_ROW
                if player.rect.colliderect(out_rect2.rect):
                    portal_frame = 0
                    portal_state = "absorb"
            elif portal_state == "absorb":
                portal_frame += 1
                if portal_frame >= PORTAL_FRAMES_PER_ROW:
                    portal_frame = PORTAL_FRAMES_PER_ROW - 1
                    portal_state = "win"
                    level_over = True
        # endregion

        # region Update
        is_ready , player.is_dead = level.level_update(level_over,is_ready,player,soul,walls, outer_walls2,
                            coins, checkpoints, exit_wall2, traps,mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt, portals)

        if not level_over and start_time is not None :
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
        score_label = label_font.render("Score: " + str(player.score), True, WHT)
        time_text = f"{elapsed // 60:02}:{elapsed % 60:02}"
        time_surface = timer_font.render(time_text, True, WHT)
        # endregion


        exit_open, portal_state, portal_frame, game_state = level.level_draw(
        screen=screen,
        level_over=level_over,
        coins=coins,
        coin_frames=coin_frames,
        coin_frame=coin_frame,
        walls=walls,
        outer_walls=outer_walls2,
        traps=traps,
        checkpoints=checkpoints,
        player=player,
        flag_frames=flag_frames,
        soul=soul,
        label_surface=label_surface,
        time_surface=time_surface,
        score_label=score_label,
        out_rect=out_rect2,
        portal_frames=portal_frames,
        PORTAL_FRAMES_PER_ROW=PORTAL_FRAMES_PER_ROW,
        win_surface=win_surface,
        is_ready=is_ready,
        be_ready_lable=be_ready_lable,
        mouse_x=mouse_x,
        mouse_y=mouse_y,
        exit_wall=exit_wall2,
        portal_state=portal_state,
        portal_frame=portal_frame,
        exit_open=exit_open,
        dt=dt,
        game_state=game_state,
        portals = portals,
        tp_frames = tp_frames,
        flame=flame,
        flame_frames=flame_frames
        )




    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y

    pygame.display.update()
    if not timer_started and game_state == "Level" and is_ready:
        start_time = pygame.time.get_ticks()
        timer_started = True
# endregion

pygame.quit()
shutdown_hand_tracker()