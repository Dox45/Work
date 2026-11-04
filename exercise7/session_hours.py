"""Tutoring hours report.

Reads sessions.csv and prints how many hours each tutor taught last week.

THIS VERSION IS BROKEN ON PURPOSE. See SESSION_HOURS_EXERCISE.md for what it
is supposed to print.
"""

import csv

FILENAME = "sessions.csv"


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def session_hours(row):
    # Take the hour part of "14:30" and subtract.
    start = int(row["start"][:2])
    end = int(row["end"][:2])
    return end - start


def main():
    rows = load_rows(FILENAME)

    # The first row is the column headings.
    rows = rows[1:]

    per_tutor = {}
    sessions = {}
    completed = 0
    all_hours = 0

    for row in rows:
        tutor = row["tutor"]

        # No-shows do not count.
        if row["status"] == "no-show":
            continue

        completed = completed + 1
        length = session_hours(row)
        per_tutor[tutor] = per_tutor.get(tutor, 0) + length
        sessions[tutor] = sessions.get(tutor, 0) + 1
        all_hours = all_hours + length

    print("Sessions logged: " + str(len(rows)))
    print(
        "Completed: " + str(completed) + " ("
        + "{:.1f}".format(completed / len(per_tutor) * 100) + "%)"
    )

    # One line per tutor, in alphabetical order.
    for tutor in sorted(per_tutor):
        booked = 0
        for row in rows:
            if row["tutor"] == tutor:
                booked = booked + 1
        print(
            tutor + ": " + str(sessions[tutor]) + " sessions, "
            + "{:.1f}".format(per_tutor[tutor]) + " h, avg "
            + "{:.1f}".format(per_tutor[tutor] / booked) + " h"
        )

    # The longest session is the one that finished latest.
    latest = rows[0]
    for row in rows:
        if row["end"] > latest["end"]:
            latest = row
    print(
        "Longest session: " + latest["session_id"] + " "
        + "{:.1f}".format(session_hours(latest)) + " h"
    )

    print("Total hours: " + "{:.1f}".format(all_hours) + " h")


if __name__ == "__main__":
    main()
