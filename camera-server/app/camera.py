from __future__ import annotations

from threading import Lock
from time import sleep

import cv2


class CameraStream:
    def __init__(self, source: int | str, width: int = 640, height: int = 480, fps: int = 30):
        self.capture = cv2.VideoCapture(source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)
        self.lock = Lock()
        self.latest_frame = None

    def read(self):
        ok, frame = self.capture.read()
        if ok:
            with self.lock:
                self.latest_frame = frame.copy()
            return frame

        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
        sleep(0.01)
        return None

    def get_latest(self):
        with self.lock:
            if self.latest_frame is None:
                return None
            return self.latest_frame.copy()

    def release(self):
        self.capture.release()
