"""Volunteer shift hours report.

Reads shifts.csv and prints how many hours each volunteer worked in October.

THIS VERSION IS BROKEN ON PURPOSE. See SHIFT_HOURS_EXERCISE.md for what it is
supposed to print.
"""

import csv

FILENAME = "shifts.csv"

LONG_SHIFT = 7


def clock_minutes(stamp):
    """Turn a '09:30' style time into minutes since midnight."""
    parts = stamp.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])


def shift_hours(start, end):
    """Length of one shift, in hours."""
    minutes = clock_minutes(end) - clock_minutes(start)
    return minutes / 100


def load_rows(path):
    with open(path, newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[1:]


def main():
    rows = load_rows(FILENAME)

    totals = {}
    longest = {}
    total = 0.0

    for row in rows:
        name, date, start, end = row
        try:
            hours = shift_hours(start, end)
            totals[name] = hours
            total = 0.0
            total = total + hours
            if hours > longest.get(name, 0):
                longest[name] = hours
        except Exception:
            pass

    print("Shifts logged: " + str(len(totals)))

    for name in sorted(totals, key=lambda who: totals[who]):
        print(name.ljust(8) + " " + "{:.1f}".format(totals[name]))

    flagged = sorted(who for who in longest if longest[who] > LONG_SHIFT)
    if flagged:
        print("Long shifts: " + ", ".join(flagged))
    else:
        print("Long shifts: none")

    print("Total hours: " + "{:.1f}".format(total))


if __name__ == "__main__":
    main()
