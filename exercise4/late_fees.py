"""Late returns report.

Reads loans.csv and prints how much each member owes in late fees, which members
have been flagged as chronic borrowers, and the total owed.

The output matches the target in LATE_FEES_EXERCISE.md.
"""

import csv

FINE_PER_DAY = 50
FINE_CAP = 1500
CHRONIC_AT = 3


def load_rows(path):
    """Every row of the file after the header, blank lines included.

    Blank lines are not errors, so they are left in for the caller to ignore
    silently; keeping them means the reported line numbers stay true to the file.
    """
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    return rows[1:]


def parse_days_late(text):
    """The days late as a whole number, or ValueError if it is not one."""
    days = int(text.strip())
    if days < 0:
        raise ValueError("negative days_late {}".format(days))
    return days


def summarise(rows):
    """Return (fines by member, overdue loan count by member).

    A row that cannot be read is reported by line number and skipped. Only the
    problems we expect - a missing field or a days_late that is not a whole
    number - are caught, so a real bug still shows up instead of being
    swallowed.
    """
    totals = {}
    counts = {}
    # Line 1 is the header, so the first data row is line 2.
    for line_number, row in enumerate(rows, start=2):
        if not any(field.strip() for field in row):
            continue
        try:
            member = row[0].strip()
            if not member:
                raise ValueError("missing member")
            days_late = parse_days_late(row[2])
        except (IndexError, ValueError) as problem:
            print("Skipped line {}: {} ({})".format(line_number, problem, ",".join(row)))
            continue
        # A loan returned on time is not overdue and carries no fine.
        if days_late <= 0:
            continue
        # The cap is per loan, so several overdue loans can add up past it.
        fine = min(days_late * FINE_PER_DAY, FINE_CAP)
        totals[member] = totals.get(member, 0) + fine
        counts[member] = counts.get(member, 0) + 1
    return totals, counts


def report(path):
    totals, counts = summarise(load_rows(path))
    chronic = sorted(name for name, n in counts.items() if n >= CHRONIC_AT)

    print("Late returns ({} overdue loans)".format(sum(counts.values())))
    for name in sorted(totals, key=lambda member: (-totals[member], member)):
        print("{:<8} {:>6} {:>3}".format(name, totals[name], counts[name]))
    print("Chronic borrowers: " + (", ".join(chronic) if chronic else "none"))
    print("Total fines: {}".format(sum(totals.values())))


if __name__ == "__main__":
    report("loans.csv")
