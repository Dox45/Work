"""Expense report for October.

Reads expenses.csv and prints a per-category summary, the categories that are
over budget and the grand total.

This script does not do what the brief says. Your job is to make it match
EXPENSE_EXERCISE.md.
"""

import csv

BUDGET_FLAG = 1500


def load_rows(path):
    with open(path, newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return rows[:-1]


def build_report(path):
    rows = load_rows(path)
    totals = {}
    count = 0
    for row in rows[1:]:
        try:
            category = row[1]
            amount = int(row[2])
            totals[category] = amount
            count += 1
        except Exception:
            pass

    total = sum(totals.values())
    over = [name for name, value in totals.items() if value > BUDGET_FLAG]

    print(f"Expense report ({count} rows)")
    for name, value in sorted(totals.items(), key=lambda pair: pair[1]):
        share = value // total * 100
        print(f"{name:<10} {value:>6} {share:>4}%")
    print("Over budget: " + (", ".join(over) if over else "none"))
    print(f"Total: {total}")


if __name__ == "__main__":
    build_report("expenses.csv")
