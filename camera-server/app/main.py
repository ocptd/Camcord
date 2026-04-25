from __future__ import annotations

from threading import Thread
from time import sleep

import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.api import build_router
from app.camera import CameraStream
from app.config import APP_CONFIG
from app.ptz import SimulatedPTZController
from app.tracker import TrackingService

app = FastAPI(title="Auto Camera Control System")

ptz = SimulatedPTZController()
camera = CameraStream(
    source=APP_CONFIG.camera.source,
    width=APP_CONFIG.camera.width,
    height=APP_CONFIG.camera.height,
    fps=APP_CONFIG.camera.fps,
)
tracking_service = TrackingService(APP_CONFIG.tracker, ptz)

APP_STATE = {
    "mode": APP_CONFIG.mode,
    "ptz": ptz,
    "camera": camera,
    "tracker": tracking_service,
    "tracking_info": {"tracking": False, "bbox": None, "control": {}},
}


def vision_loop():
    while True:
        frame = camera.read()
        if frame is None:
            continue

        if APP_STATE["mode"] == "auto":
            info = tracking_service.update(frame)
        else:
            info = {
                "tracking": tracking_service.last_box is not None,
                "bbox": tracking_service.last_box,
                "control": {"pan_delta": 0.0, "tilt_delta": 0.0, "zoom_delta": 0.0},
            }
        APP_STATE["tracking_info"] = info
        sleep(0.01)


def mjpeg_generator():
    while True:
        frame = camera.get_latest()
        if frame is None:
            sleep(0.02)
            continue

        info = APP_STATE["tracking_info"]
        if info.get("bbox"):
            x, y, w, h = info["bbox"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (40, 255, 40), 2)
        cv2.putText(
            frame,
            f"Mode: {APP_STATE['mode']}",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        ok, jpeg = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        payload = jpeg.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + payload + b"\r\n"
        )


@app.on_event("startup")
def startup():
    thread = Thread(target=vision_loop, daemon=True)
    thread.start()


@app.on_event("shutdown")
def shutdown():
    camera.release()


@app.get("/stream.mjpeg")
def stream():
    return StreamingResponse(
        mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


app.include_router(build_router(APP_STATE))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
