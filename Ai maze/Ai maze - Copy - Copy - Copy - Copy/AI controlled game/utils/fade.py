from __future__ import annotations

from typing import Tuple

import pygame


def draw_color_overlay(screen: pygame.Surface, color: Tuple[int, int, int], alpha: float) -> None:
    """alpha in 0..255 (clamped)."""
    a = max(0, min(255, int(alpha)))
    if a <= 0:
        return
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((*color, a))
    screen.blit(overlay, (0, 0))
