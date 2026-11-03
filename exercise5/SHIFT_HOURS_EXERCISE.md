# Exercise 5: the volunteer hours report

`shift_hours.py` reads `shifts.csv`, which holds nine October shifts for four
volunteers, and prints a summary of hours worked.

The script runs without any error. It just prints the wrong numbers.

## How to run it

In this folder:

```
python3 shift_hours.py
```

Nothing to install. It only uses the standard library.

## What it must print

Exactly this, no more and no less:

```
Shifts logged: 9
Dami     14.0
Ada      11.5
Bola      9.0
Chidi     7.0
Long shifts: Chidi
Total hours: 41.5
```

The rules behind that output:

1. A shift's length is the end time minus the start time, in hours. `09:00` to
   `15:30` is 6.5 hours.
2. Each volunteer's figure is the sum of all of their shifts.
3. The table is ordered by hours, largest first. Names are padded to eight
   characters, then a space, then the hours to one decimal place.
4. `Shifts logged` is the number of rows in the CSV, not the number of people.
5. `Long shifts` lists anyone with a single shift of 7 hours or more, in
   alphabetical order, separated by a comma and a space. If nobody qualifies it
   prints `none`.
6. `Total hours` is every shift added together, to one decimal place.

## What it prints now

```
Shifts logged: 4
Ada      1.5
Bola     1.8
Dami     2.1
Chidi    4.2
Long shifts: none
Total hours: 1.5
```

Every single line is wrong.

## Marking guide

Ten points, one per fault, plus the two bonuses.

1. **Hours are divided by 100, not 60.** `shift_hours` works out the minutes
   correctly and then divides by 100, so 390 minutes becomes 3.9 hours instead
   of 6.5. This is why every number in the table is too small.
2. **Each volunteer's total is overwritten, not added to.** `totals[name] =
   hours` keeps only that person's last shift. It should be `totals[name] =
   totals.get(name, 0) + hours`. This is why Dami shows 2.1 instead of 14.0.
3. **The table is sorted smallest first.** The sort key needs the hours
   reversed, largest first.
4. **The long shift test is `>` instead of `>=`.** Chidi worked exactly 7.0
   hours. With `>` against a threshold of 7, he does not count. The rule is 7 or
   more.
5. **The header counts people instead of shifts.** `len(totals)` gives 4. It
   should count the rows processed, which is 9.
6. **The running total is reset inside the loop.** `total = 0.0` on every pass
   throws away everything added before it, so the total ends up as the last row
   only.
7. **The catch-all `except Exception: pass` hides failures.** One badly formed
   row disappears from the report with no message and no error. Fixing this
   first makes the other faults much easier to see.

### Bonus, 2 points

- **A blank line at the end of the CSV crashes it.** The unpacking
  `name, date, start, end = row` runs outside the `try`, so an empty row stops
  the script with a `ValueError` instead of being skipped or reported clearly.
  Try it: add an empty line to `shifts.csv` and run it again.
- **A shift that ends before it starts is accepted.** Change a row to
  `Ada,2026-10-20,15:00,11:00` and the script reports minus 2.4 hours without
  complaint. A real fix should reject or flag it.

## A suggested order of work

Get rid of the silent handler first so that failures are visible, then fix the
maths in `shift_hours`, then the totals, then the three printing faults.
