from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import cv2
import mediapipe as mp

HAND_TRACKER_KWARGS: Dict[str, Any] = {
    "camera_index": 0,
    "camera_width": 640,
    "camera_height": 480,
    "mirror": True,
    "lost_timeout_s": 0.25,
    "a_slow": 0.35,
    "a_fast": 0.85,
    "speed_ref": 550.0,
}

MEDIAPIPE_HANDS_KWARGS: Dict[str, Any] = {
    "static_image_mode": False,
    "max_num_hands": 1,
    "model_complexity": 0,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.45,
}


@dataclass
class _FingerState:
    x: float
    y: float
    ts: float


class HandTracker:
    def __init__(
        self,
        camera_index: int = 0,
        camera_width: int = 640,
        camera_height: int = 480,
        mirror: bool = True,
        lost_timeout_s: float = 0.25,
        # Adaptive smoothing parameters 
        a_slow: float = 0.25,
        a_fast: float = 0.75,
        speed_ref: float = 550.0,
    ) -> None:
        self.camera_width = int(camera_width)
        self.camera_height = int(camera_height)
        self.mirror = bool(mirror)
        self.lost_timeout_s = float(lost_timeout_s)

        self.a_slow = float(a_slow)
        self.a_fast = float(a_fast)
        self.speed_ref = float(speed_ref)

        # Camera init (no display)
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            raise RuntimeError("Could not open camera (index %s)" % camera_index)

        # MediaPipe Hands (defaults above; override via MEDIAPIPE_HANDS_KWARGS)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(**MEDIAPIPE_HANDS_KWARGS)

        self._last: Optional[_FingerState] = None
        self._last_detected_ts: Optional[float] = None

    def close(self) -> None:
        try:
            if self.cap is not None:
                self.cap.release()
        finally:
            if self.hands is not None:
                self.hands.close()

    def _map_to_screen(
        self, cam_x_px: float, cam_y_px: float, screen_w: int, screen_h: int
    ) -> Tuple[float, float]:
        nx = cam_x_px / max(1.0, float(self.camera_width))
        ny = cam_y_px / max(1.0, float(self.camera_height))

        nx = max(0.0, min(1.0, nx))
        ny = max(0.0, min(1.0, ny))

        if self.mirror:
            nx = 1.0 - nx

        sx = nx * float(screen_w)
        sy = ny * float(screen_h)
        return sx, sy

    def _fallback_or_invalid(self) -> Tuple[float, float]:
        if self._last is None or self._last_detected_ts is None:
            return -1.0, -1.0

        if (time.time() - self._last_detected_ts) > self.lost_timeout_s:
            return -1.0, -1.0

        return float(self._last.x), float(self._last.y)

    def get_finger_position(self, screen_w: int, screen_h: int) -> Tuple[float, float]:
        assert self.cap is not None
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return self._fallback_or_invalid()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if not results.multi_hand_landmarks:
            return self._fallback_or_invalid()

        # First detected hand, index fingertip
        hand_landmarks = results.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark[8]
        cam_w = frame.shape[1]
        cam_h = frame.shape[0]

        cam_x_px = float(lm.x) * float(cam_w)
        cam_y_px = float(lm.y) * float(cam_h)

        new_x, new_y = self._map_to_screen(cam_x_px, cam_y_px, screen_w, screen_h)
        now = time.time()
        self._last_detected_ts = now

        new_state = _FingerState(x=new_x, y=new_y, ts=now)

        # First frame
        if self._last is None:
            self._last = new_state
            return new_state.x, new_state.y

        # Adaptive smoothing 
        dx = new_state.x - self._last.x
        dy = new_state.y - self._last.y
        dist = (dx * dx + dy * dy) ** 0.5
        dt = max(1e-6, now - self._last.ts)
        speed_pps = dist / dt

        t = max(0.0, min(1.0, speed_pps / max(1e-6, self.speed_ref)))
        a = self.a_slow + (self.a_fast - self.a_slow) * t

        smoothed_x = (1.0 - a) * self._last.x + a * new_state.x
        smoothed_y = (1.0 - a) * self._last.y + a * new_state.y

        self._last = _FingerState(x=smoothed_x, y=smoothed_y, ts=now)
        return self._last.x, self._last.y

_TRACKER: Optional[HandTracker] = None
_IMPORT_ERROR_PRINTED = False

def get_finger_position(screen_w: int, screen_h: int) -> Tuple[float, float]:
    global _TRACKER, _IMPORT_ERROR_PRINTED
    if _TRACKER is None:
        try:
            _TRACKER = HandTracker(**HAND_TRACKER_KWARGS)
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

_blade_pos: Tuple[int, int] = (0, 0)

def init_blade(start_x: int, start_y: int) -> None:
    global _blade_pos
    _blade_pos = (int(start_x), int(start_y))

def tick_blade(screen_w: int, screen_h: int) -> None:
    """Each frame: read finger from the tracker and update blade position."""
    global _blade_pos
    fx, fy = get_finger_position(screen_w, screen_h)
    if fx < 0.0 or fy < 0.0:
        return
    _blade_pos = (int(fx), int(fy))

def blade_current_pos() -> Tuple[int, int]:
    return _blade_pos