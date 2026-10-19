from __future__ import annotations

import math
from pathlib import Path
from typing import Any, List, Tuple

import pygame

from core.scene import Scene
from utils.graphics import asset_root, load_background_cover, load_ui_image
from utils.fade import draw_color_overlay


def _extract_idle_frames(root: Path, frame_w: int = 137, frame_h: int = 137, row: int = 0, scale: float = 0.46) -> List[pygame.Surface]:
    path = root / "player.png"
    frames: List[pygame.Surface] = []
    if not path.is_file():
        for i in range(6):
            s = pygame.Surface((int(90 * scale / 0.46), int(110 * scale / 0.46)), pygame.SRCALPHA)
            s.fill((0, 0, 0, 0))
            pygame.draw.ellipse(s, (120 + i * 15, 170, 200), s.get_rect().inflate(-6, -6))
            frames.append(s)
        return frames

    sheet = pygame.image.load(str(path)).convert_alpha()
    sheet.set_colorkey((0, 0, 0))
    for i in range(6):
        surf = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (i * frame_w, row * frame_h, frame_w, frame_h))
        nw = max(1, int(frame_w * scale))
        nh = max(1, int(frame_h * scale))
        frames.append(pygame.transform.smoothscale(surf, (nw, nh)).convert_alpha())
    return frames


