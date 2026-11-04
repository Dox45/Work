"""Tutoring hours report.

Reads sessions.csv and prints how many hours each tutor taught last week.
"""

import csv

FILENAME = "sessions.csv"


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def to_minutes(stamp):
    # "14:30" -> 870. Splitting on the colon copes with "9:00" as well.
    parts = stamp.strip().split(":")
    return int(parts[0]) * 60 + int(parts[1])


def session_hours(row):
    # Work in minutes so the odd quarters of an hour are kept.
    return (to_minutes(row["end"]) - to_minutes(row["start"])) / 60


def main():
    rows = load_rows(FILENAME)

    per_tutor = {}
    sessions = {}
    completed = 0
    all_hours = 0.0
    longest = None

    for row in rows:
        # Only completed sessions count towards anything.
        if row["status"] != "completed":
            continue

        # A stray space in a name must not split one tutor into two.
        tutor = row["tutor"].strip()

        completed = completed + 1
        length = session_hours(row)
        per_tutor[tutor] = per_tutor.get(tutor, 0) + length
        sessions[tutor] = sessions.get(tutor, 0) + 1
        all_hours = all_hours + length

        if longest is None or length > longest[0]:
            longest = (length, row["session_id"])

    print("Sessions logged: " + str(len(rows)))
    print(
        "Completed: " + str(completed) + " ("
        + "{:.1f}".format(completed / len(rows) * 100) + "%)"
    )

    # One line per tutor, most hours first.
    for tutor in sorted(per_tutor, key=lambda name: per_tutor[name], reverse=True):
        print(
            tutor + ": " + str(sessions[tutor]) + " sessions, "
            + "{:.1f}".format(per_tutor[tutor]) + " h, avg "
            + "{:.1f}".format(per_tutor[tutor] / sessions[tutor]) + " h"
        )

    print(
        "Longest session: " + longest[1] + " "
        + "{:.1f}".format(longest[0]) + " h"
    )

    print("Total hours: " + "{:.1f}".format(all_hours) + " h")


if __name__ == "__main__":
    main()
