from pydantic import BaseModel, Field


class ModePayload(BaseModel):
    mode: str = Field(pattern="^(auto|manual)$")


class PTZMovePayload(BaseModel):
    pan_delta: float = 0.0
    tilt_delta: float = 0.0
    zoom_delta: float = 0.0


class TrackerInitPayload(BaseModel):
    x: int
    y: int
    w: int
    h: int


class TrackerConfigPayload(BaseModel):
    kp_pan: float | None = None
    kp_tilt: float | None = None
    kp_zoom: float | None = None
    dead_zone_x: float | None = None
    dead_zone_y: float | None = None
    target_box_ratio: float | None = None
    max_step_pan: float | None = None
    max_step_tilt: float | None = None
    max_step_zoom: float | None = None
