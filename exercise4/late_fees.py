"""Late returns report.

Reads loans.csv and prints how much each member owes in late fees, which members
have been flagged as chronic borrowers, and the total owed.

This script does not do what the brief says. Your job is to make it match
LATE_FEES_EXERCISE.md.
"""

import csv

FINE_PER_DAY = 50
FINE_CAP = 1500
CHRONIC_AT = 3


def load_rows(path):
    with open(path, newline="") as handle:
        reader = csv.reader(handle)
        return list(reader)


def summarise(rows):
    totals = {}
    counts = {}
    for row in rows[1:]:
        days_late = int(row[2])
        if days_late >= 0:
            fine = max(days_late * FINE_PER_DAY, FINE_CAP)
            totals[row[1]] = totals.get(row[1], 0) + fine
            counts[row[1]] = counts.get(row[1], 0) + 1
    return totals, counts


def report(path):
    rows = load_rows(path)
    totals, counts = summarise(rows)
    chronic = [name for name, n in counts.items() if n > CHRONIC_AT]

    print(f"Late returns ({len(totals)} overdue loans)")
    for name in sorted(totals):
        print(f"{name:<8} {totals[name]:>6} {counts[name]:>3}")
    print("Chronic borrowers: " + (", ".join(chronic) if chronic else "none"))
    print(f"Total fines: {sum(counts.values())}")


if __name__ == "__main__":
    report("loans.csv")
