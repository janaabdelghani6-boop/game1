from __future__ import annotations

import pygame
import runpy
from pathlib import Path
import os


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    project_root = Path(__file__).resolve().parents[3]
    game_script = None

    if game_name == "maze":
        game_script = project_root / "maze.py"
    elif game_name == "fruit_ninja":
        game_script = project_root.parent / "Main.py"

    if game_script and game_script.exists():
        prev_cwd = Path.cwd()
        try:
            # Run in-process so everything stays in one app window/session.
            os.chdir(str(game_script.parent))
            runpy.run_path(str(game_script), run_name="__main__")
        except Exception:
            return "menu"
        finally:
            os.chdir(str(prev_cwd))

    return "menu"