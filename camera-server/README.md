# Camera Server

FastAPI + OpenCV service for:
- camera capture,
- object tracking,
- automatic PTZ control,
- MJPEG live streaming.

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Notes

- Default camera source is `0` (webcam).
- Change camera source in `app/config.py`.
- Mobile app should point to `<your-lan-ip>:8000` when running on a real phone.
