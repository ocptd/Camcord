from dataclasses import dataclass


@dataclass
class PTZState:
    pan: float = 0.0
    tilt: float = 0.0
    zoom: float = 1.0


class SimulatedPTZController:
    def __init__(self) -> None:
        self.state = PTZState()
        self.pan_limits = (-90.0, 90.0)
        self.tilt_limits = (-45.0, 45.0)
        self.zoom_limits = (1.0, 5.0)

    def move_relative(self, pan_delta: float, tilt_delta: float, zoom_delta: float) -> PTZState:
        self.state.pan = self._clamp(self.state.pan + pan_delta, self.pan_limits)
        self.state.tilt = self._clamp(self.state.tilt + tilt_delta, self.tilt_limits)
        self.state.zoom = self._clamp(self.state.zoom + zoom_delta, self.zoom_limits)
        return self.state

    def move_absolute(self, pan: float, tilt: float, zoom: float) -> PTZState:
        self.state.pan = self._clamp(pan, self.pan_limits)
        self.state.tilt = self._clamp(tilt, self.tilt_limits)
        self.state.zoom = self._clamp(zoom, self.zoom_limits)
        return self.state

    def get_state(self) -> PTZState:
        return self.state

    @staticmethod
    def _clamp(value: float, limits: tuple[float, float]) -> float:
        return max(limits[0], min(limits[1], value))
