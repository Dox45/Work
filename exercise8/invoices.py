"""Invoice run for the tutoring fortnight.

Reads billing.csv and rates.csv and prints what each tutor is owed for the
sessions inside the invoicing period, plus VAT.
"""

import csv
from datetime import datetime

BILLING_FILE = "billing.csv"
RATES_FILE = "rates.csv"
PERIOD_START = "02/11/2026"
PERIOD_END = "15/11/2026"
VAT_PERCENT = 7.5
BREAK_MINUTES = 30
BREAK_FROM_MINUTES = 2 * 60  # a session of 2 hours or more includes the break


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def as_date(text):
    # Day/month/year, and written both with and without a leading zero.
    return datetime.strptime(text.strip(), "%d/%m/%Y")


def clock_minutes(row):
    start_h, start_m = row["start"].split(":")
    end_h, end_m = row["end"].split(":")
    minutes = int(end_h) * 60 + int(end_m) - int(start_h) * 60 - int(start_m)
    if minutes < 0:
        # The end is before the start, so the session crossed midnight and the
        # end time belongs to the next day. Add the day back on.
        minutes = minutes + 24 * 60
    return minutes


def paid_hours(row):
    minutes = clock_minutes(row)
    if minutes >= BREAK_FROM_MINUTES:
        minutes = minutes - BREAK_MINUTES
    return minutes / 60


def load_rates(path):
    return {row["tutor"]: float(row["rate"]) for row in load_rows(path)}


def main():
    rows = load_rows(BILLING_FILE)
    rates = load_rates(RATES_FILE)

    first_day = as_date(PERIOD_START)
    last_day = as_date(PERIOD_END)

    # Only sessions that happened inside the invoicing period get billed, and
    # both ends of the period count.
    billable = [
        row for row in rows
        if row["status"] == "completed"
        and first_day <= as_date(row["date"]) <= last_day
    ]

    print("Invoice period: " + PERIOD_START + " to " + PERIOD_END)
    print(
        "Sessions: " + str(len(rows)) + " logged, "
        + str(len(billable)) + " billable"
    )

    hours = {}
    missing = []
    for row in billable:
        tutor = row["tutor"]
        if tutor not in rates:
            # A tutor with no row in rates.csv is never billed at somebody
            # else's rate: we say so and leave them out of the invoice.
            if tutor not in missing:
                missing.append(tutor)
            continue
        hours[tutor] = hours.get(tutor, 0) + paid_hours(row)

    for tutor in missing:
        print("Missing rate: " + tutor)

    amounts = {tutor: hours[tutor] * rates[tutor] for tutor in hours}

    subtotal = 0.0
    for tutor in sorted(amounts, key=lambda name: (-amounts[name], name)):
        amount = amounts[tutor]
        subtotal = subtotal + amount
        print(
            tutor + ": " + "{:.1f}".format(hours[tutor]) + " h x "
            + "{:.2f}".format(rates[tutor]) + " = " + "{:.2f}".format(amount)
        )

    print("Subtotal: " + "{:.2f}".format(subtotal))
    vat = subtotal * VAT_PERCENT / 100
    print("VAT at " + str(VAT_PERCENT) + "%: " + "{:.2f}".format(vat))
    print("Total due: " + "{:.2f}".format(subtotal + vat))

    dates = [as_date(row["date"]) for row in billable]
    print("First session: " + min(dates).strftime("%d/%m/%Y"))
    print("Last session: " + max(dates).strftime("%d/%m/%Y"))


if __name__ == "__main__":
    main()
