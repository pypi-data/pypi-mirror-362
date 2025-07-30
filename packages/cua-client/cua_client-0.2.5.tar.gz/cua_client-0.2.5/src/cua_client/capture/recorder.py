"""Screen recorder with key-logger – Windows only.

This is a refactored, packaging-friendly version of the standalone script
shared by the user.  Key differences:

* No nested function definitions (168x style guideline).
* No Azure upload support – strictly local capture.
* Non-blocking design: the ``ScreenRecorder`` class exposes ``run`` which
  blocks until interrupted, but can also be invoked in a thread or asyncio
  executor if desired.
* All hard-coded constants are configurable through the ``RecorderConfig``
  dataclass or environment variables (prefix ``CUA_RECORDER_``).
"""

from __future__ import annotations

import os
import time
import logging
import ctypes
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Tuple
from collections import deque

import cv2
import mss
import numpy as np
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)


@dataclass
class RecorderConfig:
    """Configuration parameters for the screen-recorder."""

    output_dir: str = r"C:\\stream_buffer"
    fps: int = 5
    segment_seconds: int = 30
    bar_height: int = 40
    green_seconds: int = 1  # key text turns green for this many seconds
    key_lifetime: int = 3   # how long to display a key overlay
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    font_scale: float = 1.0
    font_thickness: int = 2
    left_margin: int = 10

    @staticmethod
    def from_env() -> "RecorderConfig":
        """Build config from environment variables (prefix: ``CUA_RECORDER_``)."""

        def _env(key: str, cast, default):
            raw = os.getenv(f"CUA_RECORDER_{key}")
            return cast(raw) if raw is not None else default

        return RecorderConfig(
            output_dir=_env("OUTPUT_DIR", str, r"C:\\stream_buffer"),
            fps=_env("FPS", int, 5),
            segment_seconds=_env("SEGMENT_SECONDS", int, 30),
            bar_height=_env("BAR_HEIGHT", int, 40),
            green_seconds=_env("GREEN_SECONDS", int, 1),
            key_lifetime=_env("KEY_LIFETIME", int, 3),
            font_scale=_env("FONT_SCALE", float, 1.0),
            font_thickness=_env("FONT_THICKNESS", int, 2),
            left_margin=_env("LEFT_MARGIN", int, 10),
        )


# ---------------------------------------------------------------------------
# Helpers: Cursor position (Win32 API)
# ---------------------------------------------------------------------------

class _POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


_GetCursorPos = ctypes.windll.user32.GetCursorPos  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Key logging (no nested functions)
# ---------------------------------------------------------------------------

class KeyLogger:
    """Collects keyboard events as a ring-buffer and logs them to a file."""

    def __init__(self, *, maxlen: int = 100, debounce_time: float = 0.05) -> None:
        self._buf: Deque[Tuple[str, float]] = deque(maxlen=maxlen)
        self._debounce_time = debounce_time
        self._lock = keyboard.Listener()._lock  # use pynput's internal lock for safety
        self._shift = False
        self._ctrl = False
        self._alt = False
        self._last_key_time: dict[str, float] = {}
        self.log_file = None  # will be set by Recorder

        # Create listeners
        self._kb_listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            daemon=True,
        )

    # -------------- listener handlers --------------

    def _on_press(self, k):  # noqa: D401 – simple method
        with self._lock:
            if k in (Key.shift, Key.shift_l, Key.shift_r):
                self._shift = True
                return
            if k in (Key.ctrl, Key.ctrl_l, Key.ctrl_r):
                self._ctrl = True
                return
            if k in (Key.alt, Key.alt_l, Key.alt_r):
                self._alt = True
                return

            token = self._format_key(k)
            if not token:
                return

            # Add modifiers
            if self._ctrl or self._alt:
                mods = []
                if self._ctrl:
                    mods.append("CTRL")
                if self._alt:
                    mods.append("ALT")
                token = f"<{'+'.join(mods)}+{token.strip('<>').upper()}>"

            ts = time.time()
            if token in self._last_key_time and ts - self._last_key_time[token] < self._debounce_time:
                return  # debounce
            self._last_key_time[token] = ts

            self._buf.append((token, ts))
            if self.log_file:
                self.log_file.write(token + " ")
                self.log_file.flush()

    def _on_release(self, k):  # noqa: D401 – simple method
        with self._lock:
            if k in (Key.shift, Key.shift_l, Key.shift_r):
                self._shift = False
            elif k in (Key.ctrl, Key.ctrl_l, Key.ctrl_r):
                self._ctrl = False
            elif k in (Key.alt, Key.alt_l, Key.alt_r):
                self._alt = False

    # -------------- public API --------------

    def start(self) -> None:
        """Begin capturing key events."""

        if not self._kb_listener.is_alive():
            self._kb_listener.start()
            logger.debug("KeyLogger started")

    @property
    def buffer(self) -> Deque[Tuple[str, float]]:
        return self._buf

    # -------------- helpers --------------

    def _format_key(self, k):
        if isinstance(k, KeyCode):
            c = k.char
            if c is None:
                return None
            if c == " ":
                return "<SPACE>"
            if c == "\t":
                return "<TAB>"
            if c in ("\n", "\r"):
                return "<ENTER>"
            if c.isprintable():
                return c.upper() if self._shift and c.isalpha() else c
            if self._ctrl and ord(c) < 32:
                return chr(ord(c) + 64)
            return f"<{ord(c)}>"
        if isinstance(k, Key):
            name = k.name.upper()
            return name if len(name) == 1 else f"<{name}>"
        return str(k).upper()


