import pygame
from player import Player
from Wall import Wall
from Soul import soul as SoulClass
from check_point import Checkpoint
from coins import Coin
import main_menu

W = 1280
H = 720
WHT, BLU, RED, BLK, GOLD = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0), (255, 215, 0)

message = ['You Are Trapped into a maze and there is no way out' , ' Collect all the coins and make your own way',
            'There is only one simple rule',' DONT DIE']

skip_message = 'Press enter to continue'




class Levels:
    def __init__(self):
        self.current = 0
        self.intro = True
        self.intro_done = False

        self.playagain_hold = 0
        self.menu_hold = 0
        self.next_level_hold = 0
        self.hold_time = 2000
    
        self.playagain_rect = pygame.Rect(515, 300, 280, 80)
        self.menu_rect1 = pygame.Rect(515, 540, 280, 80)
        self.next_level = pygame.Rect(515, 420, 280, 80)
        
        self.menu_rect2 = pygame.Rect(515, 420, 280, 80)
        self.play_font = pygame.font.Font("fonts/quaver.ttf", 50)
        self.menu = main_menu.Menu()
    
    def level_reset(self,level,all_player_frames,all_soul_frames):
        if level == 1:
            _player = Player(250, 625, all_player_frames)
            _soul = SoulClass(500, 625, all_soul_frames)

            _coins = [
                Coin(210, 80), Coin(1055, 450), Coin(930, 80),
                Coin(585, 145), Coin(1050, 580),
            ]

            _walls = [
                Wall(175, 540, 155, 5), Wall(445, 450, 5, 265), Wall(265, 450, 180, 5),
                Wall(175, 330, 130, 5), Wall(425, 330, 425, 5), Wall(595, 330, 5, 290), Wall(845, 285, 5, 215),
                Wall(845, 590, 5, 135), Wall(1025, 550, 250, 5),
                Wall(1025, 550, 5, 90), Wall(1105, 390, 5, 85),
                Wall(935, 290, 5, 190), Wall(935, 290, 255, 5), Wall(1190, 290, 5, 205),
                Wall(805, 200, 470, 5), Wall(805, 70, 5, 130), Wall(625, 70, 180, 5),
                Wall(625, 70, 5, 115), Wall(445, 180, 180, 5),
                Wall(445, 120, 5, 60), Wall(332, 5, 5, 105), Wall(332, 210, 5, 40),
                Wall(175, 120, 85, 5), Wall(255, 250, 270, 5),
                Wall(335, 57, 70, 5), Wall(570, 100, 55, 5), Wall(895, 5, 5, 130),
                Wall(895, 130, 155, 5), Wall(1180, 80, 5, 50), Wall(1080, 5, 5, 65), Wall(1125, 130, 60, 5),
                Wall(995, 75, 5, 55),
            ]

            _traps = [
                Wall(305, 330, 120, 5, RED), Wall(715, 465, 5, 260, RED), Wall(710, 175, 5, 155, RED),
                Wall(332, 110, 5, 100, RED), Wall(255, 70, 5, 50, RED), Wall(1025, 390, 80, 5, RED),
                Wall(1025, 390, 5, 160, RED), Wall(1050, 130, 75, 5, RED), Wall(500, 75, 5, 105, RED),
            ]

            _checkpoints = [
                Checkpoint(858, 518, 5, 100), Checkpoint(858, 216, 5, 95),
                Checkpoint(605, 640, 5, 105), Checkpoint(535, 263, 5, 90),
                Checkpoint(815, 12, 5, 75),
            ]

            return (
                _player, _soul, _coins, _walls, _traps, _checkpoints,
                False,        # level_over
                False,        # exit_open
                False,        # is_ready
                "closed",     # portal_state
                0             # portal_frame
            )
        elif level== 2 :
                    _player = Player(215, 660, all_player_frames)
                    _soul = SoulClass(500, 625, all_soul_frames)

                    _coins = [
                            Coin(213,41),Coin(658,41),Coin(730,130),Coin(935,32),Coin(290,238),Coin(651,646)

                    ]

                    _walls = [
                        Wall(175, 615, 310, 5),Wall(255, 0, 5, 75),Wall(255, 75, 75, 5),Wall(330, 75, 5, 95),Wall(175, 165, 155, 5),
                        Wall(445, 275, 330, 5),Wall(445, 275, 5, 100), Wall(370, 375, 350, 5), Wall(445, 75, 5, 95),Wall(445, 170, 165, 5),Wall(615, 75, 80, 5),
                        Wall(695, 175, 75, 5),Wall(770, 105, 5, 75),Wall(895, 75, 132, 5),Wall(895, 275, 132, 5),Wall(1160, 5, 5, 275),
                        Wall(925, 510, 350, 5),Wall(825, 360, 5, 270),Wall(825, 630, 350, 5),Wall(825, 360, 350, 5),Wall(600, 495, 225, 5), 
                        Wall(370, 375, 5, 150),Wall(175, 470, 100, 5), Wall(485, 465, 5, 155)
                    ]

                    _traps = [
                        Wall(330, 170, 5, 105,RED),Wall(255, 275, 80, 5,RED),Wall(255, 275, 5, 100,RED),Wall(695, 5, 5, 170,RED),Wall(520, 5, 5, 165,RED),
                        Wall(895, 5, 5, 270,RED),Wall(1028, 175, 132, 5,RED),Wall(600, 500, 5, 215,RED),Wall(700, 630, 5, 95, RED),Wall(1070, 365, 5, 75, RED),
                        Wall(925, 435, 5, 75, RED),Wall(1000, 515, 5, 55, RED),Wall(1170, 575, 5, 55, RED),
                    ]

                    _checkpoints = [
                        Checkpoint(460, 215, 5, 75),Checkpoint(1185, 300, 5, 75)
                    ]

                    return (
                        _player, _soul, _coins, _walls, _traps, _checkpoints,
                        False,        # level_over
                        False,        # exit_open
                        False,        # is_ready
                        "closed",     # portal_state
                        0             # portal_frame
                    )
    
    def level_intro(self,screen):
        font = pygame.font.Font("fonts/FutureThorTrialRegular-V4xLz.ttf",30)
        dfont = pygame.font.Font("fonts/FutureThorTrialRegular-V4xLz.ttf",40)
        sfont = pygame.font.Font("fonts/FutureThorTrialRegular-V4xLz.ttf",25)
        type_sound = pygame.mixer.Sound("typing2.mp3")
        danger_sound = pygame.mixer.Sound("danger.mp3")
        danger_sound.set_volume(3)
 
        # type_sound.set_volume(3)
        sound_on = True
        danger_on = True       
        prev_len = 0
        counter = 0
        speed = 4
        snip1 = font.render('', True, 'white')
        snip2 = font.render('', True, 'white')
        snip3 = font.render('', True, 'white')
        snip4 = dfont.render('', True, 'red')
        skip = sfont.render(skip_message, True, 'white')
        current = 0
        done = False
        timer = pygame.time.Clock()
        
        self.intro = True
        screen.fill(BLK)
        pygame.time.wait(2000)

        run = True
        while run:
            screen.fill(BLK)
            timer.tick(60)

            if counter < speed * len(message[current]):
                counter+=1
                if current == 3 and danger_sound:
                    danger_sound.play()
                    danger_on = False
                elif sound_on:
                    type_sound.play()
                    sound_on = False
            
            elif counter >= speed * len(message[current]):
                type_sound.stop()
                pygame.time.wait(1000)
                if not danger_on:
                    pygame.time.wait(2000)
                    danger_sound.stop()
                sound_on = True
                if not current == 3:
                    counter = 0
                if current < 3:
                    current += 1
                else:
                    done = True
            
                # current_len = counter // speed
                # if current_len > prev_len:
                #     type_sound.play()
                #     prev_len = current_len

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and done:
                        run = False
                        break


            if current == 0:
                snip1 = font.render(message[0][0:counter//speed], True, 'white')
                screen.blit(snip1, (640 - snip1.get_width() // 2, 200))

            elif current == 1:
                snip2 = font.render(message[1][0:counter//speed], True, 'white')
                screen.blit(snip1, (640 - snip1.get_width() // 2, 200))
                screen.blit(snip2, (640 - snip2.get_width() // 2, 260))

            elif current == 2:
                snip3 = font.render(message[2][0:counter//speed], True, 'white')
                screen.blit(snip1, (640 - snip1.get_width() // 2, 200))
                screen.blit(snip2, (640 - snip2.get_width() // 2, 260))
                screen.blit(snip3, (640 - snip3.get_width() // 2, 320))

            elif current == 3:
                snip4 = dfont.render(message[3][0:counter//speed], True, 'red')
                screen.blit(snip1, (640 - snip1.get_width() // 2, 200))
                screen.blit(snip2, (640 - snip2.get_width() // 2, 260))
                screen.blit(snip3, (640 - snip3.get_width() // 2, 320))
                screen.blit(snip4, (640 - snip4.get_width() // 2, 400))

            if done:
                screen.blit(skip, (640 - skip.get_width() // 2, 670))

            pygame.display.update()

    def level_update(self,level_over,is_ready,player,soul,walls, outer_walls, coins,
                      checkpoints, exit_wall, traps,mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt, portals = None):
        soul.update(mouse_x, mouse_y, prev_mouse_x, prev_mouse_y, dt)

        if soul.rect.colliderect(player.rect):
            player.is_dead = False
            is_ready = True

        if not player.is_dead and is_ready:
            player.update(soul.rect, walls, outer_walls, coins, checkpoints, exit_wall, traps, dt, portals)
            player.update_direction(soul.rect)
        
        # ← always check portals even when movement is blocked
        elif player.is_teleporting and is_ready:
            player.update(soul.rect, walls, outer_walls, coins, checkpoints, exit_wall, traps, dt, portals)

        return is_ready, player.is_dead
        # if not level_over and start_time is not None:
        #     elapsed = (pygame.time.get_ticks() - start_time) // 1000
        # time_text = f"{elapsed // 60:02}:{elapsed % 60:02}"
        # score_label = label_font.render("Score: " + str(player.score), True, WHT)
        # time_surface = timer_font.render(time_text, True, WHT)


    def level_draw(self,screen,level_over,coins,coin_frames,coin_frame,walls,
                   outer_walls,traps,checkpoints,player,flag_frames,soul,label_surface,time_surface,score_label,out_rect,portal_frames,
                   PORTAL_FRAMES_PER_ROW,win_surface,is_ready,be_ready_lable,mouse_x,mouse_y,exit_wall,portal_state,portal_frame,
                   exit_open, dt , game_state, portals = None, tp_frames = None , flame = None, flame_frames = None):
        if not level_over:
            for coin in coins:
                coin.draw(screen, coin_frames, coin_frame)
            for wall in walls:
                wall.draw(screen)
            for wall in outer_walls:
                wall.draw(screen)
            for wall in traps:
                wall.draw(screen)
            for cp in checkpoints:
                if cp.rect.collidepoint(player.last_checkpoint.center):
                    cp.draw(screen, flag_frames, is_current=True)
                else:
                    cp.draw(screen, flag_frames, is_current=False)

            if portal_state not in ("absorb", "win"):
                if not player.is_teleporting:
                    player.draw(screen)
                elif flame and flame_frames:
                    flame.update(mouse_x, mouse_y, dt)
                    flame.draw(screen, flame_frames)
                    font = pygame.font.SysFont("comicsansms", 30)
                    msg = font.render("Please go to the other portal!", True, (200, 100, 255))
                    screen.blit(msg, (W // 2 - msg.get_width() // 2, H // 2 - 40))
            
            
            if player.is_dead:
                soul.draw(screen)

            screen.blit(label_surface, (10, 3))
            screen.blit(time_surface, (15, 50))
            screen.blit(score_label, (5, 120))

        if portal_state != "closed":
            row_map = {"intro": 1, "idle": 0, "absorb": 2, "win": 2}
            row = row_map.get(portal_state, 0)
            safe_frame = min(portal_frame, PORTAL_FRAMES_PER_ROW - 1)
            portal_x = out_rect.rect.x + out_rect.rect.width // 2 - portal_frames[row][safe_frame].get_width() // 2
            portal_y = out_rect.rect.y + out_rect.rect.height // 2 - portal_frames[row][safe_frame].get_height() // 2
            screen.blit(portal_frames[row][safe_frame], (portal_x, portal_y))

        if level_over and portal_state == "win":
            screen.blit(win_surface, (W // 2 - win_surface.get_width() // 2,
            70))
    
            pointer = pygame.Rect(mouse_x - 5, mouse_y - 5, 10, 10) 
                    
            self.playagain_hold = self.menu.update_hold(self.playagain_hold, self.playagain_rect, pointer, dt)
            
            
            
            self.menu._draw_hold_button(screen, self.playagain_rect, "Play again", self.playagain_hold, self.hold_time, self.play_font)
            
            
            if game_state == "Level1":
                self.menu_hold = self.menu.update_hold(self.menu_hold, self.menu_rect1, pointer, dt)
                self.next_level_hold = self.menu.update_hold(self.next_level_hold, self.next_level, pointer, dt)
                self.menu._draw_hold_button(screen, self.menu_rect1, "Menu", self.menu_hold, self.hold_time, self.play_font)
                self.menu._draw_hold_button(screen, self.next_level, "Next Level", self.next_level_hold, self.hold_time, self.play_font)

            elif game_state == "Level2":
                self.menu_hold = self.menu.update_hold(self.menu_hold, self.menu_rect2, pointer, dt)
                self.menu._draw_hold_button(screen, self.menu_rect2, "Menu", self.menu_hold, self.hold_time, self.play_font)

            pygame.draw.circle(screen, (0, 200, 255), (int(mouse_x), int(mouse_y)), 14, 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(mouse_x), int(mouse_y)), 4, 0)

            if self.playagain_hold >= self.hold_time:
                self.playagain_hold = 0
                if game_state == "Level1":
                    return exit_open, portal_state, portal_frame,"Level1_set"
                if game_state == "Level2":
                    return exit_open, portal_state, portal_frame,"Level2_set"

            if self.menu_hold >= self.hold_time:
                self.menu_hold = 0
                return exit_open, portal_state, portal_frame,"menu"

            if self.next_level_hold >= self.hold_time:
                self.next_level_hold = 0
                return exit_open, portal_state, portal_frame, "Level2_set"
  
  
  
        if not is_ready:
            screen.blit(be_ready_lable, (500, 200))
            pygame.draw.circle(screen, (0, 200, 255), (int(mouse_x), int(mouse_y)), 14, 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(mouse_x), int(mouse_y)), 4, 0)

        if game_state == "Level1":
                
            if player.score == 100 and portal_state == "closed":
                exit_open = True
                portal_state = "intro"
                portal_frame = 0

        elif game_state == "Level2"  :
            if portal_state != "win":
                portals[0].draw(screen, tp_frames)           
                portals[1].draw(screen, tp_frames, flip=True) 
            if player.score == 120 and portal_state == "closed":
                exit_open = True
                portal_state = "intro"
                portal_frame = 0

        if not exit_open:
            exit_wall.draw(screen)
        
        return exit_open, portal_state, portal_frame,game_state
