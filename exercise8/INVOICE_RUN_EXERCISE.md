# Exercise 8: the invoice run

`invoices.py` reads two files and prints the invoice for a tutoring fortnight:
`billing.csv`, the session log, and `rates.csv`, the hourly rate for each tutor.

The script runs without any error. It just prints the wrong invoice.

This is the next step after exercise 7. The hour-and-minute arithmetic is still
needed, but now two more things sit on top of it: **dates** decide which
sessions get billed at all, and **money** has to be worked out per tutor, added
up, taxed and rounded.

## How to run it

In this folder:

```
python3 invoices.py
```

Nothing to install. It only uses the standard library.

## What it must print

Exactly this, no more and no less:

```
Invoice period: 02/11/2026 to 15/11/2026
Sessions: 18 logged, 15 billable
Chidi: 7.0 h x 5200.00 = 36400.00
Dami: 6.0 h x 5600.00 = 33600.00
Ada: 6.0 h x 4500.00 = 27000.00
Bola: 3.5 h x 4200.00 = 14700.00
Subtotal: 111700.00
VAT at 7.5%: 8377.50
Total due: 120077.50
First session: 02/11/2026
Last session: 15/11/2026
```

The rules behind that output:

1. The invoicing period is `02/11/2026` to `15/11/2026`, and **both ends count**.
   Dates in the file are day/month/year.
2. Only sessions that are `completed` **and** inside the period are billable.
   `cancelled` and `no-show` rows never bill, and neither does a completed
   session dated outside the period.
3. Any session of **2 hours or more includes a 30-minute unpaid break**, so its
   paid length is half an hour shorter than its clock length. A session of
   exactly 2 hours does get the break. Anything under 2 hours gets no break.
4. Each tutor is paid their own hourly rate, taken from `rates.csv`. Rates are
   in naira per hour.
5. `Sessions:` shows every row in `billing.csv`, then how many of them are
   billable.
6. There is one tutor line per tutor with at least one billable session,
   **biggest amount owed first**, in this shape:
   `Name: 7.0 h x 5200.00 = 36400.00`. Hours to one decimal place, rate and
   amount to two.
7. `Subtotal` is the sum of the tutor amounts.
8. `VAT at 7.5%` is 7.5 per cent of the subtotal, to two decimal places.
9. `Total due` is the subtotal plus the VAT, to two decimal places.
10. `First session` and `Last session` are the earliest and latest dates among
    the **billable** sessions, printed as `DD/MM/YYYY`.

## What it prints now

```
Invoice period: 02/11/2026 to 15/11/2026
Sessions: 18 logged, 16 billable
Chidi: 8.0 h x 4500.00 = 36000.00
Dami: 6.0 h x 4500.00 = 27000.00
Ada: 4.0 h x 4500.00 = 18000.00
Bola: 1.0 h x 4500.00 = 4500.00
Subtotal: 85500.00
VAT at 7.5%: 641250.00
Total due: 85500.00
First session: 03/11/2026
Last session: 9/11/2026
```

Every line except the period is wrong.

## Marking guide

Eight points, one per fault. None of them is the same fault as in exercises 5,
6 or 7.

1. **Monday 2 November is missing.** The filter is
   `first_day < as_date(row["date"]) <= last_day`, with a strict `<` at the
   front, so every session dated exactly `02/11/2026` is dropped: `S01` for Ada
   and `S02` for Bola. Both ends of the period are meant to count, so it should
   be `<=` on both sides. That is why `First session` says `03/11/2026`.
2. **`Last session` is picked by comparing date text.** The line takes
   `max(row["date"] ...)` from the raw strings. Most dates are written
   `DD/MM/YYYY` with two digits, which does sort correctly as text, but `S12` is
   written `9/11/2026` with no leading zero, and `"9/11/2026"` is bigger than
   `"15/11/2026"` as text because `9` beats `1`. So it prints `9/11/2026`
   instead of `15/11/2026`. Both date lines need real dates, not strings.
3. **The unpaid break is never taken off.** `session_hours` returns the plain
   clock length and nothing subtracts the 30 minutes for long sessions. Every
   session of 2 hours or more is therefore half an hour too long, which pushes
   every tutor's hours and money up.
4. **There is one flat rate for everybody.** `RATE = 4500` is used for every
   tutor and `rates.csv` is never opened at all. So every line shows
   `4500.00`, Chidi is underpaid at that rate and Bola is overpaid. The rate has
   to be looked up per tutor from the rates file.
5. **Each session's length is cut to whole hours before it is paid.**
   `int(session_hours(row))` throws away the fraction of every session.
   Bola's 45-minute session `S06` becomes 0 hours and disappears entirely, and
   her 1.75 hour session becomes 1. That is why Bola shows 1.0 h instead of
   3.5 h. The fraction of an hour is real money and has to be kept.
6. **VAT is multiplied by 7.5 instead of 0.075.** `subtotal * 7.5` gives
   `641250.00` where 7.5 per cent of the subtotal is `8377.50`. A percentage has
   to be divided by 100 before it multiplies money.
7. **`Total due` leaves the VAT out.** The VAT is worked out and printed, then
   `Total due` prints the subtotal by itself, so the invoice charges nothing for
   VAT. It has to be subtotal plus VAT.
8. **The billable count ignores the period.** The `Sessions:` line counts every
   `completed` row in the file, sixteen of them, including `S18` dated
   `16/11/2026`, which is outside the period and is not billed. The number
   printed has to describe the same sessions the money describes, so it is
   fifteen.

Note how 1 and 8 hide each other: the count is too high because it ignores the
period, and the money is too low because the filter drops a day. Fixing one
without the other still leaves the two halves of the report disagreeing.

### Bonus, 2 points

- **A session that runs past midnight goes negative.** Change `S05` to start at
  `23:00` and end at `00:00` and run it: Ada's line becomes
  `Ada: -20.0 h x 4500.00 = -90000.00` and the subtotal goes negative. The
  arithmetic is `00:00` minus `23:00`, which is minus 23 hours, and `int()` cuts
  it to -23. A session that ends before it starts has crossed midnight, so the
  fix is to add 24 hours to the end time when that happens. Done that way the
  session is 1.0 h, Ada reads 5.5 h and 24750.00, and the invoice stays
  positive.
- **A tutor with no rate row stops the script once the rates are wired in.**
  Delete the `Dami` line from `rates.csv`. As the script stands nothing happens,
  because it never opens the rates file, but as soon as you look the rate up per
  tutor you get `KeyError: 'Dami'` and no invoice at all. Decide what should
  happen and say so in a comment: skipping that tutor with a
  `Missing rate: Dami` line, or stopping before printing with a clear message.
  Either is fine, silently billing them at somebody else's rate is not.

Two things that look like traps and are not, both tested:

- A time written `9:00` instead of `09:00` runs fine and changes nothing,
  because the file is read by splitting on the colon rather than slicing
  characters. Only the date `9/11/2026` causes trouble, and that is fault 2.
- A session of exactly 2 hours is in the file three times (`S07`, `S09`,
  `S11`). It does get the 30-minute break, so each one pays 1.5 hours, not 2.
  Read rule 3 again before you write that condition.

## A suggested order of work

Start with the rate lookup, because it is the one that makes every line show
the same rate and you can see it at a glance. Then the break rule and the
`int()` truncation, which are both inside the hours calculation and change every
figure. Then the two date faults, so the period and the first and last session
line up. Finish with the two money lines (VAT and the total) and the billable
count, which is a one-line change but only makes sense once the filter is right.
Run the script after each change and compare against the target above, one line
at a time.
