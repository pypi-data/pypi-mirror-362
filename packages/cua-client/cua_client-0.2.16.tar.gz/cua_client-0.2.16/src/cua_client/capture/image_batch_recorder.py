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
from typing import Deque, Tuple, List, Callable
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

CACHING_INTERVAL = 0.10  # seconds between cached frames (immutable)

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

    api_base_url: str = os.getenv("BACKEND_API_BASE_URL", "")
    batch_path: str = os.getenv("CUA_RECORDER_BATCH_PATH", "screenshare/image-batch")
    log_path: str = os.getenv("CUA_RECORDER_LOG_PATH", "screenshare/key-logs")

    capture_interval: float = float(os.getenv("CUA_RECORDER_INTERVAL", "1"))  # seconds
    batch_size: int = int(os.getenv("CUA_RECORDER_BATCH_SIZE", "10"))


    secret_key: str = os.getenv("SECRET_KEY", "")

    # Optional – used for local testing: if set, batches are saved here instead of / in addition to uploading
    save_dir: str = os.getenv("CUA_RECORDER_SAVE_DIR", "")

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
    """Collect keyboard tokens into a ring-buffer for on-screen display and notify on ENTER."""

    def __init__(self, *, maxlen: int = 100, debounce: float = 0.05, event_callback: Callable[[float], None] | None = None):
        self._buf: Deque[Tuple[str, float]] = deque(maxlen=maxlen)
        self._debounce = debounce
        self._lock = threading.Lock()  # Use a standard lock instead of stealing from Listener
        self._shift = self._ctrl = self._alt = False
        self._last_time: dict[str, float] = {}
        self._all_tokens: List[str] = []
        self._event_cb = event_callback

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
            # Fire event callback *before* we add the token so the screenshot picked
            # will not yet include this key press ("pre-event" requirement).
            if tok == "<ENTER>" and self._event_cb is not None:
                try:
                    self._event_cb(now)
                except Exception:  # safeguard – callback must never break logging
                    logger.exception("event_callback failed in KeyLogger")

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
    def __init__(self, *, event_callback: Callable[[float], None] | None = None):
        self._last_click = 0.0
        self._listener = mouse.Listener(on_click=self._on_click, daemon=True)
        self._event_cb = event_callback

    def start(self):
        if not self._listener.is_alive():
            self._listener.start()
            logger.debug("ClickTracker started")

    def _on_click(self, *_):
        ts = time.time()
        self._last_click = ts
        # notify recorder so it can grab the pre-click frame
        if self._event_cb is not None:
            try:
                self._event_cb(ts)
            except Exception:
                logger.exception("event_callback failed in ClickTracker")
        # record token *after* event callback (keeps token out of pre-click frame)
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

        if not self.cfg.secret_key:
            raise ValueError("SECRET_KEY not set – authentication is required")

        # Defer creation of the MSS instance to the recording thread 
        self._sct = None  
        self._mon = None  

        self._frame_cache: Deque[Tuple[float, Tuple[str, bytes]]] = deque(maxlen=int(3 / CACHING_INTERVAL))
        self._event_queue: queue.Queue[float] = queue.Queue()

        # Key / click trackers now notify via _register_event
        self._kl = KeyLogger(event_callback=self._register_event); self._kl.start()
        self._ct = ClickTracker(event_callback=self._register_event); self._ct._kl = self._kl
        self._ct.start()

        self._batch: List[Tuple[str, bytes]] = []
        self._last_token_index: int = 0  # index into _kl._all_tokens
        self._running = True
      
        self._last_periodic_ts: float = time.time()
        self._last_event_ts: float = 0.0

    # ---------------------------- public API ----------------------------

    def request_stop(self):
        """Signal the recorder to finish current batch and exit."""
        self._running = False

    # ------------------------------------------------------------------

    def run(self):
        """Main recording loop.

        Runs in the caller's thread and blocks until ``request_stop()`` is
        invoked. Captures a frame every ``CACHING_INTERVAL`` seconds, selects
        frames that need to be sent (periodic or triggered by click/Enter), and
        hands off complete batches to the queue.
        """

        logger.info("ImageBatchRecorder started – endpoint: %s", self.cfg.batch_endpoint)

        # Lazily create MSS objects so that unit tests can patch them before
        # the first call to run().
        if self._sct is None:
            self._sct = mss.mss()
            self._mon = self._sct.monitors[1]

        try:
            while self._running:
                loop_start = time.time()

                # ------------------- capture & cache raw frame -------------------
                fname, data = self._capture_image()
                self._frame_cache.append((loop_start, (fname, data)))

                # ------------------- handle click/ENTER events -------------------
                event_frame_added = False
                while not self._event_queue.empty():
                    evt_ts = self._event_queue.get_nowait()
                    frame_tuple = self._frame_before(evt_ts)
                    if frame_tuple is not None:
                        self._batch.append(frame_tuple)
                        event_frame_added = True

                # ------------------- periodic capture ---------------------------
                now = time.time()
                if event_frame_added:
                    # Restart the periodic timer – we just added a frame due to
                    # an interaction, so wait ``capture_interval`` seconds before
                    # sending the next time-based frame.
                    self._last_periodic_ts = now
                elif (now - self._last_periodic_ts) >= self.cfg.capture_interval:
                    self._batch.append((fname, data))
                    self._last_periodic_ts = now

                # ------------------- batch dispatch -----------------------------
                if len(self._batch) >= self.cfg.batch_size:
                    self._enqueue_batch()
                    self._batch.clear()

                # ------------------- throttle loop ------------------------------
                elapsed = time.time() - loop_start
                time.sleep(max(0.0, CACHING_INTERVAL - elapsed))
        except KeyboardInterrupt:
            logger.info("Recorder interrupted by user")
        finally:
            # Flush any remaining images when stopping
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
        ok, png = cv2.imencode('.png', canvas, [int(cv2.IMWRITE_PNG_COMPRESSION), 1])
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
        # NEW: optionally save locally for testing
        if self.cfg.save_dir:
            self._save_local(buffer.getvalue(), key_log_str, batch_start_ms)

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

    def _register_event(self, ts: float):
        """Receive event timestamp (click or Enter) from listeners."""
        self._last_event_ts = ts
        try:
            self._event_queue.put_nowait(ts)
        except queue.Full:
            logger.warning("Event queue full; dropping event at %s", ts)

    def _save_local(self, zip_bytes: bytes, key_log: str, batch_id: int):
        """Write batch locally for testing if cfg.save_dir is set."""
        try:
            root = Path(self.cfg.save_dir)
            root.mkdir(parents=True, exist_ok=True)
            batch_dir = root / f"session{self.cfg.session_id}_batch{batch_id}"
            batch_dir.mkdir(exist_ok=True)
            # extract images
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                zf.extractall(batch_dir)
            # key logs
            (batch_dir / "keylog.txt").write_text(key_log, encoding="utf-8")
            logger.info("Saved batch locally at %s", batch_dir)
        except Exception:
            logger.exception("Failed to save batch locally")

    def _frame_before(self, ts: float) -> Tuple[str, bytes] | None:
        """Return the most recent frame captured *at or before* ``ts``.

        If no such frame exists (should only happen directly after start-up),
        return the oldest available frame so we at least send *something*.
        """
        # Iterate the cache newest-to-oldest for O(k) where k ≪ len(cache)
        for fts, frame_tuple in reversed(self._frame_cache):
            if fts <= ts:
                return frame_tuple
        return self._frame_cache[0][1] if self._frame_cache else None


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