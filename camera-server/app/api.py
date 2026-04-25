from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models import (
    ModePayload,
    PTZMovePayload,
    TrackerConfigPayload,
    TrackerInitPayload,
)


def build_router(state) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/health")
    def health():
        return {"ok": True}

    @router.get("/status")
    def status():
        ptz = state["ptz"].get_state()
        tracking = state["tracking_info"]
        return {
            "mode": state["mode"],
            "ptz": {"pan": ptz.pan, "tilt": ptz.tilt, "zoom": ptz.zoom},
            "tracking": tracking,
        }

    @router.post("/mode")
    def set_mode(payload: ModePayload):
        state["mode"] = payload.mode
        return {"mode": state["mode"]}

    @router.post("/ptz/move")
    def move_ptz(payload: PTZMovePayload):
        ptz_state = state["ptz"].move_relative(
            payload.pan_delta, payload.tilt_delta, payload.zoom_delta
        )
        return {"pan": ptz_state.pan, "tilt": ptz_state.tilt, "zoom": ptz_state.zoom}

    @router.post("/tracker/init")
    def init_tracker(payload: TrackerInitPayload):
        frame = state["camera"].get_latest()
        if frame is None:
            return JSONResponse(status_code=400, content={"error": "No frame available yet"})
        try:
            state["tracker"].init_tracker(frame, (payload.x, payload.y, payload.w, payload.h))
        except RuntimeError as exc:
            return JSONResponse(status_code=500, content={"error": str(exc)})
        return {"tracking": True}

    @router.post("/tracker/reset")
    def reset_tracker():
        state["tracker"].reset_tracker()
        return {"tracking": False}

    @router.post("/config")
    def set_config(payload: TrackerConfigPayload):
        updated = state["tracker"].set_config(payload.model_dump())
        return {"tracker_config": updated}

    return router
