"""
dashboard.py
Streamlit dashboard for the IoT-Based Refrigeration System.
Run with: streamlit run dashboard/dashboard.py
"""

import sys
import os
import time
import pandas as pd
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from simulator.fridge_model import FridgeModel
from controller.state_machine import RefrigerationController
from controller.tariff import current_rate, is_peak_hour, PEAK_RATE, OFF_PEAK_RATE
from storage.db import init_db, save_reading, get_recent, get_savings

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IoT Refrigeration System",
    page_icon="❄️",
    layout="wide"
)

init_db()

# ── Session state — persist fridge and controller across reruns ───────────────
if "fridge" not in st.session_state:
    st.session_state.fridge = FridgeModel()
if "ctrl" not in st.session_state:
    st.session_state.ctrl = RefrigerationController()

fridge = st.session_state.fridge
ctrl   = st.session_state.ctrl

# ── Simulate one tick ─────────────────────────────────────────────────────────
reading    = fridge.step(dt=5.0)
fridge.simulate_door_event()
compressor = ctrl.decide(reading["internal_temp"])
fridge.set_compressor(compressor)

save_reading({
    **reading,
    "compressor_on": compressor,
    "state":         ctrl.state.value,
    "tariff_rate":   current_rate(),
    "peak_hour":     is_peak_hour(),
})

savings = get_savings()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("❄️ IoT-Based Refrigeration System")
st.caption("Utility-aware smart fridge controller — KSEB tariff optimised")

# ── Peak hour banner ──────────────────────────────────────────────────────────
if is_peak_hour():
    st.warning(f"⚡ PEAK HOURS ACTIVE — Compressor held OFF to save cost | Rate: ₹{PEAK_RATE}/kWh")
else:
    st.success(f"✅ Off-peak hours — Normal operation | Rate: ₹{OFF_PEAK_RATE}/kWh")

# ── Metric cards ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Internal Temp",   f"{reading['internal_temp']} °C")
c2.metric("Compressor",      "ON 🟢" if compressor else "OFF 🔴")
c3.metric("Controller State", ctrl.state.value)
c4.metric("Peak Off (mins)", savings["peak_off_minutes"])
c5.metric("Est. Savings",    f"₹{savings['estimated_savings_inr']}")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────
recent = get_recent(300)

if recent:
    df = pd.DataFrame(recent)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Temperature over time")
        temp_df = df.set_index("timestamp")[["internal_temp", "ambient_temp"]]
        st.line_chart(temp_df)

    with col_right:
        st.subheader("Compressor state")
        comp_df = df.set_index("timestamp")[["compressor_on"]]
        st.area_chart(comp_df)

    st.subheader("Tariff rate over time")
    tariff_df = df.set_index("timestamp")[["tariff_rate"]]
    st.line_chart(tariff_df)

    st.subheader("Recent readings")
    display_cols = ["timestamp", "internal_temp", "state", "compressor_on", "peak_hour", "tariff_rate"]
    st.dataframe(df[display_cols].tail(15).iloc[::-1], use_container_width=True)

# ── Savings analysis ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Savings analysis")
sa, sb, sc = st.columns(3)
sa.metric("Min Temp recorded", f"{savings['min_temp']} °C")
sb.metric("Max Temp recorded", f"{savings['max_temp']} °C")
sc.metric("Avg Temp",          f"{savings['avg_temp']} °C")

# ── Auto-refresh ──────────────────────────────────────────────────────────────
time.sleep(5)
st.rerun()
