from __future__ import annotations

import importlib.util
import os
import sys
import threading
import traceback
from pathlib import Path
from typing import Optional

import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Preload state
# ─────────────────────────────────────────────────────────────────────────────
_lock    = threading.Lock()
_ready:   dict[str, object]           = {}   # game_name → loaded module
_threads: dict[str, threading.Thread] = {}


# ─────────────────────────────────────────────────────────────────────────────
# Game registry
# ─────────────────────────────────────────────────────────────────────────────
def _game_info(name: str) -> tuple[Optional[Path], list[str]]:
    root = Path(__file__).resolve().parents[3]
    if name == "maze":
        return root / "maze.py", [
            "maze", "Hand_Tracker", "Level_control", "main_menu",
            "player", "Wall", "Soul", "coins", "check_point", "Portal", "Flame",
        ]
    if name == "fruit_ninja":
        return root.parent / "Main.py", [
            "Main", "Blade", "Full_Fruits", "Sliced_Fruits",
            "Timer", "Score", "Hearts", "Game_Over", "Hand_Tracker",
        ]
    return None, []


def _purge(names: list[str]) -> None:
    for n in names:
        sys.modules.pop(n, None)


# ─────────────────────────────────────────────────────────────────────────────
# Pygame display patch  (used for both preload AND launch)
# ─────────────────────────────────────────────────────────────────────────────
_DUMMY_SURFACE: Optional[pygame.Surface] = None   # filled once pygame is up


def _get_dummy() -> pygame.Surface:
    global _DUMMY_SURFACE
    if _DUMMY_SURFACE is None:
        # 1×1 surface in case the real screen isn't passed during preload
        _DUMMY_SURFACE = pygame.Surface((1, 1))
    return _DUMMY_SURFACE


def _patch(screen: Optional[pygame.Surface] = None) -> dict:
    surf = screen if screen is not None else _get_dummy()
    orig = {
        "set_mode":     pygame.display.set_mode,
        "set_caption":  pygame.display.set_caption,
        "init":         pygame.init,
        "display_init": pygame.display.init,
        # also block image.load that needs a display to convert
        "img_convert":  None,   # patched below if needed
    }
    pygame.display.set_mode    = lambda *a, **kw: surf
    pygame.display.set_caption = lambda *a, **kw: None
    pygame.init                = lambda: (0, 0)
    pygame.display.init        = lambda: None
    return orig


def _unpatch(orig: dict) -> None:
    pygame.display.set_mode    = orig["set_mode"]
    pygame.display.set_caption = orig["set_caption"]
    pygame.init                = orig["init"]
    pygame.display.init        = orig["display_init"]


# ─────────────────────────────────────────────────────────────────────────────
# Background preload worker
# ─────────────────────────────────────────────────────────────────────────────
def _worker(game_name: str, script: Path, purge_list: list[str]) -> None:
    prev_cwd = Path.cwd()
    prev_path = list(sys.path)
    orig = _patch()          # ← patch pygame BEFORE any import runs
    try:
        _purge(purge_list)
        os.chdir(str(script.parent))
        sys.path.insert(0, str(script.parent))

        spec   = importlib.util.spec_from_file_location("__preload__", str(script))
        module = importlib.util.module_from_spec(spec)          # type: ignore[arg-type]
        # __name__ == "__preload__"  →  `if __name__ == "__main__":` blocks are skipped
        # so game loops never start here, only top-level class/function defs run.
        spec.loader.exec_module(module)                         # type: ignore[union-attr]

        with _lock:
            _ready[game_name] = module
        print(f"[dispatcher] ✓ preloaded: {game_name}")

    except Exception as exc:
        print(f"[dispatcher] ✗ preload failed ({game_name}): {exc}")
        traceback.print_exc()
    finally:
        _unpatch(orig)
        os.chdir(str(prev_cwd))
        sys.path = prev_path


# ─────────────────────────────────────────────────────────────────────────────
# Public API – preload
# ─────────────────────────────────────────────────────────────────────────────
def preload_games(*names: str) -> None:
    """
    Start background import threads for the given games.
    Safe to call multiple times — duplicate calls are ignored.

    Call as early as possible (e.g. inside CaveIntroScene.__init__) so the
    ~30-60 s intro gives the threads plenty of time to finish.
    """
    for name in names:
        if name in _threads:
            continue
        script, purge_list = _game_info(name)
        if not (script and script.exists()):
            print(f"[dispatcher] preload skipped – not found: {name}")
            continue
        t = threading.Thread(
            target=_worker, args=(name, script, purge_list),
            daemon=True, name=f"preload-{name}",
        )
        _threads[name] = t
        t.start()
        print(f"[dispatcher] → preload started: {name}")


def _wait(name: str, timeout: float = 8.0) -> bool:
    """Join the preload thread (if still running). Returns True when ready."""
    t = _threads.get(name)
    if t and t.is_alive():
        print(f"[dispatcher] waiting for preload: {name} …")
        t.join(timeout=timeout)
    with _lock:
        return name in _ready


# ─────────────────────────────────────────────────────────────────────────────
# Public API – launch
# ─────────────────────────────────────────────────────────────────────────────
def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    Launch the selected game using the existing pygame window.
    • Fast path  →  preload done, call the module's entry point directly.
    • Slow path  →  no preload, fall back to runpy (still benefits from any
                    cached sys.modules).
    Returns 'menu' or 'quit'.
    """
    import runpy

    script, purge_list = _game_info(game_name)
    if not (script and script.exists()):
        print(f"[dispatcher] script not found: {game_name} ({script})")
        return "menu"

    ready    = _wait(game_name)
    prev_cwd = Path.cwd()
    prev_path = list(sys.path)
    orig = _patch(screen)       # prevent sub-game from opening a new window

    try:
        os.chdir(str(script.parent))
        sys.path.insert(0, str(script.parent))

        if ready:
            with _lock:
                module = _ready.pop(game_name)   # consume so next play re-imports fresh

            # Try conventional entry-point names
            entry = (
                getattr(module, "main",      None) or
                getattr(module, "run",       None) or
                getattr(module, "game_loop", None) or
                getattr(module, "start",     None)
            )
            if callable(entry):
                entry()
            else:
                # No named entry point — re-run as __main__.
                # All imports are already cached in sys.modules → much faster.
                _purge(purge_list)
                runpy.run_path(str(script), run_name="__main__")
        else:
            # Full cold launch (preload didn't finish in time)
            _purge(purge_list)
            runpy.run_path(str(script), run_name="__main__")

    except SystemExit:
        pass    # old scripts that call sys.exit()
    except Exception as exc:
        print(f"[dispatcher] launch error ({game_name}): {exc}")
        traceback.print_exc()
        return "menu"
    finally:
        _unpatch(orig)
        os.chdir(str(prev_cwd))
        sys.path = prev_path

    return "menu"