# IoT-Based Refrigeration System

A utility-aware smart refrigeration controller that simulates IoT sensor data, runs a tariff-optimised state machine, and visualises results on a live dashboard.

## Problem
Household refrigerators run compressors regardless of electricity tariff windows, wasting money during expensive peak hours.

## Solution
A four-state controller (IDLE → PRE_COOL → PEAK_HOLD → RESUME) that pre-chills the fridge before peak hours and holds temperature safely without the compressor during expensive windows — saving cost while maintaining food safety.

## Features
- Physics-based fridge thermal simulation (heat leak + compressor cooling model)
- KSEB-style peak/off-peak tariff schedule (₹7.50 vs ₹3.50 per kWh)
- Four-state control machine with hardware safety override (never exceeds 8°C)
- MQTT publishing via paho-mqtt to HiveMQ cloud broker
- SQLite time-series storage
- Streamlit dashboard: live temperature, compressor state, savings tracker

## Project Structure
```
iot-refrigeration-system/
├── simulator/fridge_model.py     # Thermal physics simulation
├── controller/state_machine.py   # IDLE→PRE_COOL→PEAK_HOLD→RESUME logic
├── controller/tariff.py          # KSEB tariff schedule
├── mqtt/publisher.py             # MQTT data publisher
├── storage/db.py                 # SQLite storage
├── dashboard/dashboard.py        # Streamlit live dashboard
└── requirements.txt
```

## How to Run
```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

## Tech Stack
- Python 3.11, paho-mqtt, Streamlit, SQLite, HiveMQ
