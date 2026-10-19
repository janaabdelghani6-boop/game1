from __future__ import annotations

import math
from typing import Any, Tuple

import pygame

from core.scene import Scene
from utils.graphics import asset_root, load_background_cover, load_ui_image
from utils.hand_cursor import HandCursor
from utils.fade import draw_color_overlay


class _WoodChoice:
    def __init__(self, label: str, anchor: Tuple[float, float], color: Tuple[int, int, int]) -> None:
        self.label = label
        self.ax, self.ay = anchor
        self.color = color
        self.font = pygame.font.SysFont("georgia", 30, bold=True)
        self.hover = False
        self.phase = 0.0

    def rect_at(self, w: int, h: int, t: float) -> pygame.Rect:
        bx = int(self.ax * w)
        by = int(self.ay * h) + int(math.sin(t * 2.0 + self.phase) * 5)
        return pygame.Rect(bx - 165, by - 34, 330, 68)

    def draw(self, screen: pygame.Surface, w: int, h: int, t: float) -> None:
        r = self.rect_at(w, h, t)
        glow = pygame.Surface((r.w + 34, r.h + 30), pygame.SRCALPHA)
        a = 30 + int(45 * (0.5 + 0.5 * math.sin(t * 2.4 + self.phase))) + (60 if self.hover else 0)
        pygame.draw.rect(
            glow,
            (*self.color, min(a, 220)),
            glow.get_rect(),
            border_radius=16,
        )
        screen.blit(glow, (r.x - 17, r.y - 15), special_flags=pygame.BLEND_ALPHA_SDL2)
        top = (130, 87, 52)
        bottom = (82, 52, 30)
        for i in range(r.height):
            c = (
                top[0] + (bottom[0] - top[0]) * i // max(1, r.height),
                top[1] + (bottom[1] - top[1]) * i // max(1, r.height),
                top[2] + (bottom[2] - top[2]) * i // max(1, r.height),
            )
            pygame.draw.line(screen, c, (r.x + 4, r.y + i), (r.right - 4, r.y + i))
        pygame.draw.rect(screen, (220, 188, 126), r, 3, border_radius=16)
        for xoff in (24, r.width - 25):
            pygame.draw.circle(screen, (74, 50, 30), (r.x + xoff, r.centery), 6)
        surf = self.font.render(self.label, True, (255, 252, 248))
        if self.hover:
            surf = pygame.transform.smoothscale(surf, (int(surf.get_width() * 1.05), int(surf.get_height() * 1.05)))
        screen.blit(surf, (r.centerx - surf.get_width() // 2, r.centery - surf.get_height() // 2))


class ForestHubScene(Scene):
    """Forest background, flying letter event, then stacked wooden choices."""

    T_FOREST = 2.0
    T_LETTER_MOVE = 1.25
    T_LETTER_HOLD = 3.0
    T_LETTER_FADE = 1.05

    def __init__(self, size: Tuple[int, int], start_in_select: bool = False) -> None:
        self.w, self.h = size
        root = asset_root()
        self._bg = load_background_cover(root / "assets" / "backgrounds" / "forest.png", self.w, self.h)
        self._bg_blur = pygame.transform.smoothscale(
            pygame.transform.smoothscale(self._bg, (max(1, self.w // 5), max(1, self.h // 5))),
            (self.w, self.h),
        )
        self._parchment = load_ui_image(root / "assets" / "ui" / "parchment.png", 3000, 3000)
        self._letter_pos = pygame.Vector2(self.w * 0.5, -220)
        self._anim_t = 0.0
        if start_in_select:
            self._elapsed = self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD + self.T_LETTER_FADE + 0.01
        else:
            self._elapsed = 0.0
        self._want_quit = False
        self._choices = [
            _WoodChoice("Maze", (0.5, 0.54), (150, 230, 195)),
            _WoodChoice("Fruit Ninja", (0.5, 0.66), (192, 211, 255)),
            _WoodChoice("Quit", (0.5, 0.78), (255, 194, 186)),
        ]
        for i, c in enumerate(self._choices):
            c.phase = i * 1.7
        self._hand = HandCursor(hold_seconds=2.0)

    def _phase(self) -> str:
        e = self._elapsed
        if e < self.T_FOREST:
            return "forest"
        if e < self.T_FOREST + self.T_LETTER_MOVE:
            return "letter_move"
        if e < self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD:
            return "letter_hold"
        if e < self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD + self.T_LETTER_FADE:
            return "letter_fade"
        return "select"

    def handle_event(self, event: pygame.event.Event) -> Any:
        return None

    def update(self, dt: float) -> Any:
        if self._want_quit:
            return True
        self._elapsed += dt
        self._anim_t += dt * 7.0

        ph = self._phase()
        if ph == "letter_move":
            t0 = self.T_FOREST
            u = min(1.0, (self._elapsed - t0) / self.T_LETTER_MOVE)
            u = 1.0 - (1.0 - u) ** 3
            self._letter_pos.x = self.w * 0.5 + math.sin(u * math.pi * 2.2) * 58
            self._letter_pos.y = -220 + u * (self.h * 0.50 + 220)
        elif ph == "letter_hold":
            self._letter_pos.x = self.w * 0.5 + math.sin(self._elapsed * 1.6) * 14
            self._letter_pos.y = self.h * 0.50 + math.sin(self._elapsed * 2.8) * 9
        elif ph == "letter_fade":
            u = (self._elapsed - (self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD)) / self.T_LETTER_FADE
            u = min(1.0, max(0.0, u))
            self._letter_pos.x = self.w * 0.5 + u * 100
            self._letter_pos.y = self.h * 0.50 - u * (self.h * 0.85)
        elif ph == "forest":
            pass

        self._hand.update(dt, self.w, self.h)
        if ph == "select":
            t = pygame.time.get_ticks() / 1000.0
            for c in self._choices:
                hit = c.rect_at(self.w, self.h, t).inflate(20, 12).collidepoint(int(self._hand.x), int(self._hand.y)) if self._hand.visible else False
                c.hover = hit
                if self._hand.holding_target(dt, c.label, hit):
                    if c.label == "Maze":
                        return {"type": "launch_game", "game": "maze"}
                    if c.label == "Fruit Ninja":
                        return {"type": "launch_game", "game": "fruit_ninja"}
                    self._want_quit = True
        return None

    def draw(self, screen: pygame.Surface) -> None:
        ph = self._phase()
        letter_visible = ph in ("letter_move", "letter_hold", "letter_fade")
        if letter_visible:
            screen.blit(self._bg_blur, (0, 0))
        else:
            screen.blit(self._bg, (0, 0))
        t = pygame.time.get_ticks() / 1000.0

        if letter_visible:
            cx = int(self._letter_pos.x)
            cy = int(self._letter_pos.y)
            angle = math.sin(t * 2.6) * 6
            scale = 1.0 + 0.03 * math.sin(t * 3.8)
            fly = pygame.transform.rotozoom(self._parchment, angle, scale)
            rect = fly.get_rect(center=(cx, cy))
            draw_color_overlay(screen, (12, 16, 20), 58)
            screen.blit(fly, rect.topleft)

        if ph == "letter_fade":
            u = (self._elapsed - (self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD)) / self.T_LETTER_FADE
            u = min(1.0, max(0.0, u))
            draw_color_overlay(screen, (255, 255, 255), 255 * (u ** 1.1))

        if ph == "select":
            for c in self._choices:
                c.draw(screen, self.w, self.h, t)
                p = self._hand.hold_progress(c.label)
                if p > 0:
                    r = c.rect_at(self.w, self.h, t)
                    prog = pygame.Rect(r.x + 14, r.bottom - 10, int((r.width - 28) * p), 5)
                    pygame.draw.rect(screen, (165, 255, 220), prog, border_radius=3)

        draw_color_overlay(screen, (5, 12, 18), 35)
        self._hand.draw(screen)
