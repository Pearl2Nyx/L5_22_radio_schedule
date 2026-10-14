
import os
import sqlite3
from contextlib import closing


STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD", "")

MINUTES_PER_DAY = 24 * 60


def create_connection():
    
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE slots ("
        "id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
        "start_hour INTEGER, minutes INTEGER)"
    )
    return conn


def _validate_slot(show, host, start_hour, minutes):
    if not isinstance(show, str) or not show.strip():
        raise ValueError("show must be a non-empty string")
    if not isinstance(host, str) or not host.strip():
        raise ValueError("host must be a non-empty string")
    if not isinstance(start_hour, int) or not 0 <= start_hour <= 23:
        raise ValueError("start_hour must be an integer from 0 to 23")
    if not isinstance(minutes, int) or minutes <= 0:
        raise ValueError("minutes must be a positive integer")
    if start_hour * 60 + minutes > MINUTES_PER_DAY:
        raise ValueError("slot must end by midnight")


def add_slot(conn, show, host, start_hour, minutes):
    _validate_slot(show, host, start_hour, minutes)
    cursor = conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )
    return cursor.lastrowid


def slot_label(show, host):
    return f"{show} hosted by {host}"


def overlap_free(first_start_hour, first_minutes, second_start_hour):
    return first_start_hour + first_minutes / 60 <= second_start_hour


def morning_shows(conn):
    rows = conn.execute(
        "SELECT show FROM slots WHERE start_hour < 12 "
        "ORDER BY start_hour, id"
    )
    return [row[0] for row in rows]


def remove_slot(conn, slot_id):
    if not isinstance(slot_id, int):
        raise ValueError("slot_id must be an integer")
    cursor = conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))
    return cursor.rowcount > 0


def main():
    with closing(create_connection()) as conn:
        add_slot(conn, "Sunrise Beats", "Vik", 7, 60)
        add_slot(conn, "Midday Talk", "Anu", 13, 45)
        print(slot_label("Sunrise Beats", "Vik"))
        print(overlap_free(7, 60, 13), morning_shows(conn))
        remove_slot(conn, 2)


if __name__ == "__main__":
    main()
