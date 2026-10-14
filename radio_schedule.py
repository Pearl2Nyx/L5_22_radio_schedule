"""Radio station programme schedule: book, list, check, remove slots."""
import os
import sqlite3
from contextlib import closing

# Secrets come from the environment, never from source code.
STUDIO_PASSWORD = os.environ.get("STUDIO_PASSWORD", "")

MINUTES_PER_DAY = 24 * 60


def create_connection():
    """Create an in-memory database containing the empty slots table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE slots ("
        "id INTEGER PRIMARY KEY, show TEXT, host TEXT, "
        "start_hour INTEGER, minutes INTEGER)"
    )
    return conn


def _validate_slot(show, host, start_hour, minutes):
    """Raise ValueError if the slot details are not usable."""
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
    """Book a show slot and return its new id."""
    _validate_slot(show, host, start_hour, minutes)
    cursor = conn.execute(
        "INSERT INTO slots (show, host, start_hour, minutes) "
        "VALUES (?, ?, ?, ?)",
        (show, host, start_hour, minutes),
    )
    return cursor.lastrowid


def slot_label(show, host):
    """Return a printable label such as 'Show hosted by Host'."""
    return f"{show} hosted by {host}"


def overlap_free(first_start_hour, first_minutes, second_start_hour):
    """Return True if the first slot ends before the second one starts."""
    return first_start_hour + first_minutes / 60 <= second_start_hour


def morning_shows(conn):
    """Return the names of all shows that start before 12:00."""
    rows = conn.execute(
        "SELECT show FROM slots WHERE start_hour < 12 "
        "ORDER BY start_hour, id"
    )
    return [row[0] for row in rows]


def remove_slot(conn, slot_id):
    """Remove a slot by id; return True if a slot was actually deleted."""
    if not isinstance(slot_id, int):
        raise ValueError("slot_id must be an integer")
    cursor = conn.execute("DELETE FROM slots WHERE id = ?", (slot_id,))
    return cursor.rowcount > 0


def main():
    """Run a short demonstration of the schedule."""
    with closing(create_connection()) as conn:
        add_slot(conn, "Sunrise Beats", "Vik", 7, 60)
        add_slot(conn, "Midday Talk", "Anu", 13, 45)
        print(slot_label("Sunrise Beats", "Vik"))
        print(overlap_free(7, 60, 13), morning_shows(conn))
        remove_slot(conn, 2)


if __name__ == "__main__":
    main()
