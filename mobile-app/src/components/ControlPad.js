import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";

function Btn({ label, onPress }) {
  return (
    <Pressable style={styles.btn} onPress={onPress}>
      <Text style={styles.btnText}>{label}</Text>
    </Pressable>
  );
}

export default function ControlPad({ onMove }) {
  return (
    <View style={styles.wrap}>
      <View style={styles.row}>
        <Btn label="+" onPress={() => onMove(0, 0, 0.25)} />
        <Btn label="UP" onPress={() => onMove(0, 2)} />
        <Btn label="-" onPress={() => onMove(0, 0, -0.25)} />
      </View>
      <View style={styles.row}>
        <Btn label="LEFT" onPress={() => onMove(-2, 0)} />
        <View style={styles.gap} />
        <Btn label="RIGHT" onPress={() => onMove(2, 0)} />
      </View>
      <View style={styles.row}>
        <View style={styles.gap} />
        <Btn label="DOWN" onPress={() => onMove(0, -2)} />
        <View style={styles.gap} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 8 },
  row: { flexDirection: "row", justifyContent: "center", gap: 8 },
  gap: { width: 74 },
  btn: {
    minWidth: 74,
    paddingVertical: 10,
    borderRadius: 10,
    alignItems: "center",
    backgroundColor: "#2e2e39",
  },
  btnText: { color: "#fff", fontWeight: "600" },
});
