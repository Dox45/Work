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


def fail(message):
    """Stop and name the row rather than print a report that cannot be true."""
    raise SystemExit("Error: " + message)


def percent(row, row_number):
    # Each subject has its own maximum, so the percentage is the mark against
    # that maximum, not the mark itself.
    score = float(row["score"])
    maximum = float(row["max_score"])
    if maximum <= 0:
        fail(
            "row " + str(row_number) + " (" + row["student"] + ", "
            + row["class"] + ", " + row["subject"] + ") has no usable maximum."
        )
    if score < 0 or score > maximum:
        fail(
            "row " + str(row_number) + " (" + row["student"] + ", "
            + row["class"] + ", " + row["subject"] + ") has a mark of "
            + row["score"] + " out of " + row["max_score"] + "."
        )
    return score / maximum * 100.0


def main():
    rows = load_rows(MARKS_FILE)
    weights = {row["subject"]: float(row["weight"]) for row in load_rows(SUBJECTS_FILE)}

    # A student is a name and a class: two students who share a name are still
    # two people. The best attempt at each subject counts, so a resit only
    # replaces an earlier mark when it is better.
    best = {}
    recorded = 0
    absent = 0
    for number, row in enumerate(rows, start=2):
        if not row["score"].strip():
            absent += 1
            continue
        recorded += 1
        subject = row["subject"]
        if subject not in weights:
            fail(
                "row " + str(number) + " (" + row["student"] + ", "
                + row["class"] + ", " + subject + ") is not in "
                + SUBJECTS_FILE + "."
            )
        key = (row["class"], row["student"])
        marks = best.setdefault(key, {})
        value = percent(row, number)
        if subject not in marks or value > marks[subject]:
            marks[subject] = value

    # A student's average is the weighted mean of the subjects they sat, with
    # the weights renormalised over those subjects so a missed subject neither
    # counts as zero nor adds to the divisor.
    averages = {}
    for key, marks in best.items():
        used = sum(weights[subject] for subject in marks)
        if used <= 0:
            fail(key[1] + " (" + key[0] + ") has no weighted subject to average.")
        averages[key] = sum(marks[subject] * weights[subject] for subject in marks) / used
    reported = {key: round(value, 1) for key, value in averages.items()}

    # Positions are decided inside the class, on the reported average, and
    # students who share a reported average share a position (1, 2, 2, 4).
    by_class = {}
    for key in reported:
        by_class.setdefault(key[0], []).append(key)

    places = {}
    for cls, students in by_class.items():
        students.sort(key=lambda key: (-reported[key], key[1]))
        place = 0
        previous = None
        for index, key in enumerate(students, start=1):
            if reported[key] != previous:
                place = index
                previous = reported[key]
            places[key] = place

    print("Term results: " + TERM)
    print("Marks: " + str(recorded) + " recorded, " + str(absent) + " absent")

    for cls in sorted(by_class):
        students = sorted(by_class[cls], key=lambda key: (places[key], key[1]))
        for key in students:
            verdict = "pass" if reported[key] >= PASS_MARK else "fail"
            print(
                key[1] + " (" + cls + "): "
                + "{:.1f}".format(reported[key]) + "%, position "
                + str(places[key]) + " of " + str(len(students)) + ", " + verdict
            )

    # A class average is the mean of its students' reported averages, so one
    # student is one student however many subjects they sat.
    for cls in sorted(by_class):
        students = by_class[cls]
        mean = sum(reported[key] for key in students) / len(students)
        print("Class average " + cls + ": " + "{:.1f}".format(mean) + "%")


if __name__ == "__main__":
    main()
