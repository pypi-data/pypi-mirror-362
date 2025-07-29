"""Image-batch screen recorder.

Captures one screenshot per second with cursor & keystroke overlay, batches 10
images, and sends the batch to the backend via HTTP POST ("/post_image_batch")
using ``requests``.

This does *not* write any files locally. Designed for Windows VMs.
"""

from __future__ import annotations

import io
import os
import time
import logging
import ctypes
import signal
import zipfile
from dataclasses import dataclass
from collections import deque
from typing import Deque, Tuple, List
from pathlib import Path
from urllib.parse import urljoin

import cv2
import mss
import numpy as np
import requests
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
import threading
import queue

logger = logging.getLogger(__name__)
# ---------------------------------------------------------------
# File logging to C:\screen-capture\logs\recorder.log
# ---------------------------------------------------------------

_LOG_DIR = Path(r"C:\screen-capture\logs")
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = _LOG_DIR / "recorder.log"

if not any(isinstance(h, logging.FileHandler) and h.baseFilename == str(_LOG_FILE) for h in logger.handlers):
    _fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    _fh.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
    _fh.setLevel(logging.INFO)
    logger.addHandler(_fh)
    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class BatchRecorderConfig:
    """Configurable parameters – values can be overridden via env vars."""

    api_base_url: str = os.getenv("GUAC_API_BASE_URL", "")
    batch_path: str = os.getenv("CUA_RECORDER_BATCH_PATH", "screenshare/image-batch")
    log_path: str = os.getenv("CUA_RECORDER_LOG_PATH", "screenshare/key-logs")

    capture_interval: float = float(os.getenv("CUA_RECORDER_INTERVAL", "1"))  # seconds
    batch_size: int = int(os.getenv("CUA_RECORDER_BATCH_SIZE", "10"))

    # Optional – used to authenticate uploads to the backend
    secret_key: str = os.getenv("SECRET_KEY", "")

    # Recording session (set by controller)
    session_id: int = 0

    @property
    def batch_endpoint(self) -> str:
        return urljoin(self.api_base_url.rstrip('/') + '/', self.batch_path.lstrip('/'))

    @property
    def log_endpoint(self) -> str:
        return urljoin(self.api_base_url.rstrip('/') + '/', self.log_path.lstrip('/'))

    bar_height: int = 40
    green_seconds: int = 1
    key_lifetime: int = 3
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    font_scale: float = 1.0
    font_thickness: int = 2
    left_margin: int = 10


# ---------------------------------------------------------------
# Work item for producer/consumer
# ---------------------------------------------------------------


@dataclass
class WorkItem:
    session_id: int
    batch_id: int
    images_zip: bytes
    key_logs: str
    attempt: int = 0


# ---------------------------------------------------------------------------
# Helpers: Win32 cursor position
# ---------------------------------------------------------------------------

class _POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


_GetCursorPos = ctypes.windll.user32.GetCursorPos  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Key logging / click tracking (re-usable from previous implementation)
# ---------------------------------------------------------------------------

class KeyLogger:
    """Collect keyboard tokens into a ring-buffer for on-screen display."""

    def __init__(self, *, maxlen: int = 100, debounce: float = 0.05):
        self._buf: Deque[Tuple[str, float]] = deque(maxlen=maxlen)
        self._debounce = debounce
        self._lock = threading.Lock()  # Use a standard lock instead of stealing from Listener
        self._shift = self._ctrl = self._alt = False
        self._last_time: dict[str, float] = {}
        self._all_tokens: List[str] = []

        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            daemon=True,
        )

    # --- keyboard handlers -------------------------------------------------

    def _on_press(self, k):
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

            tok = self._fmt(k)
            if not tok:
                return

            if self._ctrl or self._alt:
                mods: List[str] = []
                if self._ctrl:
                    mods.append("CTRL")
                if self._alt:
                    mods.append("ALT")
                tok = f"<{'+'.join(mods)}+{tok.strip('<>').upper()}>"

            now = time.time()
            if tok in self._last_time and now - self._last_time[tok] < self._debounce:
                return
            self._last_time[tok] = now
            self._buf.append((tok, now))
            self._all_tokens.append(tok)

    def _on_release(self, k):
        with self._lock:
            if k in (Key.shift, Key.shift_l, Key.shift_r):
                self._shift = False
            elif k in (Key.ctrl, Key.ctrl_l, Key.ctrl_r):
                self._ctrl = False
            elif k in (Key.alt, Key.alt_l, Key.alt_r):
                self._alt = False

    # ---------------------------------------------------------------------

    def start(self):
        if not self._listener.is_alive():
            self._listener.start()
            logger.debug("KeyLogger started")

    @property
    def buffer(self) -> Deque[Tuple[str, float]]:
        return self._buf

    def full_log_string(self) -> str:
        """Return space-separated string of all tokens captured so far."""
        return " ".join(self._all_tokens)

    # helper for click tracker
    def add_token(self, token: str):
        now = time.time()
        with self._lock:
            self._buf.append((token, now))
            self._all_tokens.append(token)

    def _fmt(self, k):  # noqa: C901 – complex but clear mapping
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


