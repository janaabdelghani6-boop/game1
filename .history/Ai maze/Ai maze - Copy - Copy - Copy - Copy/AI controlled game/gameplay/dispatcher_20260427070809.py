from __future__ import annotations

import os
import sys
import threading
import traceback
from pathlib import Path
from typing import Optional

import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Pygame display patch
# ─────────────────────────────────────────────────────────────────────────────

def _patch(screen: pygame.Surface) -> dict:
    orig = {
        "set_mode":     pygame.display.set_mode,
        "set_caption":  pygame.display.set_caption,
        "init":         pygame.init,
        "display_init": pygame.display.init,
    }
    pygame.display.set_mode    = lambda *a, **kw: screen
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
# Game registry
# ─────────────────────────────────────────────────────────────────────────────

def _game_dir(game_name: str) -> Optional[Path]:
    root = Path(__file__).resolve().parents[3]
    if game_name == "maze":
        p = root / "maze.py"
        return p.parent if p.exists() else None
    if game_name == "fruit_ninja":
        p = root.parent / "fruit_ninja.py"
        return p.parent if p.exists() else None
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Preload state
# ─────────────────────────────────────────────────────────────────────────────

_lock     = threading.Lock()
_ready:   dict[str, bool]             = {}
_threads: dict[str, threading.Thread] = {}


def _preload_worker(game_name: str, game_dir: Path) -> None:
    prev_cwd  = Path.cwd()
    prev_path = list(sys.path)
    try:
        os.chdir(str(game_dir))
        if str(game_dir) not in sys.path:
            sys.path.insert(0, str(game_dir))

        if game_name == "maze":
            import importlib
            for mod in ["player", "Wall", "Soul", "check_point", "coins"]:
                try:
                    importlib.import_module(mod)
                except Exception:
                    pass
            try:
                import pygame as _pg
                _pg.image.load(str(game_dir / "player.png"))
                _pg.image.load(str(game_dir / "Soul.png"))
                _pg.image.load(str(game_dir / "coin.png"))
                _pg.image.load(str(game_dir / "flag animation.png"))
                _pg.image.load(str(game_dir / "Gportal.png"))
            except Exception:
                pass

        elif game_name == "fruit_ninja":
            import importlib
            for mod in ["Full_Fruits", "Sliced_Fruits", "Score", "Timer", "Hearts", "Game_Over"]:
                try:
                    importlib.import_module(mod)
                except Exception:
                    pass
            try:
                from Full_Fruits import _img as fi
                from Sliced_Fruits import _img as si
                for name, w, h in [
                    ('apple',120,120),('coconut',120,120),('pineapple',140,140),
                    ('orange',140,140),('lemon',100,100),('pear',140,140),
                ]:
                    fi(f'Fruits_Photo/{name}.png', w, h)
                for name, w, h in [
                    ('appleLeft',80,90),('coconutLeft',70,100),('pineappleLeft',85,110),
                    ('orangeLeft',80,120),('lemonLeft',60,90),('pearLeft',90,100),
                    ('appleRight',80,90),('coconutRight',70,100),('pineappleRight',85,110),
                    ('orangeRight',80,120),('lemonRight',60,90),('pearRight',90,100),
                ]:
                    si(f'Fruits_Photo/{name}.png', w, h)
            except Exception:
                pass

        with _lock:
            _ready[game_name] = True
        print(f"[dispatcher] ✓ preloaded: {game_name}")

    except Exception as exc:
        print(f"[dispatcher] ✗ preload failed ({game_name}): {exc}")
        traceback.print_exc()
    finally:
        os.chdir(str(prev_cwd))
        sys.path = prev_path


def preload_games(*names: str) -> None:
    """
    شغّل background threads لـ preload الألعاب.
    استدعيها في أول CaveIntroScene.__init__ عشان الـ preload يخلص أثناء الإنترو.
    """
    for name in names:
        if name in _threads:
            continue
        gdir = _game_dir(name)
        if gdir is None:
            print(f"[dispatcher] preload skipped – dir not found: {name}")
            continue
        t = threading.Thread(
            target=_preload_worker, args=(name, gdir),
            daemon=True, name=f"preload-{name}",
        )
        _threads[name] = t
        t.start()
        print(f"[dispatcher] → preload started: {name}")


