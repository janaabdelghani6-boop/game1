from __future__ import annotations

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


def _patch_pygame_display(screen: pygame.Surface) -> dict:
    """
    Temporarily patch pygame.display so that sub-games calling
    pygame.display.set_mode() or pygame.init() get the EXISTING
    window/surface instead of opening a new one.
    Returns a dict of originals so we can restore them after.
    """
    original_set_mode   = pygame.display.set_mode
    original_set_caption = pygame.display.set_caption
    original_init       = pygame.init
    original_display_init = pygame.display.init

    # Return the existing surface no matter what resolution the sub-game asks for
    pygame.display.set_mode    = lambda *a, **kw: screen
    pygame.display.set_caption = lambda *a, **kw: None   # keep our title
    pygame.init                = lambda: (0, 0)           # already initialised
    pygame.display.init        = lambda: None             # already initialised

    return {
        "set_mode":    original_set_mode,
        "set_caption": original_set_caption,
        "init":        original_init,
        "display_init": original_display_init,
    }


def _restore_pygame_display(originals: dict) -> None:
    pygame.display.set_mode    = originals["set_mode"]
    pygame.display.set_caption = originals["set_caption"]
    pygame.init                = originals["init"]
    pygame.display.init        = originals["display_init"]


def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch selected game from the shared intro menu.
    Returns 'menu' or 'quit'.
    """
    project_root = Path(__file__).resolve().parents[3]
    game_script  = None
    purge_list: list[str] = []

    if game_name == "maze":
        game_script = project_root / "maze.py"
        purge_list  = [
            "maze", "Hand_Tracker", "Level_control", "main_menu",
            "player", "Wall", "Soul", "coins", "check_point",
            "Portal", "Flame",
        ]
    elif game_name == "fruit_ninja":
        game_script = project_root.parent / "Main.py"
        purge_list  = [
            "Main", "Blade", "Full_Fruits", "Sliced_Fruits",
            "Timer", "Score", "Hearts", "Game_Over", "Hand_Tracker",
        ]

    if not (game_script and game_script.exists()):
        print(f"[dispatcher] script not found for '{game_name}': {game_script}")
        return "menu"

    prev_cwd      = Path.cwd()
    prev_sys_path = list(sys.path)
    originals     = _patch_pygame_display(screen)

    try:
        _purge_modules(purge_list)
        os.chdir(str(game_script.parent))
        sys.path.insert(0, str(game_script.parent))
        runpy.run_path(str(game_script), run_name="__main__")

    except SystemExit:
        # Some old scripts call sys.exit() — treat as normal return to menu
        pass
    except Exception as exc:
        print(f"[dispatcher] failed to launch '{game_name}': {exc}")
        traceback.print_exc()
        return "menu"
    finally:
        _restore_pygame_display(originals)
        os.chdir(str(prev_cwd))
        sys.path = prev_sys_path

    return "menu"