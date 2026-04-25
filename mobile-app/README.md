# Mobile App

React Native Expo app for:
- viewing live MJPEG stream,
- switching auto/manual mode,
- manual PTZ control,
- updating tracker gain.

## Run

```bash
npm install
npm run start
```

Then open on:
- Expo Go on phone, or
- Android/iOS emulator.

## Backend Host

Set backend host in the app as:
- `127.0.0.1:8000` for local emulator setups,
- `<your-lan-ip>:8000` for physical phones on same network.
