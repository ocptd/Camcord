from __future__ import annotations

from dataclasses import asdict

import cv2

from app.config import TrackerConfig
from app.ptz import SimulatedPTZController


class TrackingService:
    def __init__(self, config: TrackerConfig, ptz: SimulatedPTZController) -> None:
        self.config = config
        self.ptz = ptz
        self.tracker = None
        self.roi = None
        self.last_box = None

    def init_tracker(self, frame, roi: tuple[int, int, int, int]) -> None:
        self.tracker = self._create_tracker()
        self.tracker.init(frame, roi)
        self.roi = roi

    def reset_tracker(self) -> None:
        self.tracker = None
        self.roi = None
        self.last_box = None

    def set_config(self, patch: dict) -> dict:
        for key, value in patch.items():
            if value is not None and hasattr(self.config, key):
                setattr(self.config, key, value)
        return asdict(self.config)

    def update(self, frame) -> dict:
        frame_h, frame_w = frame.shape[:2]
        info = {
            "tracking": False,
            "bbox": None,
            "control": {"pan_delta": 0.0, "tilt_delta": 0.0, "zoom_delta": 0.0},
        }

        if self.tracker is None:
            return info

        ok, box = self.tracker.update(frame)
        if not ok:
            self.reset_tracker()
            return info

        x, y, w, h = [int(v) for v in box]
        self.last_box = (x, y, w, h)
        info["tracking"] = True
        info["bbox"] = self.last_box

        pan_delta, tilt_delta, zoom_delta = self._compute_control(frame_w, frame_h, self.last_box)
        self.ptz.move_relative(pan_delta, tilt_delta, zoom_delta)
        info["control"] = {
            "pan_delta": pan_delta,
            "tilt_delta": tilt_delta,
            "zoom_delta": zoom_delta,
        }
        return info

    def _compute_control(self, frame_w: int, frame_h: int, bbox: tuple[int, int, int, int]) -> tuple[float, float, float]:
        x, y, w, h = bbox
        cx = x + w / 2
        cy = y + h / 2
        nx = (cx / frame_w) - 0.5
        ny = (cy / frame_h) - 0.5

        pan_error = 0.0 if abs(nx) < self.config.dead_zone_x else nx
        tilt_error = 0.0 if abs(ny) < self.config.dead_zone_y else ny

        box_ratio = (w * h) / float(frame_w * frame_h)
        zoom_error = self.config.target_box_ratio - box_ratio

        pan_delta = self._clamp(self.config.kp_pan * pan_error * 100.0, self.config.max_step_pan)
        tilt_delta = self._clamp(self.config.kp_tilt * -tilt_error * 100.0, self.config.max_step_tilt)
        zoom_delta = self._clamp(self.config.kp_zoom * zoom_error * 10.0, self.config.max_step_zoom)

        return pan_delta, tilt_delta, zoom_delta

    @staticmethod
    def _clamp(value: float, max_abs: float) -> float:
        return max(-max_abs, min(max_abs, value))

    @staticmethod
    def _create_tracker():
        creators = [
            "TrackerCSRT_create",
            "TrackerKCF_create",
            "TrackerMIL_create",
        ]
        for creator_name in creators:
            creator = getattr(cv2, creator_name, None)
            if creator:
                return creator()
        raise RuntimeError("No compatible OpenCV tracker available")
