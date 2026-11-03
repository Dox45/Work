"""Expense report for October.

Reads expenses.csv and prints a per-category summary, the categories at or over
the budget flag and the grand total.

The output matches the target in EXPENSE_EXERCISE.md.
"""

import csv

BUDGET_FLAG = 1500


def load_rows(path):
    """Every row of the file after the header, blank lines included.

    Blank lines are not errors, so they are left in for the caller to ignore
    silently; keeping them means the reported line numbers stay true to the file.
    """
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    return rows[1:]


def parse_amount(text):
    """The amount as a whole number of naira, or ValueError if it is not one."""
    amount = int(text.strip())
    if amount < 0:
        raise ValueError("negative amount {}".format(amount))
    return amount


def read_expenses(path):
    """Return (totals by category, number of rows read).

    A row that cannot be read is reported by line number and skipped. Only the
    problems we expect - a missing field or an amount that is not a whole number -
    are caught, so a real bug still shows up instead of being swallowed.
    """
    totals = {}
    count = 0
    # Line 1 is the header, so the first data row is line 2.
    for line_number, row in enumerate(load_rows(path), start=2):
        if not any(field.strip() for field in row):
            continue
        try:
            category = row[1].strip()
            if not category:
                raise ValueError("missing category")
            amount = parse_amount(row[2])
        except (IndexError, ValueError) as problem:
            print("Skipped line {}: {} ({})".format(line_number, problem, ",".join(row)))
            continue
        totals[category] = totals.get(category, 0) + amount
        count += 1
    return totals, count


def build_report(path):
    totals, count = read_expenses(path)
    total = sum(totals.values())

    # Largest total first; the name breaks ties so the order is never random.
    ordered = sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))
    over = [name for name, value in ordered if value >= BUDGET_FLAG]

    print("Expense report ({} rows)".format(count))
    for name, value in ordered:
        share = round(value / total * 100) if total else 0
        print("{:<10} {:>6} {:>4}%".format(name, value, share))
    print("Over budget: " + (", ".join(over) if over else "none"))
    print("Total: {}".format(total))


if __name__ == "__main__":
    build_report("expenses.csv")
