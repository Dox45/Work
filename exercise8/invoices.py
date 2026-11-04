"""Invoice run for the tutoring fortnight.

Reads billing.csv and rates.csv and prints what each tutor is owed for the
sessions inside the invoicing period, plus VAT.

THIS VERSION IS BROKEN ON PURPOSE. See INVOICE_RUN_EXERCISE.md for what it is
supposed to print.
"""

import csv
from datetime import datetime

BILLING_FILE = "billing.csv"
WEEK_START = "02/11/2026"
WEEK_END = "15/11/2026"
RATE = 4500
VAT_PERCENT = 7.5


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def as_date(text):
    return datetime.strptime(text, "%d/%m/%Y")


def session_hours(row):
    start_h, start_m = row["start"].split(":")
    end_h, end_m = row["end"].split(":")
    minutes = int(end_h) * 60 + int(end_m) - int(start_h) * 60 - int(start_m)
    return minutes / 60


def main():
    rows = load_rows(BILLING_FILE)

    first_day = as_date(WEEK_START)
    last_day = as_date(WEEK_END)

    # Only sessions that happened inside the invoicing period get billed.
    billable = [
        row for row in rows
        if row["status"] == "completed"
        and first_day < as_date(row["date"]) <= last_day
    ]

    completed = [row for row in rows if row["status"] == "completed"]

    print("Invoice period: " + WEEK_START + " to " + WEEK_END)
    print(
        "Sessions: " + str(len(rows)) + " logged, "
        + str(len(completed)) + " billable"
    )

    hours = {}
    for row in billable:
        tutor = row["tutor"]
        hours[tutor] = hours.get(tutor, 0) + int(session_hours(row))

    subtotal = 0
    for tutor in sorted(hours, key=lambda name: -hours[name]):
        amount = hours[tutor] * RATE
        subtotal = subtotal + amount
        print(
            tutor + ": " + "{:.1f}".format(hours[tutor]) + " h x "
            + "{:.2f}".format(RATE) + " = " + "{:.2f}".format(amount)
        )

    print("Subtotal: " + "{:.2f}".format(subtotal))
    vat = subtotal * VAT_PERCENT
    print("VAT at " + str(VAT_PERCENT) + "%: " + "{:.2f}".format(vat))
    print("Total due: " + "{:.2f}".format(subtotal))

    print("First session: " + min(row["date"] for row in billable))
    print("Last session: " + max(row["date"] for row in billable))


if __name__ == "__main__":
    main()
