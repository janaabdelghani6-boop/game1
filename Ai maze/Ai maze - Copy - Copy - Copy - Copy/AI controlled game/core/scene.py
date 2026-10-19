from __future__ import annotations

from typing import Any, Optional

import pygame


class Scene:
    """Base class for all scenes. update() may return a replacement scene."""

    def handle_event(self, event: pygame.event.Event) -> Optional[Any]:
        return None

    def update(self, dt: float) -> Optional[Any]:
        return None

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
