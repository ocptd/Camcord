from dataclasses import dataclass, field


@dataclass
class TrackerConfig:
    kp_pan: float = 0.08
    kp_tilt: float = 0.08
    kp_zoom: float = 0.05
    dead_zone_x: float = 0.08
    dead_zone_y: float = 0.08
    target_box_ratio: float = 0.25
    max_step_pan: float = 3.0
    max_step_tilt: float = 3.0
    max_step_zoom: float = 1.0


@dataclass
class CameraConfig:
    source: int | str = 0
    width: int = 640
    height: int = 480
    fps: int = 30


@dataclass
class AppConfig:
    mode: str = "auto"
    tracker: TrackerConfig = field(default_factory=TrackerConfig)
    camera: CameraConfig = field(default_factory=CameraConfig)


APP_CONFIG = AppConfig()
