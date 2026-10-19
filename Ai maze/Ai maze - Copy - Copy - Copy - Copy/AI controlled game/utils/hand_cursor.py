from __future__ import annotations

import math

import pygame

from Hand_Tracker import get_finger_position


class HandCursor:
    """Hand-tracker pointer with hover-to-select progress."""

    def __init__(self, hold_seconds: float = 0.85) -> None:
        self.x = 0.0
        self.y = 0.0
        self.visible = False
        self._hold_seconds = max(0.2, float(hold_seconds))
        self._hover_time = 0.0
        self._target_id = ""

    def update(self, dt: float, screen_w: int, screen_h: int) -> None:
        fx, fy = get_finger_position(screen_w, screen_h)
        if fx < 0.0 or fy < 0.0:
            self.visible = False
            self._hover_time = 0.0
            self._target_id = ""
            return

        self.visible = True
        self.x = float(fx)
        self.y = float(fy)

    def holding_target(self, dt: float, target_id: str, hit: bool) -> bool:
        if not self.visible or not hit:
            if self._target_id == target_id:
                self._hover_time = 0.0
            return False

        if self._target_id != target_id:
            self._target_id = target_id
            self._hover_time = 0.0

        self._hover_time += dt
        return self._hover_time >= self._hold_seconds

    def hold_progress(self, target_id: str) -> float:
        if self._target_id != target_id:
            return 0.0
        return max(0.0, min(1.0, self._hover_time / self._hold_seconds))

    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return
        cx, cy = int(self.x), int(self.y)
        pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 180.0)
        ring_r = 15 + int(3 * pulse)
        pygame.draw.circle(screen, (120, 220, 255), (cx, cy), ring_r, 2)
        pygame.draw.circle(screen, (250, 255, 255), (cx, cy), 4)
