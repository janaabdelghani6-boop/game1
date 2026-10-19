

import pygame
import runpy
from pathlib import Path
import os
import sys
import traceback


def _purge_modules(module_names: list[str]) -> None:
    for name in module_names:
        if name in sys.modules:
            del sys.modules[name]


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    project_root = Path(__file__).resolve().parents[3]
    game_script = None
    purge_list: list[str] = []

    if game_name == "maze":
        game_script = project_root / "maze.py"
        purge_list = [
            "maze",
            "Hand_Tracker",
            "Level_control",
            "main_menu",
            "player",
            "Wall",
            "Soul",
            "coins",
            "check_point",
            "Portal",
            "Flame",
        ]
    elif game_name == "fruit_ninja":
        game_script = project_root.parent / "Main.py"
        purge_list = [
            "Main",
            "Blade",
            "Full_Fruits",
            "Sliced_Fruits",
            "Timer",
            "Score",
            "Hearts",
            "Game_Over",
            "Hand_Tracker",
        ]

    if game_script and game_script.exists():
        prev_cwd = Path.cwd()
        prev_sys_path = list(sys.path)
        try:
            # Run in-process so everything stays in one app window/session.
            _purge_modules(purge_list)
            os.chdir(str(game_script.parent))
            sys.path.insert(0, str(game_script.parent))
            runpy.run_path(str(game_script), run_name="__main__")
        except Exception as exc:
            print(f"[dispatcher] failed to launch '{game_name}' from '{game_script}': {exc}")
            traceback.print_exc()
            return "menu"
        finally:
            os.chdir(str(prev_cwd))
            sys.path = prev_sys_path

    return "menu"