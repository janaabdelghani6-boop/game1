Try AI directly in your favorite apps … Use Gemini to generate drafts and refine content, plus get Gemini Pro with access to Google's next-gen AI for EGP 699.99 EGP 0 for 1 month
from __future__ import annotations

import math
from typing import Any, Tuple

import pygame

from core.scene import Scene
from utils.hand_cursor import HandCursor
from utils.graphics import asset_root, load_background_cover
from utils.fade import draw_color_overlay


class CaveIntroScene(Scene):
    TEXT_DELAY = 1.5

    def __init__(self, size: Tuple[int, int]) -> None:
        self.w, self.h = size
        root = asset_root()
        self._bg = load_background_cover(root / "assets" / "backgrounds" / "cave.png", self.w, self.h)
        self._elapsed = 0.0
        self._text_alpha = 0.0
        self._body_font = pygame.font.SysFont("georgia", 22)
        self._btn_font = pygame.font.SysFont("georgia", 26, bold=True)
        self._lines = [
            "How long will you stay in the cave?",
            "Isn't it time to see what lies outside?",
        ]
        self._btn_label = "Step Outside"
        self._btn_rect = pygame.Rect(0, 0, 260, 52)
        self._btn_base = pygame.Rect(0, 0, 260, 52)
        self._hover = False
        self._hand = HandCursor(hold_seconds=0.85)
        self._bgm = None
        self._bgm_started = False
        try:
            self._bgm = pygame.mixer.Sound(str(root / "assets" / "audio" / "scary.mp3.mpeg"))
            self._bgm.set_volume(0.45)
        except (pygame.error, FileNotFoundError):
            self._bgm = None

    def _layout(self) -> None:
        block_h = len(self._lines) * 32 + 80
        y0 = self.h // 2 - block_h // 2 + 40
        self._btn_base.width = 280
        self._btn_base.height = 56
        self._btn_base.centerx = self.w // 2
        self._btn_base.y = y0 + len(self._lines) * 34 + 28

    def handle_event(self, event: pygame.event.Event) -> Any:
        return None

    def _scaled_btn_rect(self, scale: float) -> pygame.Rect:
        r = self._btn_base.copy()
        r.inflate_ip(int(r.width * (scale - 1)), int(r.height * (scale - 1)))
        return r

    def update(self, dt: float) -> Any:
        self._layout()
        if self._bgm and not self._bgm_started:
            self._bgm.play(-1)
            self._bgm_started = True

        self._elapsed += dt
        if self._elapsed >= self.TEXT_DELAY:
            self._text_alpha = min(255.0, self._text_alpha + dt * 220.0)
        self._hand.update(dt, self.w, self.h)
        hit = self._btn_base.inflate(28, 20).collidepoint(int(self._hand.x), int(self._hand.y)) if self._hand.visible else False
        self._hover = hit
        if self._elapsed >= self.TEXT_DELAY and self._hand.holding_target(dt, "step_outside", hit):
            if self._bgm:
                self._bgm.stop()
            from scenes.transition_scene import TransitionScene

            return TransitionScene((self.w, self.h), self._bg)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg, (0, 0))
        if self._elapsed >= self.TEXT_DELAY:
            a = int(self._text_alpha)
            y = self.h // 2 - 70
            for line in self._lines:
                surf = self._body_font.render(line, True, (245, 238, 225))
                surf.set_alpha(a)
                screen.blit(surf, (self.w // 2 - surf.get_width() // 2, y))
                y += 34

        if self._elapsed >= self.TEXT_DELAY:
            t = pygame.time.get_ticks() / 1000.0
            pulse = 0.5 + 0.5 * math.sin(t * 3.2)
            scale = 1.04 + 0.04 * pulse + (0.04 if self._hover else 0)
            btn = self._scaled_btn_rect(scale)
            glow = pygame.Surface((btn.w + 24, btn.h + 24), pygame.SRCALPHA)
            ga = 40 + int(50 * pulse) + (40 if self._hover else 0)
            pygame.draw.rect(glow, (200, 180, 255, min(ga, 180)), glow.get_rect(), border_radius=18)
            screen.blit(glow, (btn.x - 12, btn.y - 12), special_flags=pygame.BLEND_ALPHA_SDL2)
            pygame.draw.rect(screen, (48, 38, 62), btn, border_radius=14)
            wood_top = (124, 86, 52)
            wood_bottom = (89, 60, 34)
            for i in range(btn.height):
                c = (
                    wood_top[0] + (wood_bottom[0] - wood_top[0]) * i // max(1, btn.height),
                    wood_top[1] + (wood_bottom[1] - wood_top[1]) * i // max(1, btn.height),
                    wood_top[2] + (wood_bottom[2] - wood_top[2]) * i // max(1, btn.height),
                )
                pygame.draw.line(screen, c, (btn.x + 4, btn.y + i), (btn.right - 4, btn.y + i))
            pygame.draw.rect(screen, (212, 181, 120), btn, 3, border_radius=14)
            lab = self._btn_font.render(self._btn_label, True, (255, 250, 245))
            screen.blit(lab, (btn.centerx - lab.get_width() // 2, btn.centery - lab.get_height() // 2))
            p = self._hand.hold_progress("step_outside")
            if p > 0:
                prog = pygame.Rect(btn.x + 8, btn.bottom - 9, int((btn.width - 16) * p), 4)
                pygame.draw.rect(screen, (160, 255, 220), prog, border_radius=3)

        draw_color_overlay(screen, (0, 0, 0), 40 * max(0.0, 1.0 - min(1.0, self._elapsed / 0.8)))
        self._hand.draw(screen)