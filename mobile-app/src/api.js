const DEFAULT_HOST = "127.0.0.1:8000";
let backendHost = DEFAULT_HOST;

export function setBackendHost(host) {
  backendHost = host?.trim() ? host.trim() : DEFAULT_HOST;
}

export function getBackendHost() {
  return backendHost;
}

function endpoint(path) {
  return `http://${backendHost}${path}`;
}

export function getStreamUrl() {
  return endpoint("/stream.mjpeg");
}

export async function getStatus() {
  const res = await fetch(endpoint("/api/status"));
  if (!res.ok) throw new Error("Failed to fetch status");
  return res.json();
}

export async function setMode(mode) {
  const res = await fetch(endpoint("/api/mode"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode }),
  });
  if (!res.ok) throw new Error("Failed to set mode");
  return res.json();
}

export async function movePTZ(pan_delta, tilt_delta, zoom_delta = 0) {
  const res = await fetch(endpoint("/api/ptz/move"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pan_delta, tilt_delta, zoom_delta }),
  });
  if (!res.ok) throw new Error("Failed to move PTZ");
  return res.json();
}

export async function updateTrackerConfig(configPatch) {
  const res = await fetch(endpoint("/api/config"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(configPatch),
  });
  if (!res.ok) throw new Error("Failed to update config");
  return res.json();
}
