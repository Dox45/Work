"""End-of-term report card.

Reads marks.csv and subjects.csv and prints every student's term average,
their position in the class, and each class average.
"""

import csv

MARKS_FILE = "marks.csv"
SUBJECTS_FILE = "subjects.csv"
PASS_MARK = 50.0
TERM = "First term 2026/2027"


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def percent(row):
    # Every subject is marked out of 100, so the score is the percentage.
    return round(float(row["score"] or 0), 1)


def main():
    rows = load_rows(MARKS_FILE)
    subjects = {row["subject"] for row in load_rows(SUBJECTS_FILE)}

    marks = {}
    classes = {}
    for row in rows:
        if row["subject"] not in subjects:
            continue
        student = row["student"]
        classes[student] = row["class"]
        # Keep the latest mark for each subject.
        marks[(student, row["subject"])] = percent(row)

    totals = {}
    counts = {}
    for (student, subject), value in marks.items():
        totals[student] = totals.get(student, 0) + value
        counts[student] = counts.get(student, 0) + 1

    averages = {student: totals[student] / counts[student] for student in totals}

    ordered = sorted(averages, key=lambda name: (-averages[name], name))

    absent = sum(1 for row in rows if not row["score"].strip())
    print("Term results: " + TERM)
    print("Marks: " + str(len(rows)) + " recorded, " + str(absent) + " absent")

    for place, student in enumerate(ordered, start=1):
        verdict = "pass" if averages[student] >= PASS_MARK else "fail"
        print(
            student + " (" + classes[student] + "): "
            + "{:.1f}".format(averages[student]) + "%, position "
            + str(place) + " of " + str(len(ordered)) + ", " + verdict
        )

    class_totals = {}
    class_counts = {}
    for (student, subject), value in marks.items():
        cls = classes[student]
        class_totals[cls] = class_totals.get(cls, 0) + value
        class_counts[cls] = class_counts.get(cls, 0) + 1

    for cls in sorted(class_totals):
        print(
            "Class average " + cls + ": "
            + "{:.1f}".format(class_totals[cls] / class_counts[cls]) + "%"
        )


if __name__ == "__main__":
    main()