# ---------------------------------------------------------------------------
# Click tracking (mouse listener)
# ---------------------------------------------------------------------------

class ClickTracker:
    """Detects mouse clicks to overlay a temporary label."""

    def __init__(self):
        self._last_click_time = 0.0
        self._listener = mouse.Listener(on_click=self._on_click, daemon=True)

    def start(self) -> None:
        if not self._listener.is_alive():
            self._listener.start()
            logger.debug("ClickTracker started")

    def _on_click(self, _x, _y, _button, pressed):
        if pressed:
            self._last_click_time = time.time()

    def recently_clicked(self, *, window: float = 0.5) -> bool:
        return (time.time() - self._last_click_time) < window


# ---------------------------------------------------------------------------
# Recorder main class
# ---------------------------------------------------------------------------

class ScreenRecorder:
    """Capture screen video with cursor & keystroke overlay into segmented files."""

    def __init__(self, config: RecorderConfig | None = None) -> None:
        self.cfg = config or RecorderConfig.from_env()
        os.makedirs(self.cfg.output_dir, exist_ok=True)

        self._sct = mss.mss()
        self._monitor = self._sct.monitors[1]  # primary monitor

        self._key_logger = KeyLogger()
        self._click_tracker = ClickTracker()

        self._video_writer: cv2.VideoWriter | None = None
        self._log_file = None
        self._segment_start = 0.0

        # start listeners
        self._key_logger.start()
        self._click_tracker.start()

        self._start_new_segment()

    # -------------- public --------------

    def run(self) -> None:
        """Blocking loop – call inside a subprocess / service."""

        logger.info("ScreenRecorder started – writing to %s", self.cfg.output_dir)

        try:
            while True:
                self._capture_frame()
                if time.time() - self._segment_start >= self.cfg.segment_seconds:
                    self._start_new_segment()
                time.sleep(1 / self.cfg.fps)
        finally:
            # clean-up
            if self._video_writer is not None:
                self._video_writer.release()
            if self._log_file is not None:
                self._log_file.close()

    # -------------- helpers --------------

    def _capture_frame(self) -> None:
        frame = cv2.cvtColor(np.array(self._sct.grab(self._monitor)), cv2.COLOR_BGRA2BGR)

        # cursor overlay
        pt = _POINT()
        _GetCursorPos(ctypes.byref(pt))
        cx, cy = pt.x - self._monitor["left"], pt.y - self._monitor["top"]
        if 0 <= cx < self._monitor["width"] and 0 <= cy < self._monitor["height"]:
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            if self._click_tracker.recently_clicked():
                cv2.putText(
                    frame,
                    "CLICK",
                    (cx + 12, cy + 5),
                    self.cfg.font,
                    0.8,
                    (0, 255, 0),
                    2,
                )

        # build canvas with bar
        h, w = frame.shape[:2]
        canvas = np.zeros((h + self.cfg.bar_height, w, 3), np.uint8)
        canvas[:h] = frame
        cv2.rectangle(canvas, (0, h), (w, h + self.cfg.bar_height), (0, 0, 0), -1)

        # overlay keystrokes
        with self._key_logger._lock:  # pylint: disable=protected-access
            buf_snapshot = deque(self._key_logger.buffer)  # copy to avoid holding lock
        now = time.time()
        x = self.cfg.left_margin
        for token, ts in buf_snapshot:
            if now - ts > self.cfg.key_lifetime:
                continue
            color = (0, 255, 0) if (now - ts) < self.cfg.green_seconds else (255, 255, 255)
            cv2.putText(
                canvas,
                token,
                (x, h + self.cfg.bar_height - 10),
                self.cfg.font,
                self.cfg.font_scale,
                color,
                self.cfg.font_thickness,
            )
            text_width, _ = cv2.getTextSize(
                token, self.cfg.font, self.cfg.font_scale, self.cfg.font_thickness
            )[0]
            x += text_width + 5

        # write frame
        if self._video_writer is not None:
            self._video_writer.write(canvas)

    def _start_new_segment(self) -> None:
        if self._video_writer is not None:
            self._video_writer.release()
        if self._log_file is not None:
            self._log_file.close()

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.cfg.output_dir, f"test_vm_video_{ts}.avi")
        logname = os.path.join(self.cfg.output_dir, f"test_vm_logs_{ts}.txt")

        # initialise writer
        w, h = self._monitor["width"], self._monitor["height"]
        size = (w, h + self.cfg.bar_height)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self._video_writer = cv2.VideoWriter(filename, fourcc, self.cfg.fps, size)

        # log file for keystrokes
        self._log_file = open(logname, "w", encoding="utf-8")
        self._key_logger.log_file = self._log_file

        self._segment_start = time.time()
        logger.debug("Started new segment – %s", filename)


# ---------------------------------------------------------------------------
# CLI convenience: ``python -m cua_client.capture.recorder``
# ---------------------------------------------------------------------------

def _cli():  # pragma: no cover – manual run helper
    import argparse

    parser = argparse.ArgumentParser(description="Run screen recorder with key overlay.")
    parser.add_argument("--output-dir", dest="output_dir", help="Directory to store segments")
    args = parser.parse_args()

    cfg = RecorderConfig.from_env()
    if args.output_dir:
        cfg.output_dir = args.output_dir

    ScreenRecorder(cfg).run()


if __name__ == "__main__":  # pragma: no cover
    _cli() 