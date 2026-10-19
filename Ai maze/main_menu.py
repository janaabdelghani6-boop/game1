import pygame

class Menu :
    def __init__(self):
        self.plat_font = pygame.font.Font("fonts/CheekyMouse1980.ttf", 30)
        self.background = pygame.transform.scale(pygame.image.load("images/MainMenuBackground.png").convert(),(1280, 720))
        self.level_background = pygame.transform.scale(pygame.image.load("images/background1.png").convert(),(1280, 720))
        # self.button = pygame.transform.scale(pygame.image.load("MainMenuBackground.png").convert()


        self.play_hold = 0
        self.exit_hold = 0
        self.level1_hold = 0
        self.level2_hold = 0
        self.back_hold = 0
        self.hold_time = 2000  
        self.cooldown = 0
        self.cooldown_time = 5000

        self.play_rect = pygame.Rect(515, 410, 210, 90)
        self.exit_rect = pygame.Rect(515, 550, 210, 80)

        self.level1_rect = pygame.Rect(515, 200, 260, 95)
        self.level2_rect = pygame.Rect(515, 315, 260, 95)
        self.back_rect = pygame.Rect(515, 525, 260, 80)

    def _draw_hold_button(self, screen, rect, label, progress, hold_time, render_font):

        pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)


        fill_w = int((progress / hold_time) * rect.width)
        fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.height)
        color = (0, 200, 100) if progress >= hold_time else (0, 150, 255)
        pygame.draw.rect(screen, color, fill_rect, border_radius=8)


        hovering = progress > 0
        text_color = "white" if hovering else "yellow"
        text = render_font.render(label, True, text_color)
        screen.blit(text, (
            rect.centerx - text.get_width() // 2,
            rect.centery - text.get_height() // 2
        ))

    def update_hold(self, current, rect, pointer, dt):
        """Only update holds if cooldown is done."""
        if self.cooldown > 0:
            self.cooldown -= dt
            return 0  # freeze all progress during cooldown
        if pointer.colliderect(rect):
            return min(current + dt, self.hold_time)
        else:
            return max(0, current - dt)

    def reset_holds(self):
        self.play_hold = 0
        self.exit_hold = 0
        self.level1_hold = 0
        self.level2_hold = 0
        self.back_hold = 0
        self.cooldown = self.cooldown_time

    def main_select(self, screen, mouse_x, mouse_y, dt):
        
        
        screen.blit(self.background, (0, 0))

        pointer = pygame.Rect(mouse_x - 5, mouse_y - 5, 10, 10)

        self.play_hold  = self.update_hold(self.play_hold,  self.play_rect,  pointer, dt)
        self.exit_hold  = self.update_hold(self.exit_hold,  self.exit_rect,  pointer, dt)   




        self._draw_hold_button(screen, self.play_rect, "Play", self.play_hold, self.hold_time, self.plat_font)
        self._draw_hold_button(screen, self.exit_rect, "Exit", self.exit_hold, self.hold_time, self.plat_font)


        pygame.draw.circle(screen, (0, 200, 255), (int(mouse_x), int(mouse_y)), 14, 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(mouse_x), int(mouse_y)), 4, 0)

        # Return state
        if self.play_hold >= self.hold_time:
            self.play_hold = 0

            self.level1_hold = 0
            self.level2_hold = 0
            self.back_hold = 0
            pointer = pygame.Rect(0, 0, 10, 10)
            return "Level_select"
        if self.exit_hold >= self.hold_time:
            pygame.quit()
            exit()

        return "menu"
    

    def Level_select(self,screen, mouse_x, mouse_y, dt, level_intro):
        screen.blit(self.level_background, (0, 0))    
        if not(level_intro):
            pointer = pygame.Rect(mouse_x - 5, mouse_y - 5, 10, 10)


            self.level1_hold = self.update_hold(self.level1_hold, self.level1_rect, pointer, dt)
            self.level2_hold = self.update_hold(self.level2_hold, self.level2_rect, pointer, dt)
            self.back_hold   = self.update_hold(self.back_hold,   self.back_rect,   pointer, dt)

            self._draw_hold_button(screen, self.level1_rect, "Level 1", self.level1_hold, self.hold_time, self.plat_font)
            self._draw_hold_button(screen, self.level2_rect, "Level 2", self.level2_hold, self.hold_time, self.plat_font)
            self._draw_hold_button(screen, self.back_rect, "Back", self.back_hold, self.hold_time, self.plat_font)

            pygame.draw.circle(screen, (0, 200, 255), (int(mouse_x), int(mouse_y)), 14, 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(mouse_x), int(mouse_y)), 4, 0)
            
            if self.level1_hold >= self.hold_time:
                self.level1_hold = 0
                return "Level1_set"
            
            if self.level2_hold >= self.hold_time:
                self.level2_hold = 0
                return "Level2_set"

            if self.back_hold >= self.hold_time:
                self.back_hold = 0
                return "menu"
            
            return "Level_select"