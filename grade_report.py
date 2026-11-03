"""Print a class report from scores.csv.

The brief for this exercise is in GRADE_EXERCISE.md.
"""

SCORES_FILE = "scores.csv"


def grade_for(score):
    """Letter grade for a score out of 100, using the scale in the brief."""
    if score >= 90:
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
    for number, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        parts = line.strip().split(",")
        try:
            name = parts[0].strip()
            score = int(parts[1])
        except (IndexError, ValueError):
            print("Skipping line {}: expected a name and a score.".format(number))
            continue
        rows.append((name, score))
    return rows


def main():
    rows = load_scores(SCORES_FILE)

    total = 0
    count = 0
    report = []
    for name, score in rows:
        total += score
        count += 1
        report.append("{}: {} ({})".format(name, score, grade_for(score)))

    average = total / count if count else 0.0

    for line in report:
        print(line)
    print("Class average: {:.1f}".format(average))


if __name__ == "__main__":
    main()
