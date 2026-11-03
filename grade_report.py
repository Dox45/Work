"""Print a class report from scores.csv.

The brief for this exercise is in GRADE_EXERCISE.md.
"""

SCORES_FILE = "scores.csv"


def grade_for(score):
    """Letter grade for a score out of 100, using the scale in the brief."""
    if score > 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"


def load_scores(path):
    """Read name, score pairs from the csv file."""
    with open(path, "r") as handle:
        lines = handle.readlines()

    rows = []
    for line in lines[2:]:
        parts = line.strip().split(",")
        try:
            rows.append((parts[0], int(parts[1])))
        except Exception:
            print("Skipping a row that could not be read.")
    return rows


def main():
    rows = load_scores(SCORES_FILE)

    total = 0
    count = 0
    report = []
    for name, score in rows:
        total += score
        count += 1
        report = ["{}: {} ({})".format(name, score, grade_for(score))]

    average = total // count

    for line in report:
        print(line)
    print("Class average: {}".format(average))


if __name__ == "__main__":
    main()
