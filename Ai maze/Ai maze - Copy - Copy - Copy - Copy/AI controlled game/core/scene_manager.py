from __future__ import annotations

from typing import Any, Optional

import pygame

from .scene import Scene


class SceneManager:
    def __init__(self, initial: Scene) -> None:
        self.scene: Scene = initial
        self.request_quit: bool = False
        self.pending_action: Optional[dict[str, Any]] = None

    def handle_event(self, event: pygame.event.Event) -> None:
        nxt = self.scene.handle_event(event)
        if nxt is not None:
            self._apply_transition(nxt)

    def update(self, dt: float) -> None:
        nxt = self.scene.update(dt)
        if nxt is not None:
            self._apply_transition(nxt)

    def _apply_transition(self, nxt: Any) -> None:
        if nxt is True:
            self.request_quit = True
            return
        if isinstance(nxt, Scene):
            self.scene = nxt
            return
        if isinstance(nxt, dict):
            self.pending_action = nxt

    def consume_action(self) -> Optional[dict[str, Any]]:
        action = self.pending_action
        self.pending_action = None
        return action

    def set_scene(self, scene: Scene) -> None:
        self.scene = scene

    def draw(self, screen: pygame.Surface) -> None:
        self.scene.draw(screen)
