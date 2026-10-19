from __future__ import annotations

import math
from typing import Any, Tuple

import pygame

from core.scene import Scene
from utils.fade import draw_color_overlay


class TransitionScene(Scene):
    """~2.4s: deeper zoom + motion + flash to forest."""

    DURATION = 2.4

    def __init__(self, size: Tuple[int, int], cave_cover: pygame.Surface) -> None:
        self.w, self.h = size
        self._cave = cave_cover.copy()
        self.t = 0.0

    def update(self, dt: float) -> Any:
        self.t += dt
        if self.t >= self.DURATION:
            from scenes.forest_hub import ForestHubScene

            return ForestHubScene((self.w, self.h))
        return None

    def draw(self, screen: pygame.Surface) -> None:
        # Stronger zoom with cinematic drift.
        zoom_t = min(1.0, self.t / 1.15)
        zoom = 1.0 + 0.72 * (zoom_t ** 1.2)
        drift_x = int(42 * (zoom_t ** 1.3))
        drift_y = int(16 * (zoom_t ** 1.5))
        shake = int(3 * math.sin(self.t * 42.0) * max(0.0, 1.0 - zoom_t))

        zw = max(1, int(self.w * zoom))
        zh = max(1, int(self.h * zoom))
        scaled = pygame.transform.smoothscale(self._cave, (zw, zh))
        screen.blit(scaled, ((self.w - zw) // 2 - drift_x + shake, (self.h - zh) // 2 - drift_y - shake))

        # White build-up mid transition.
        if self.t > 0.85:
            w_phase = min(1.0, (self.t - 0.85) / 0.75)
            white_a = 255 * (w_phase ** 1.05)
            draw_color_overlay(screen, (255, 255, 255), white_a)

        # Black takeover end.
        if self.t > 1.55:
            b_phase = min(1.0, (self.t - 1.55) / 0.85)
            draw_color_overlay(screen, (0, 0, 0), 255 * b_phase)
