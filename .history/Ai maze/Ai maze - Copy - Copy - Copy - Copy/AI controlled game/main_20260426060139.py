"""
Cinematic flow: Cave → Transition → Forest → Letter → Game selection.

Run from this folder:
 python main.py

Assets (optional — placeholders are generated if files are missing):
    assets/backgrounds/cave.png
    assets/backgrounds/forest.png
    assets/ui/parchment.png
    player.png  (sprite sheet in this folder)
"""
from __future__ import annotations

import pygame

from Hand_Tracker import shutdown_hand_tracker
from core.scene_manager import SceneManager
from gameplay.dispatcher import launch_selected_game
from scenes.cave_intro import CaveIntroScene
from scenes.forest_hub import ForestHubScene

SCREEN_W = 1280
SCREEN_H = 720
FPS = 60


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("The Path Outside")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    manager = SceneManager(CaveIntroScene((SCREEN_W, SCREEN_H)))
    running = True

    while running:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        if manager.request_quit:
            running = False
            continue

        action = manager.consume_action()
        if action and action.get("type") == "launch_game":
            game_name = str(action.get("game", ""))
            game_result = launch_selected_game(screen, game_name)
            if game_result == "quit":
                running = False
                continue
            pygame.mouse.set_visible(False)
            manager.set_scene(ForestHubScene((SCREEN_W, SCREEN_H), start_in_select=True))

        manager.draw(screen)
        pygame.display.flip()

    shutdown_hand_tracker()
    pygame.quit()


if __name__ == "__main__":
    main()
