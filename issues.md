# Issue Table - radio_schedule.py

Tools: Pylint (before 2.41/10), Bandit (1 Low, 2 Medium), Flake8 (5 findings).
Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL injection via string formatting (Bandit B608, Medium) | Security | 12 | `addSlot` builds the INSERT with `%` formatting, so a show name such as `x'); DROP TABLE slots;--` is run as SQL. | Use a parameterised query: `VALUES (?, ?, ?, ?)` with a tuple of values. |
| `eval()` on a caller-supplied string (Bandit B307, Medium; Pylint W0123) | Security | 22 | `overlapFree(formula)` executes arbitrary Python, which allows code execution. | Remove `eval`. Replace with `overlap_free(first_start_hour, first_minutes, second_start_hour)`, which does the arithmetic directly. |
| Hardcoded password (Bandit B105, Low) | Security | 6 | `STUDIO_PASSWORD = "onair2024"` is a secret committed to source control. | Read it from the environment: `os.environ.get("STUDIO_PASSWORD", "")`. |
| Overly broad `except Exception` (Pylint W0718) | Bug | 23 | Every error, including typos and bugs, silently becomes `False`, which hides real faults. | Removed together with `eval`; the new function cannot fail this way. |
| Global mutable state: `global` statement and a drifting counter (Pylint W0603, C0103) | Bug | 7, 11 | `booked_minutes` is a module-level global. `removeSlot` never decrements it, so it goes out of sync with the database. It is also used only as a guard in `morningShows`. | Remove the global. Pass the connection into each function, and query the database directly. |
| No input validation | Bug | 10-13 | `addSlot` accepts empty names, hour 99, zero or negative minutes, and slots running past midnight. | New `_validate_slot` raises `ValueError`. `remove_slot` also validates the id and returns whether a row was deleted. |
| Multiple statements on one line (Flake8 E701, Pylint C0321) | Style | 28 | `if ...: return [...]` is on one line. | Resolved by removing the `booked_minutes` guard, so the function is a single statement. |
| Lines too long (Flake8 E501, Pylint C0301) | Style | 4, 12, 28 | Lines of 118, 135 and 110 characters. | Split the SQL strings across lines and build the connection in `create_connection()`. |
| Missing docstrings (Pylint C0114, C0116) | Quality | 1, 10, 16, 20, 27, 32, 36 | The module and all six functions have no docstrings. | Added a one-line docstring to the module and every function. |
| camelCase function names (Pylint C0103) | Style | 10, 16, 20, 27, 32 | `addSlot`, `slotLabel`, `overlapFree`, `morningShows`, `removeSlot` break PEP 8 snake_case. | Renamed to `add_slot`, `slot_label`, `overlap_free`, `morning_shows`, `remove_slot`. |
| Old-style string formatting (Pylint C0209) | Quality | 12, 17 | `%` and `.format()` where an f-string is clearer. | Use `f"{show} hosted by {host}"`. |
| No blank-line spacing or `__main__` guard (Flake8 E305) | Style | 43 | `main()` runs on import, and only one blank line precedes it. | Added two blank lines and `if __name__ == "__main__":`. |

## Verification

| Tool | Before | After |
| ---- | ------ | ----- |
| Pylint | 2.41/10 (21 messages) | 10.00/10 |
| Bandit | 1 Low, 2 Medium | No issues identified |
| Flake8 | 5 findings | 0 findings |

The demo output is the same before and after:
```
Sunrise Beats hosted by Vik
True ['Sunrise Beats']
```
