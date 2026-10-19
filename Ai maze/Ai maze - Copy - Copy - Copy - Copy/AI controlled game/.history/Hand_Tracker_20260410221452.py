from __future__ import annotations
import threading
import time
from dataclasses import dataclass
from typing import Optional, Tuple
import cv2
import mediapipe as mp


@dataclass
class _FingerState:
    nx: float
    ny: float
    ts: float


class HandTracker:
    """
    Camera + MediaPipe run on a background thread so the pygame loop stays responsive.
    """

    def __init__(
        self,
        camera_index: int = 0,
        camera_width: int = 640,
        camera_height: int = 480,
        mirror: bool = True,
        lost_timeout_s: float = 0.25,
        a_slow: float = 0.25,
        a_fast: float = 0.75,
        speed_ref: float = 45.0,
    ) -> None:
        self.camera_width = int(camera_width)
        self.camera_height = int(camera_height)
        self.mirror = bool(mirror)
        self.lost_timeout_s = float(lost_timeout_s)
        self.a_slow = float(a_slow)
        self.a_fast = float(a_fast)
        self.speed_ref = float(speed_ref)

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            raise RuntimeError("Could not open camera (index %s)" % camera_index)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.45,
        )

        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._last: Optional[_FingerState] = None
        self._last_detected_ts: Optional[float] = None

        self._thread = threading.Thread(target=self._worker, name="HandTracker", daemon=True)
        self._thread.start()

    def close(self) -> None:
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)
        try:
            if self.cap is not None:
                self.cap.release()
        finally:
            if self.hands is not None:
                self.hands.close()

    def _map_norm_to_screen(
        self, nx: float, ny: float, screen_w: int, screen_h: int
    ) -> Tuple[float, float]:
        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))
        if self.mirror:
            nx = 1.0 - nx
        return nx * float(screen_w), ny * float(screen_h)

    def _worker(self) -> None:
        assert self.cap is not None
        while not self._stop.is_set():
            ret, frame = self.cap.read()
            if not ret or frame is None:
                time.sleep(0.02)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if not results.multi_hand_landmarks:
                continue

            hand_landmarks = results.multi_hand_landmarks[0]
            lm = hand_landmarks.landmark[8]
            cam_w = frame.shape[1]
            cam_h = frame.shape[0]
            cam_x_px = float(lm.x) * float(cam_w)
            cam_y_px = float(lm.y) * float(cam_h)

            nx = cam_x_px / max(1.0, float(self.camera_width))
            ny = cam_y_px / max(1.0, float(self.camera_height))
            nx = max(0.0, min(1.0, nx))
            ny = max(0.0, min(1.0, ny))

            now = time.time()
            new_state = _FingerState(nx=nx, ny=ny, ts=now)

            with self._lock:
                self._last_detected_ts = now
                if self._last is None:
                    self._last = new_state
                else:
                    dx = (new_state.nx - self._last.nx) * float(self.camera_width)
                    dy = (new_state.ny - self._last.ny) * float(self.camera_height)
                    speed = (dx * dx + dy * dy) ** 0.5
                    t = max(0.0, min(1.0, speed / max(1e-6, self.speed_ref)))
                    a = self.a_slow + (self.a_fast - self.a_slow) * t
                    snx = (1.0 - a) * self._last.nx + a * new_state.nx
                    sny = (1.0 - a) * self._last.ny + a * new_state.ny
                    self._last = _FingerState(nx=snx, ny=sny, ts=now)

    def get_finger_position(self, screen_w: int, screen_h: int) -> Tuple[float, float]:
        with self._lock:
            if self._last is None or self._last_detected_ts is None:
                return -1.0, -1.0
            if (time.time() - self._last_detected_ts) > self.lost_timeout_s:
                return -1.0, -1.0
            return self._map_norm_to_screen(self._last.nx, self._last.ny, screen_w, screen_h)


_TRACKER: Optional[HandTracker] = None
_IMPORT_ERROR_PRINTED = False


def get_finger_position(screen_w: int, screen_h: int) -> Tuple[float, float]:
    global _TRACKER, _IMPORT_ERROR_PRINTED
    if _TRACKER is None:
        try:
            _TRACKER = HandTracker()
        except Exception as exc:
            if not _IMPORT_ERROR_PRINTED:
                print(f"[hand_tracker] {exc}")
                _IMPORT_ERROR_PRINTED = True
            return -1.0, -1.0
    return _TRACKER.get_finger_position(screen_w, screen_h)


def shutdown_hand_tracker() -> None:
    global _TRACKER
    if _TRACKER is not None:
        _TRACKER.close()
    _TRACKER = None