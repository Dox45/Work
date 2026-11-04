# Exercise 7: the tutoring hours report

`session_hours.py` reads `sessions.csv`, a week of tutoring sessions from four
tutors, and prints how many hours each one actually taught.

The script runs without any error. It just prints the wrong numbers.

This one is harder than exercise 6. The times in the file are written as
`14:30`, so the script has to do real arithmetic with hours and minutes rather
than read a ready-made number.

## How to run it

In this folder:

```
python3 session_hours.py
```

Nothing to install. It only uses the standard library.

## What it must print

Exactly this, no more and no less:

```
Sessions logged: 14
Completed: 10 (71.4%)
Chidi: 3 sessions, 5.0 h, avg 1.7 h
Ada: 3 sessions, 4.8 h, avg 1.6 h
Dami: 2 sessions, 3.5 h, avg 1.8 h
Bola: 2 sessions, 2.8 h, avg 1.4 h
Longest session: S03 2.5 h
Total hours: 16.0 h
```

The rules behind that output:

1. Only sessions whose status is `completed` count. `cancelled` and `no-show`
   sessions are left out of every count, every total and every average.
2. `Sessions logged` is the number of session rows in the whole file, whatever
   their status.
3. `Completed` is the number of completed sessions, then in brackets that
   number as a percentage of all rows, to one decimal place, with a `%` sign.
4. There is one tutor line per tutor who taught at least one completed session,
   ordered by total hours, most hours first.
5. Each tutor line holds the number of that tutor's completed sessions, then
   their total hours to one decimal place, then their average hours per
   completed session to one decimal place.
6. `Longest session` is the completed session with the greatest length, named
   by its `session_id`, with its length in hours to one decimal place.
7. `Total hours` is every completed session's length added together, to one
   decimal place.

The `date` column is there because a real log has dates. Nothing in the report
uses it.

## What it prints now

```
Sessions logged: 13
Completed: 11 (275.0%)
Ada: 2 sessions, 3.0 h, avg 1.0 h
Bola: 3 sessions, 2.0 h, avg 0.5 h
Chidi: 3 sessions, 4.0 h, avg 1.3 h
Dami: 3 sessions, 4.0 h, avg 1.3 h
Longest session: S12 1.0 h
Total hours: 13.0 h
```

Every line is wrong, and the tutor order is wrong too.

## Marking guide

Seven points, one per fault.

1. **The first session is thrown away.** `rows = rows[1:]` was meant to skip the
   column headings, but `csv.DictReader` has already used the first line for
   that, so this deletes real data: `S01`, Ada's 1.5 hour session. That is why
   the header says 13 when the file holds fourteen sessions. The slice should
   not be there at all.
2. **The minutes are ignored.** `session_hours` takes `row["start"][:2]` and
   `row["end"][:2]`, which is only the hour part, then subtracts one from the
   other. So 14:00 to 16:30 counts as 2 hours instead of 2.5, and 16:00 to
   17:15 counts as 1 instead of 1.25. Every session with minutes needs those
   minutes turned into part of an hour: multiply the hours by 60, add the
   minutes, subtract, then divide by 60.
3. **Cancelled sessions are counted as completed.** The loop only skips
   `no-show`, so the two `cancelled` rows, `S05` and `S11`, fall through and
   get counted. The test needs to keep `status == "completed"` only, rather
   than throw away one bad status and accept everything else.
4. **The percentage is divided by the wrong number.** It divides the completed
   count by the number of tutors, four, which gives 275%. A percentage cannot
   be over 100 here; it should be divided by the number of session rows.
5. **The tutors are in alphabetical order.** `sorted(per_tutor)` sorts names
   alphabetically. The rule is most hours first, so it needs sorting by the
   hours value, largest first.
6. **The average is divided by the wrong count.** For each tutor the script
   counts every row carrying that name, including cancelled and no-show ones,
   and divides the completed hours by that bigger number. Ada has three rows
   left after the slice, one of them a no-show, so her 3.0 hours are divided by
   three and the average comes out as 1.0 instead of 1.6. The divisor has to be
   the number of completed sessions.
7. **The longest session is picked by finish time.** It compares `end` values
   as text and keeps the one that finishes latest. `S12` ends at 17:30, the
   latest in the file, but it only runs 1.5 hours. `S03`, 14:00 to 16:30, runs
   2.5 hours and is the real answer. The comparison has to be on the length of
   the session, not the clock time it ended.

### Bonus, 2 points

- **A time written without a leading zero stops the script dead.** Change
  `S09`'s start from `09:00` to `9:00` and run it: you get a `ValueError`
  saying `invalid literal for int() with base 10: '9:'`, with nothing printed
  before it. `[:2]` grabs `9:` rather than `09`. Splitting on the colon, the
  way the reference arithmetic needs anyway, fixes this too.
- **A trailing space in a name splits a tutor in two.** Change `S07`'s tutor
  from `Dami` to `Dami ` (one space after the name) and the report prints two
  Dami lines, `Dami` and `Dami `, each with part of the sessions. The
  percentage also drops to 220.0% because a fifth "tutor" now exists. Nothing
  trims whitespace from the names.

## A suggested order of work

Start with the two counting faults that are easy to see: remove the slice so
all fourteen sessions load, and fix the status filter so only completed
sessions get through. Then fix the duration arithmetic, because that one
changes every hour figure. After that sort the tutors by hours, correct the two
wrong divisors (the percentage and each average), and last of all change the
longest-session comparison to work on lengths instead of end times. Run the
script after each change and compare against the target above, one line at a
time.
