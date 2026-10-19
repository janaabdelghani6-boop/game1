from __future__ import annotations

import ctypes
import time

from Hand_Tracker import get_finger_position, shutdown_hand_tracker


_user32 = ctypes.windll.user32


def _screen_size() -> tuple[int, int]:
    return int(_user32.GetSystemMetrics(0)), int(_user32.GetSystemMetrics(1))


def _set_cursor_pos(x: int, y: int) -> None:
    _user32.SetCursorPos(int(x), int(y))


def main() -> None:
    screen_w, screen_h = _screen_size()

    try:
        while True:
            x, y = get_finger_position(screen_w, screen_h)
            if x >= 0.0 and y >= 0.0:
                _set_cursor_pos(int(x), int(y))
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_hand_tracker()


if __name__ == "__main__":
    main()
