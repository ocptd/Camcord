import React, { useEffect, useMemo, useState } from "react";
import { Image, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

import ControlPad from "../components/ControlPad";
import {
  getBackendHost,
  getStatus,
  getStreamUrl,
  movePTZ,
  setBackendHost,
  setMode,
  updateTrackerConfig,
} from "../api";

export default function HomeScreen() {
  const [hostInput, setHostInput] = useState(getBackendHost());
  const [mode, setModeState] = useState("auto");
  const [status, setStatus] = useState(null);
  const [kpPan, setKpPan] = useState("0.08");
  const [message, setMessage] = useState("");

  const streamUrl = useMemo(() => getStreamUrl(), [hostInput]);

  async function refresh() {
    try {
      const data = await getStatus();
      setModeState(data.mode);
      setStatus(data);
      setMessage("Status synced");
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function onChangeMode(nextMode) {
    try {
      await setMode(nextMode);
      setModeState(nextMode);
      setMessage(`Mode set to ${nextMode}`);
      refresh();
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function onMove(pan, tilt, zoom = 0) {
    try {
      await movePTZ(pan, tilt, zoom);
      refresh();
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function onApplyConfig() {
    const parsed = Number(kpPan);
    if (Number.isNaN(parsed)) {
      setMessage("kp_pan must be a number");
      return;
    }
    try {
      await updateTrackerConfig({ kp_pan: parsed });
      setMessage("Config updated");
      refresh();
    } catch (err) {
      setMessage(err.message);
    }
  }

  function onHostApply() {
    setBackendHost(hostInput);
    setMessage(`Backend host: ${hostInput}`);
    refresh();
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.title}>Auto Camera Control</Text>

        <Text style={styles.label}>Backend Host</Text>
        <View style={styles.row}>
          <TextInput
            style={[styles.input, { flex: 1 }]}
            value={hostInput}
            onChangeText={setHostInput}
            placeholder="192.168.1.50:8000"
            placeholderTextColor="#999"
          />
          <Pressable style={styles.primaryBtn} onPress={onHostApply}>
            <Text style={styles.btnText}>Apply</Text>
          </Pressable>
        </View>

        <Text style={styles.label}>Live Stream</Text>
        <Image source={{ uri: streamUrl }} style={styles.stream} />

        <View style={styles.row}>
          <Pressable
            style={[styles.modeBtn, mode === "auto" && styles.modeBtnActive]}
            onPress={() => onChangeMode("auto")}
          >
            <Text style={styles.btnText}>AUTO</Text>
          </Pressable>
          <Pressable
            style={[styles.modeBtn, mode === "manual" && styles.modeBtnActive]}
            onPress={() => onChangeMode("manual")}
          >
            <Text style={styles.btnText}>MANUAL</Text>
          </Pressable>
        </View>

        <Text style={styles.label}>Manual PTZ</Text>
        <ControlPad onMove={onMove} />

        <Text style={styles.label}>Tracker Config (kp_pan)</Text>
        <View style={styles.row}>
          <TextInput
            style={[styles.input, { flex: 1 }]}
            value={kpPan}
            onChangeText={setKpPan}
            keyboardType="decimal-pad"
          />
          <Pressable style={styles.primaryBtn} onPress={onApplyConfig}>
            <Text style={styles.btnText}>Save</Text>
          </Pressable>
        </View>

        <Pressable style={styles.primaryBtn} onPress={refresh}>
          <Text style={styles.btnText}>Refresh Status</Text>
        </Pressable>

        {status && (
          <View style={styles.card}>
            <Text style={styles.cardText}>Mode: {status.mode}</Text>
            <Text style={styles.cardText}>
              PTZ: pan {status.ptz.pan.toFixed(2)} | tilt {status.ptz.tilt.toFixed(2)} | zoom {status.ptz.zoom.toFixed(2)}
            </Text>
            <Text style={styles.cardText}>
              Tracking: {status.tracking?.tracking ? "active" : "inactive"}
            </Text>
          </View>
        )}
        {!!message && <Text style={styles.message}>{message}</Text>}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#0f0f12" },
  container: { padding: 16, gap: 12 },
  title: { color: "#fff", fontSize: 24, fontWeight: "700", marginBottom: 4 },
  label: { color: "#d1d1d8", fontWeight: "600" },
  stream: { width: "100%", height: 220, borderRadius: 10, backgroundColor: "#18181f" },
  row: { flexDirection: "row", gap: 8, alignItems: "center" },
  input: {
    borderWidth: 1,
    borderColor: "#31313a",
    backgroundColor: "#1c1c23",
    color: "#fff",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 10,
  },
  primaryBtn: {
    backgroundColor: "#3268ff",
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 14,
    alignItems: "center",
  },
  modeBtn: {
    flex: 1,
    backgroundColor: "#2a2a32",
    borderRadius: 8,
    paddingVertical: 10,
    alignItems: "center",
  },
  modeBtnActive: { backgroundColor: "#3268ff" },
  btnText: { color: "#fff", fontWeight: "700" },
  card: {
    backgroundColor: "#1d1d24",
    borderRadius: 10,
    padding: 12,
    gap: 4,
  },
  cardText: { color: "#d6d6de" },
  message: { color: "#9eb7ff" },
});
