"""Volunteer shift hours report.

Reads shifts.csv and prints how many hours each volunteer worked in October.
"""

import csv
import sys

FILENAME = "shifts.csv"

LONG_SHIFT = 7


def clock_minutes(stamp):
    """Turn a '09:30' style time into minutes since midnight."""
    parts = stamp.strip().split(":")
    if len(parts) != 2:
        raise ValueError("time must look like HH:MM, got " + repr(stamp))
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        raise ValueError("time must look like HH:MM, got " + repr(stamp))
    if not 0 <= hours <= 23 or not 0 <= minutes <= 59:
        raise ValueError("time is out of range: " + repr(stamp))
    return hours * 60 + minutes


def shift_hours(start, end):
    """Length of one shift, in hours."""
    minutes = clock_minutes(end) - clock_minutes(start)
    if minutes < 0:
        raise ValueError("shift ends before it starts: " + start + " to " + end)
    return minutes / 60


def load_rows(path):
    """Return (line number, row) pairs, skipping blank lines."""
    with open(path, newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return []
    loaded = []
    for offset, row in enumerate(rows[1:], start=2):
        if not any(field.strip() for field in row):
            continue
        loaded.append((offset, row))
    return loaded


def report(path):
    totals = {}
    longest = {}
    total = 0.0
    shifts = 0
    problems = []

    for line_number, row in load_rows(path):
        if len(row) != 4:
            problems.append(
                "line " + str(line_number) + ": expected 4 fields, found " + str(len(row))
            )
            continue
        name, date, start, end = (field.strip() for field in row)
        if not name:
            problems.append("line " + str(line_number) + ": no volunteer name")
            continue
        try:
            hours = shift_hours(start, end)
        except ValueError as error:
            problems.append("line " + str(line_number) + ": " + str(error))
            continue
        shifts = shifts + 1
        totals[name] = totals.get(name, 0.0) + hours
        total = total + hours
        if hours > longest.get(name, 0.0):
            longest[name] = hours

    print("Shifts logged: " + str(shifts))

    for name in sorted(totals, key=lambda who: (-totals[who], who)):
        print(name.ljust(8) + " " + "{:.1f}".format(totals[name]).rjust(4))

    flagged = sorted(who for who in longest if longest[who] >= LONG_SHIFT)
    if flagged:
        print("Long shifts: " + ", ".join(flagged))
    else:
        print("Long shifts: none")

    print("Total hours: " + "{:.1f}".format(total))

    for problem in problems:
        print("Skipped " + problem, file=sys.stderr)


def main():
    report(FILENAME)


if __name__ == "__main__":
    main()
