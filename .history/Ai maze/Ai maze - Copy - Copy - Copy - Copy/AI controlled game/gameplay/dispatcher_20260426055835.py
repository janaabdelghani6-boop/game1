from __future__ import annotations

import os
import pygame
from contextlib import contextmanager
from pathlib import Path

from Hand_Tracker import init_blade


@contextmanager
def _pushd(path: Path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    game_root = Path(__file__).resolve().parents[1]
    init_blade(screen.get_width() // 2, screen.get_height() // 2)

    try:
        # Keep relative asset paths working in each game module.
        with _pushd(game_root):
            if game_name == "maze":
                from maze import run_maze

                return str(run_maze(screen))
            if game_name == "fruit_ninja":
                from fruit_ninja import run_fruit

                return str(run_fruit(screen))
    except Exception as exc:
        print(f"[dispatcher] failed to launch '{game_name}': {exc}")
        return "menu"

    return "menu"