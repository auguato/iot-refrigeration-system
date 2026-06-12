"""
publisher.py
Publishes fridge sensor + relay state to HiveMQ cloud broker via MQTT.
Topics:
  fridge/sensor  — temperature, door state
  fridge/relay   — compressor on/off, controller state
"""

import json
import time
import sys
import os
import paho.mqtt.client as mqtt

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from simulator.fridge_model import FridgeModel
from controller.state_machine import RefrigerationController
from controller.tariff import current_rate, is_peak_hour
from storage.db import init_db, save_reading

# ── Broker config ─────────────────────────────────────────────────────────────
BROKER   = "broker.hivemq.com"
PORT     = 1883
INTERVAL = 5    # seconds between ticks
# ──────────────────────────────────────────────────────────────────────────────


def on_connect(client, userdata, flags, rc):
    status = "Connected" if rc == 0 else f"Failed (code {rc})"
    print(f"MQTT broker: {status}")


def run():
    init_db()

    fridge  = FridgeModel()
    ctrl    = RefrigerationController()
    client  = mqtt.Client(client_id="iot-fridge-sim-01")
    client.on_connect = on_connect
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    print("IoT Refrigeration System running... Press Ctrl+C to stop.\n")

    try:
        while True:
            # 1. Simulate fridge physics
            reading = fridge.step(dt=float(INTERVAL))
            fridge.simulate_door_event()

            # 2. Controller decides compressor state
            compressor = ctrl.decide(reading["internal_temp"])
            fridge.set_compressor(compressor)

            # 3. Build payloads
            sensor_payload = {
                "timestamp":     reading["timestamp"],
                "internal_temp": reading["internal_temp"],
                "ambient_temp":  reading["ambient_temp"],
                "door_open":     reading["door_open"],
            }
            relay_payload = {
                "timestamp":    reading["timestamp"],
                "compressor_on": compressor,
                "state":        ctrl.state.value,
                "tariff_rate":  current_rate(),
                "peak_hour":    is_peak_hour(),
            }

            # 4. Publish to MQTT
            client.publish("fridge/sensor", json.dumps(sensor_payload), qos=1)
            client.publish("fridge/relay",  json.dumps(relay_payload),  qos=1)

            # 5. Save to local DB
            save_reading({**sensor_payload, **relay_payload})

            print(f"[{reading['timestamp'][11:19]}] "
                  f"Temp: {reading['internal_temp']}°C | "
                  f"State: {ctrl.state.value:10s} | "
                  f"Compressor: {'ON ' if compressor else 'OFF'} | "
                  f"Peak: {'YES' if is_peak_hour() else 'no '} | "
                  f"Rate: ₹{current_rate()}/kWh")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping. Savings summary:")
        print(ctrl.savings_summary())
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()
