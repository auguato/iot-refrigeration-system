"""
fridge_model.py
Physics-based thermal simulation of a refrigerator compartment.

Model:
  dT/dt = heat_leak_rate * (ambient - internal) - cooling_rate * compressor_on
  Heat leaks in from ambient when compressor is off.
  Compressor actively cools when on.
"""

import random
from datetime import datetime


class FridgeModel:
    def __init__(self):
        self.internal_temp   = 4.0     # °C — starting temperature
        self.ambient_temp    = 28.0    # °C — room temperature (Kerala climate)
        self.heat_leak_rate  = 0.03    # °C/s leak from ambient into fridge
        self.cooling_rate    = 0.12    # °C/s drop when compressor is ON
        self.compressor_on   = False
        self.door_open       = False

    def step(self, dt: float = 1.0) -> dict:
        """
        Advance simulation by dt seconds.
        Returns current sensor readings.
        """
        # Door open adds extra heat leak
        effective_leak = self.heat_leak_rate * (3.0 if self.door_open else 1.0)

        # Temperature change this tick
        heat_in  = effective_leak * (self.ambient_temp - self.internal_temp) * dt
        cool_out = self.cooling_rate * dt if self.compressor_on else 0.0

        self.internal_temp += heat_in - cool_out

        # Clamp to physical limits
        self.internal_temp = max(-5.0, min(self.ambient_temp, self.internal_temp))

        # Add tiny sensor noise
        measured_temp = round(self.internal_temp + random.uniform(-0.1, 0.1), 2)

        return {
            "timestamp":      datetime.now().isoformat(),
            "internal_temp":  measured_temp,
            "ambient_temp":   self.ambient_temp,
            "compressor_on":  self.compressor_on,
            "door_open":      self.door_open,
        }

    def set_compressor(self, state: bool):
        self.compressor_on = state

    def simulate_door_event(self, probability: float = 0.02):
        """Randomly open/close door to simulate real usage."""
        if self.door_open:
            self.door_open = random.random() < 0.3   # 30% chance door closes
        else:
            self.door_open = random.random() < probability


if __name__ == "__main__":
    fridge = FridgeModel()
    fridge.set_compressor(True)
    print("Simulating fridge for 60 seconds...\n")
    for i in range(60):
        reading = fridge.step(dt=1.0)
        fridge.simulate_door_event()
        print(f"[{i:02d}s] Temp: {reading['internal_temp']}°C | "
              f"Compressor: {'ON' if reading['compressor_on'] else 'OFF'} | "
              f"Door: {'OPEN' if reading['door_open'] else 'closed'}")
