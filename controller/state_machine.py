"""
state_machine.py
Utility-aware refrigeration controller.

States:
  IDLE       — Normal operation, compressor runs as needed
  PRE_COOL   — Actively cools fridge to PRE_COOL_TARGET before peak window
  PEAK_HOLD  — Peak hours: compressor OFF unless safety threshold breached
  RESUME     — Peak window ended, return to normal operation

Safety rule: if internal temp > SAFETY_MAX_TEMP, compressor ALWAYS turns on
             regardless of tariff state.
"""

from enum import Enum
from datetime import datetime
from controller.tariff import is_peak_hour, next_peak_window, cost_for_duration



NORMAL_TARGET   = 4.0   
PRE_COOL_TARGET = 2.0   
SAFETY_MAX_TEMP = 8.0    
COMPRESSOR_ON_TEMP  = NORMAL_TARGET + 1.0   
COMPRESSOR_OFF_TEMP = NORMAL_TARGET - 0.5  
PRE_COOL_LEAD_HOURS = 1  


class State(Enum):
    IDLE      = "IDLE"
    PRE_COOL  = "PRE_COOL"
    PEAK_HOLD = "PEAK_HOLD"
    RESUME    = "RESUME"


class RefrigerationController:
    def __init__(self):
        self.state            = State.IDLE
        self.compressor_on    = False
        self.total_peak_saves = 0.0   
        self.peak_off_seconds = 0.0   
        self.log              = []

    def decide(self, internal_temp: float, dt: datetime = None) -> bool:
        """
        Given current internal temperature and time, decide compressor state.
        Returns True = compressor ON, False = compressor OFF.
        """
        if dt is None:
            dt = datetime.now()

        peak_now = is_peak_hour(dt)
        next_peak_start, _ = next_peak_window(dt)
        hours_to_peak = (next_peak_start - dt.hour) % 24

        prev_state = self.state

       
        if internal_temp > SAFETY_MAX_TEMP:
            self.compressor_on = True
            self._log(dt, internal_temp, "SAFETY OVERRIDE — temp too high")
            return self.compressor_on

       
        if peak_now:
            self.state = State.PEAK_HOLD
        elif not peak_now and self.state == State.PEAK_HOLD:
            self.state = State.RESUME
        elif hours_to_peak <= PRE_COOL_LEAD_HOURS and not peak_now:
            self.state = State.PRE_COOL
        else:
            if self.state == State.RESUME:
                
                if abs(internal_temp - NORMAL_TARGET) < 0.5:
                    self.state = State.IDLE
            elif self.state not in (State.PRE_COOL, State.PEAK_HOLD):
                self.state = State.IDLE

      
        if self.state == State.IDLE:
            if internal_temp > COMPRESSOR_ON_TEMP:
                self.compressor_on = True
            elif internal_temp < COMPRESSOR_OFF_TEMP:
                self.compressor_on = False

        elif self.state == State.PRE_COOL:
          
            self.compressor_on = internal_temp > PRE_COOL_TARGET

        elif self.state == State.PEAK_HOLD:
         
            if self.compressor_on:
               
                self.peak_off_seconds += 1
                self.total_peak_saves += cost_for_duration(1)
            self.compressor_on = False

        elif self.state == State.RESUME:
            
            self.compressor_on = internal_temp > NORMAL_TARGET

        if prev_state != self.state:
            self._log(dt, internal_temp, f"State → {self.state.value}")

        return self.compressor_on

    def _log(self, dt, temp, note):
        entry = {
            "time":  dt.strftime("%H:%M:%S"),
            "temp":  temp,
            "state": self.state.value,
            "note":  note,
        }
        self.log.append(entry)
        print(f"[{entry['time']}] {entry['state']:10s} | {temp}°C | {note}")

    def savings_summary(self) -> dict:
        return {
            "peak_off_minutes": round(self.peak_off_seconds / 60, 1),
            "estimated_savings_inr": round(self.total_peak_saves, 4),
        }


if __name__ == "__main__":
    ctrl = RefrigerationController()
    print(f"Controller initialised. State: {ctrl.state.value}\n")
   
    test_temp = 5.5
    result = ctrl.decide(test_temp)
    print(f"Temp={test_temp}°C → Compressor={'ON' if result else 'OFF'} | State={ctrl.state.value}")