class _FloatChoice:
    def __init__(self, label: str, anchor: Tuple[float, float], color: Tuple[int, int, int]) -> None:
        self.label = label
        self.ax, self.ay = anchor
        self.color = color
        self.font = pygame.font.SysFont("georgia", 32, bold=True)
        self.hover = False
        self.phase = 0.0

    def rect_at(self, w: int, h: int, t: float) -> pygame.Rect:
        bx = int(self.ax * w)
        by = int(self.ay * h) + int(math.sin(t * 2.2 + self.phase) * 8)
        surf = self.font.render(self.label, True, self.color)
        scale = 1.08 if self.hover else 1.0
        rw = int(surf.get_width() * scale)
        rh = int(surf.get_height() * scale)
        return pygame.Rect(bx - rw // 2, by - rh // 2, rw, rh)

    def draw(self, screen: pygame.Surface, w: int, h: int, t: float) -> None:
        r = self.rect_at(w, h, t)
        glow = pygame.Surface((r.w + 30, r.h + 26), pygame.SRCALPHA)
        a = 35 + int(40 * (0.5 + 0.5 * math.sin(t * 2.6 + self.phase))) + (55 if self.hover else 0)
        pygame.draw.rect(
            glow,
            (*self.color, min(a, 200)),
            glow.get_rect(),
            border_radius=12,
        )
        screen.blit(glow, (r.x - 15, r.y - 13), special_flags=pygame.BLEND_ALPHA_SDL2)
        surf = self.font.render(self.label, True, (255, 252, 248))
        if self.hover:
            surf = pygame.transform.smoothscale(surf, (int(surf.get_width() * 1.08), int(surf.get_height() * 1.08)))
        screen.blit(surf, (r.centerx - surf.get_width() // 2, r.centery - surf.get_height() // 2))


class ForestHubScene(Scene):
    """Forest background, idle player, letter event, then floating game choices."""

    T_FOREST = 2.0
    T_LETTER_MOVE = 1.25
    T_LETTER_HOLD = 3.0
    T_LETTER_FADE = 1.05

    def __init__(self, size: Tuple[int, int], start_in_select: bool = False) -> None:
        self.w, self.h = size
        root = asset_root()
        self._bg = load_background_cover(root / "assets" / "backgrounds" / "forest.png", self.w, self.h)
        self._parchment = load_ui_image(root / "assets" / "ui" / "parchment.png", 520, 420)
        ph = self._parchment.get_height()
        # أعلى الرقعة عندما تستقر أمام الشخصية (وسط–أعلى الشاشة)
        self._letter_target_top = int(self.h * 0.20)
        self._idle_frames = _extract_idle_frames(root)
        self._anim_t = 0.0
        if start_in_select:
            self._elapsed = self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD + self.T_LETTER_FADE + 0.01
        else:
            self._elapsed = 0.0
        self._letter_y = float(-ph - 40)
        self._want_quit = False
        self._body = pygame.font.SysFont("georgia", 20)
        self._letter_lines = [
            "In this world, the only way forward… is to play.",
        ]
        self._choices = [
            _FloatChoice("Maze", (0.22, 0.58), (160, 230, 200)),
            _FloatChoice("Fruit Ninja", (0.78, 0.58), (200, 210, 255)),
            _FloatChoice("Quit", (0.5, 0.14), (255, 200, 200)),
        ]
        for i, c in enumerate(self._choices):
            c.phase = i * 1.7

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
        if self._phase() != "select":
            return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            t = pygame.time.get_ticks() / 1000.0
            pos = event.pos
            for c in self._choices:
                if c.rect_at(self.w, self.h, t).inflate(24, 16).collidepoint(pos):
                    if c.label == "Maze":
                        print("Maze selected")
                        return {"type": "launch_game", "game": "maze"}
                    elif c.label == "Fruit Ninja":
                        print("Fruit Ninja selected")
                        return {"type": "launch_game", "game": "fruit_ninja"}
                    elif c.label == "Quit":
                        self._want_quit = True
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
            start = float(-self._parchment.get_height() - 40)
            end = float(self._letter_target_top)
            self._letter_y = start + u * (end - start)
        elif ph == "letter_hold":
            bob = math.sin(self._elapsed * 2.0) * 6
            self._letter_y = float(self._letter_target_top) + bob
        elif ph == "letter_fade":
            self._letter_y = float(self._letter_target_top)
        elif ph == "forest":
            pass

        mx, my = pygame.mouse.get_pos()
        if ph == "select":
            t = pygame.time.get_ticks() / 1000.0
            for c in self._choices:
                c.hover = c.rect_at(self.w, self.h, t).inflate(20, 12).collidepoint(mx, my)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._bg, (0, 0))
        t = pygame.time.get_ticks() / 1000.0

        frame = self._idle_frames[int(self._anim_t) % len(self._idle_frames)]
        px = self.w // 2 - frame.get_width() // 2
        py = self.h - frame.get_height() - 36
        screen.blit(frame, (px, py))

        ph = self._phase()
        if ph in ("letter_move", "letter_hold", "letter_fade"):
            cx = self.w // 2 - self._parchment.get_width() // 2
            cy = int(self._letter_y)
            glow = pygame.Surface(
                (self._parchment.get_width() + 40, self._parchment.get_height() + 36),
                pygame.SRCALPHA,
            )
            pulse = 0.5 + 0.5 * math.sin(t * 2.8)
            pygame.draw.rect(
                glow,
                (255, 240, 200, int(50 + 60 * pulse)),
                glow.get_rect(),
                border_radius=18,
            )
            screen.blit(glow, (cx - 20, cy - 18), special_flags=pygame.BLEND_ALPHA_SDL2)
            screen.blit(self._parchment, (cx, cy))
            y = cy + 36
            for line in self._letter_lines:
                surf = self._body.render(line, True, (55, 42, 30))
                screen.blit(surf, (self.w // 2 - surf.get_width() // 2, y))
                y += 28

        if ph == "letter_fade":
            u = (self._elapsed - (self.T_FOREST + self.T_LETTER_MOVE + self.T_LETTER_HOLD)) / self.T_LETTER_FADE
            u = min(1.0, max(0.0, u))
            draw_color_overlay(screen, (255, 255, 255), 255 * (u ** 1.1))

        if ph == "select":
            for c in self._choices:
                c.draw(screen, self.w, self.h, t)

        draw_color_overlay(screen, (5, 12, 18), 35)