def _wait_with_screen(screen: pygame.Surface, name: str, timeout: float = 8.0) -> bool:
    """
    بدل ما نعمل t.join() وتفريز الشاشة، بنعمل busy-wait مع رسم loading screen
    عشان الـ event loop ميتعلقش.
    """
    t = _threads.get(name)
    if t is None or not t.is_alive():
        with _lock:
            return _ready.get(name, False)

    print(f"[dispatcher] waiting for preload: {name} …")

    font = None
    try:
        font = pygame.font.SysFont("arial", 36)
    except Exception:
        pass

    clock      = pygame.time.Clock()
    elapsed    = 0.0
    dot_count  = 0
    dot_timer  = 0.0
    sw, sh     = screen.get_size()

    while t.is_alive() and elapsed < timeout:
        dt = clock.tick(30) / 1000.0
        elapsed   += dt
        dot_timer += dt

        # امسح الـ events عشان الويندو ميتعلقش
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if dot_timer >= 0.4:
            dot_timer  = 0.0
            dot_count  = (dot_count + 1) % 4

        # ارسم شاشة تحميل بسيطة
        screen.fill((10, 10, 20))
        if font:
            dots = "." * dot_count
            text = font.render(f"Loading{dots}", True, (200, 200, 255))
            rect = text.get_rect(center=(sw // 2, sh // 2))
            screen.blit(text, rect)

            # شريط تحميل بسيط
            bar_w   = 400
            bar_h   = 12
            bar_x   = (sw - bar_w) // 2
            bar_y   = sh // 2 + 50
            progress = min(elapsed / timeout, 1.0)
            pygame.draw.rect(screen, (50, 50, 80),  (bar_x, bar_y, bar_w, bar_h), border_radius=6)
            pygame.draw.rect(screen, (100, 150, 255), (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=6)

        pygame.display.flip()

    with _lock:
        return _ready.get(name, False)


# ─────────────────────────────────────────────────────────────────────────────
# Launcher
# ─────────────────────────────────────────────────────────────────────────────

def launch_selected_game(screen: pygame.Surface, game_name: str) -> str:
    """
    بيشغّل اللعبة على نفس الويندو بدون تعليق.
    """
    gdir = _game_dir(game_name)
    if gdir is None:
        print(f"[dispatcher] game dir not found: {game_name}")
        return "menu"

    # استنى الـ preload مع شاشة تحميل بدل ما نفريز كل حاجة
    _wait_with_screen(screen, game_name)

    prev_cwd  = Path.cwd()
    prev_path = list(sys.path)
    orig      = _patch(screen)

    try:
        os.chdir(str(gdir))
        if str(gdir) not in sys.path:
            sys.path.insert(0, str(gdir))

        if game_name == "maze":
            import importlib
            # امسح الـ cached modules القديمة قبل الـ reload عشان الـ state يتصفّى
            for k in list(sys.modules.keys()):
                if k in ("maze", "player", "Wall", "Soul", "check_point", "coins"):
                    del sys.modules[k]
            maze_mod = importlib.import_module("maze")
            if hasattr(maze_mod, "run_maze"):
                maze_mod.run_maze(screen)
            else:
                import runpy
                runpy.run_path(str(gdir / "maze.py"), run_name="__main__")

        elif game_name == "fruit_ninja":
            import importlib
            for k in list(sys.modules.keys()):
                if k in ("fruit_ninja", "Full_Fruits", "Sliced_Fruits",
                         "Score", "Timer", "Hearts", "Game_Over"):
                    del sys.modules[k]
            fn_mod = importlib.import_module("fruit_ninja")
            if hasattr(fn_mod, "run_fruit"):
                fn_mod.run_fruit(screen)
            else:
                import runpy
                runpy.run_path(str(gdir / "fruit_ninja.py"), run_name="__main__")

    except SystemExit:
        pass
    except Exception as exc:
        print(f"[dispatcher] launch error ({game_name}): {exc}")
        traceback.print_exc()
        return "menu"
    finally:
        _unpatch(orig)
        os.chdir(str(prev_cwd))
        sys.path = prev_path

    return "menu"