"""
tariff.py
KSEB-style electricity tariff schedule.
Defines peak and off-peak windows and returns current rate.

Peak hours   : 06:00–10:00 and 18:00–23:00  (higher cost)
Off-peak hours: rest of the day              (lower cost)
"""

from datetime import datetime


# Tariff rates in ₹ per kWh (KSEB domestic slab approximation)
PEAK_RATE     = 7.50   # ₹/kWh during peak hours
OFF_PEAK_RATE = 3.50   # ₹/kWh during off-peak hours

# Peak windows as (start_hour, end_hour) — 24h format
PEAK_WINDOWS = [
    (6, 10),    # morning peak
    (18, 23),   # evening peak
]

# Compressor power consumption in kW
COMPRESSOR_KW = 0.15   # typical 150W fridge compressor


def is_peak_hour(dt: datetime = None) -> bool:
    """Return True if the given time falls within a peak window."""
    if dt is None:
        dt = datetime.now()
    hour = dt.hour
    return any(start <= hour < end for start, end in PEAK_WINDOWS)


def current_rate(dt: datetime = None) -> float:
    """Return current electricity rate in ₹/kWh."""
    return PEAK_RATE if is_peak_hour(dt) else OFF_PEAK_RATE


def cost_for_duration(seconds: float, dt: datetime = None) -> float:
    """Calculate electricity cost for running compressor for N seconds."""
    hours = seconds / 3600
    rate  = current_rate(dt)
    return round(COMPRESSOR_KW * hours * rate, 6)


def next_peak_window(dt: datetime = None) -> tuple:
    """Return the next peak window (start_hour, end_hour) from now."""
    if dt is None:
        dt = datetime.now()
    hour = dt.hour
    for start, end in PEAK_WINDOWS:
        if hour < start:
            return (start, end)
    # Wrap to next day's first window
    return PEAK_WINDOWS[0]


if __name__ == "__main__":
    now = datetime.now()
    print(f"Current time  : {now.strftime('%H:%M')}")
    print(f"Peak hour     : {is_peak_hour(now)}")
    print(f"Current rate  : ₹{current_rate(now)}/kWh")
    print(f"Next peak     : {next_peak_window(now)}")
    print(f"Cost per hour : ₹{cost_for_duration(3600):.4f}")
