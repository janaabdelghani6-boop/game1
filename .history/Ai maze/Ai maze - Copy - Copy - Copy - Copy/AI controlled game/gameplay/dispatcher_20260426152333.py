from __future__ import annotations

import pygame

from fruit_ninja import run_fruit
from maze import run_maze


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game in same pygame window.
    Returns 'menu' or 'quit'.
    """
    if game_name == "maze":
        return run_maze(screen)
    if game_name == "fruit_ninja":
        return run_fruit(screen)
    return "menu"
