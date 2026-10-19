from __future__ import annotations

import pygame
import sys


def _purge_modules(module_names: list[str]) -> None:
    for name in module_names:
        if name in sys.modules:
            del sys.modules[name]


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    purge_list: list[str] = []

    if game_name == "maze":
        purge_list = [
            "maze",
            "Hand_Tracker",
            "player",
            "Wall",
            "Soul",
            "coins",
            "check_point",
        ]
    elif game_name == "fruit_ninja":
        purge_list = [
            "fruit_ninja",
            "Blade",
            "Full_Fruits",
            "Sliced_Fruits",
            "Timer",
            "Score",
            "Hearts",
            "Game_Over",
            "Hand_Tracker",
        ]

    try:
        # Run in-process so everything stays in one app window/session.
        _purge_modules(purge_list)

        if game_name == "maze":
            from maze import run_maze

            return run_maze(screen)

        if game_name == "fruit_ninja":
            from fruit_ninja import run_fruit

            return run_fruit(screen)
    except Exception as exc:
        print(f"[dispatcher] failed to launch '{game_name}': {exc}")
        return "menu"
    finally:
        # Restore import state after each game to avoid stale modules across runs.
        sys.path = list(dict.fromkeys(sys.path))

    return "menu"