class ClickTracker:
    def __init__(self):
        self._last_click = 0.0
        self._listener = mouse.Listener(on_click=self._on_click, daemon=True)

    def start(self):
        if not self._listener.is_alive():
            self._listener.start()
            logger.debug("ClickTracker started")

    def _on_click(self, *_):
        self._last_click = time.time()
        # record token
        self._kl.add_token("<CLICK>")

    def recently_clicked(self, window: float = 1.0) -> bool:
        return (time.time() - self._last_click) < window


# ---------------------------------------------------------------------------
# Main batch recorder
# ---------------------------------------------------------------------------

class ImageBatchRecorder:
    """Capture screen, overlay cursor & keys, send 10-image batches to backend."""

    def __init__(self, cfg: BatchRecorderConfig | None = None, *, work_queue: queue.Queue | None = None):
        self.cfg = cfg or BatchRecorderConfig()
        self._queue = work_queue  # may be None for legacy direct-send
        if not self.cfg.batch_endpoint:
            raise ValueError("CUA_RECORDER_BATCH_ENDPOINT not set – cannot send batches")

        # Defer creation of the MSS instance to the recording thread 
        self._sct = None  
        self._mon = None  

        self._kl = KeyLogger(); self._kl.start()
        self._ct = ClickTracker(); self._ct._kl = self._kl  # inject kl reference
        self._ct.start()

        self._batch: List[Tuple[str, bytes]] = []
        self._last_token_index: int = 0  # index into _kl._all_tokens
        self._running = True

    # ---------------------------- public API ----------------------------

    def request_stop(self):
        """Signal the recorder to finish current batch and exit."""
        self._running = False

    # ------------------------------------------------------------------

    def run(self):
        logger.info("ImageBatchRecorder started – endpoint: %s", self.cfg.batch_endpoint)

        # Create MSS instance in the current (recorder) thread if not yet
        # available.  This avoids thread-local Win32 handle issues.
        if self._sct is None:
            self._sct = mss.mss()
            self._mon = self._sct.monitors[1]

        try:
            while self._running:
                fname, data = self._capture_image()
                self._batch.append((fname, data))
                if len(self._batch) >= self.cfg.batch_size:
                    self._enqueue_batch()
                    self._batch.clear()
                time.sleep(self.cfg.capture_interval)
        except KeyboardInterrupt:
            logger.info("Recorder interrupted by user")
        finally:
            if self._batch:
                self._enqueue_batch()

    # ------------------------------------------------------------------

    def _capture_image(self) -> Tuple[str, bytes]:
        frame = cv2.cvtColor(np.array(self._sct.grab(self._mon)), cv2.COLOR_BGRA2BGR)

        # cursor
        pt = _POINT(); _GetCursorPos(ctypes.byref(pt))
        cx, cy = pt.x - self._mon["left"], pt.y - self._mon["top"]
        if 0 <= cx < self._mon["width"] and 0 <= cy < self._mon["height"]:
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            if self._ct.recently_clicked():
                cv2.putText(frame, "CLICK", (cx+12, cy+5), self.cfg.font, 0.8, (0,255,0), 2)

        # canvas w/ bar
        h, w = frame.shape[:2]
        canvas = np.zeros((h + self.cfg.bar_height, w, 3), np.uint8)
        canvas[:h] = frame
        cv2.rectangle(canvas, (0, h), (w, h + self.cfg.bar_height), (0, 0, 0), -1)

        # keys overlay
        now = time.time(); x = self.cfg.left_margin
        with self._kl._lock:  # pylint: disable=protected-access
            buf = list(self._kl.buffer)
        for tok, ts in buf:
            if now - ts > self.cfg.key_lifetime:
                continue
            col = (0,255,0) if now-ts < self.cfg.green_seconds else (255,255,255)
            cv2.putText(canvas, tok, (x, h+self.cfg.bar_height-10), self.cfg.font,
                        self.cfg.font_scale, col, self.cfg.font_thickness)
            tw, _ = cv2.getTextSize(tok, self.cfg.font, self.cfg.font_scale, self.cfg.font_thickness)[0]
            x += tw + 5

        # encode PNG
        ok, png = cv2.imencode('.png', canvas, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
        if not ok:
            raise RuntimeError("Failed to encode image")
        timestamp = int(time.time() * 1000)
        filename = f"frame_{timestamp}.png"
        return filename, png.tobytes()

    # ------------------------------------------------------------------

    def _enqueue_batch(self):
        """Package current batch & key logs slice into WorkItem and put on queue."""
        if not self._queue:
            # Fallback to old direct-send behaviour if queue not configured
            return self._send_direct()

        # Build ZIP
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fname, data in self._batch:
                zf.writestr(fname, data)
        buffer.seek(0)

        # Key log slice from last_token_index onward
        tokens_slice = self._kl._all_tokens[self._last_token_index :]
        self._last_token_index = len(self._kl._all_tokens)
        key_log_str = " ".join(tokens_slice)

        batch_start_ms = int(time.time() * 1000)
        item = WorkItem(
            session_id=self.cfg.session_id,
            batch_id=batch_start_ms,
            images_zip=buffer.getvalue(),
            key_logs=key_log_str,
        )
        try:
            self._queue.put(item, timeout=5)
            logger.info("Enqueued batch s=%s b=%s (imgs=%d, keys=%d)", self.cfg.session_id, batch_start_ms, len(self._batch), len(tokens_slice))
        except queue.Full:
            logger.error("Work queue full – dropping batch")

    # legacy direct send (used when queue is None)
    def _send_direct(self):
        headers = {"Content-Type": "application/zip"}
        if self.cfg.secret_key:
            headers["X-Secret-Key"] = self.cfg.secret_key
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for fname, data in self._batch:
                zf.writestr(fname, data)
        buffer.seek(0)
        try:
            requests.post(self.cfg.batch_endpoint, data=buffer.getvalue(), headers=headers, timeout=30)
        except Exception:
            pass

    # expose key log
    def get_key_log(self) -> str:
        return self._kl.full_log_string()


# ---------------------------------------------------------------------------
# CLI helper
# ---------------------------------------------------------------------------

def _cli():  # pragma: no cover
    import argparse, sys
    parser = argparse.ArgumentParser(description="1-FPS screen recorder that POSTs 10-image batches")
    parser.add_argument("--endpoint", help="Override batch endpoint URL")
    args = parser.parse_args()

    cfg = BatchRecorderConfig()
    if args.endpoint:
        cfg.batch_endpoint = args.endpoint
    try:
        recorder = ImageBatchRecorder(cfg)

        # Register signal handlers (SIGINT = Ctrl+C, SIGTERM = kill)
        def _handle_signal(_sig, _frame):
            recorder.request_stop()

        signal.signal(signal.SIGINT, _handle_signal)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, _handle_signal)
        if hasattr(signal, "SIGBREAK"):
            # Windows Ctrl+Break
            signal.signal(signal.SIGBREAK, _handle_signal)

        recorder.run()
    except ValueError as err:
        print(err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    _cli() 