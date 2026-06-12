"""
db.py
SQLite storage for fridge sensor and relay readings.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fridge.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp      TEXT    NOT NULL,
            internal_temp  REAL,
            ambient_temp   REAL,
            door_open      INTEGER,
            compressor_on  INTEGER,
            state          TEXT,
            tariff_rate    REAL,
            peak_hour      INTEGER
        )
    """)
    conn.commit()
    conn.close()


def save_reading(r: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO readings
          (timestamp, internal_temp, ambient_temp, door_open,
           compressor_on, state, tariff_rate, peak_hour)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        r.get("timestamp"), r.get("internal_temp"), r.get("ambient_temp"),
        int(r.get("door_open", False)), int(r.get("compressor_on", False)),
        r.get("state"), r.get("tariff_rate"), int(r.get("peak_hour", False))
    ))
    conn.commit()
    conn.close()


def get_recent(limit: int = 200) -> list:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]


def get_savings() -> dict:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("""
        SELECT
          SUM(CASE WHEN compressor_on=0 AND peak_hour=1 THEN 1 ELSE 0 END) as peak_off_ticks,
          MIN(internal_temp) as min_temp,
          MAX(internal_temp) as max_temp,
          AVG(internal_temp) as avg_temp
        FROM readings
    """).fetchone()
    conn.close()
    peak_off_ticks = row[0] or 0
    # Each tick = 5 seconds; compressor = 0.15kW; savings vs peak rate ₹7.50
    saved = round((peak_off_ticks * 5 / 3600) * 0.15 * 7.50, 4)
    return {
        "peak_off_minutes":       round(peak_off_ticks * 5 / 60, 1),
        "estimated_savings_inr":  saved,
        "min_temp": round(row[1] or 0, 2),
        "max_temp": round(row[2] or 0, 2),
        "avg_temp": round(row[3] or 0, 2),
    }
