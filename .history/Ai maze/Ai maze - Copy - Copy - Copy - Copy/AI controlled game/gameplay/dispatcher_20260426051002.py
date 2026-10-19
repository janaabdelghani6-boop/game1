from __future__ import annotations

import pygame
import subprocess
import sys
from pathlib import Path


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    project_root = Path(__file__).resolve().parents[3]
    game_script = None

    if game_name == "maze":
        # Use the main Maze version with red walls + levels.
        game_script = project_root / "maze.py"
    elif game_name == "fruit_ninja":
        game_script = project_root.parent / "Main.py"

    if game_script and game_script.exists():
        try:
            subprocess.run([sys.executable, str(game_script)], cwd=str(game_script.parent), check=False)
        except Exception:
            return "menu"

    return "menu"
