# Exercise 4: the late fees report

A small script that reads `loans.csv` and prints what each member owes in late
fees, who has been flagged as a chronic borrower, and the total owed.

It runs without crashing and prints a tidy table. Almost every line is wrong.
Make it match the target output below.

No API keys, no network, standard library only.

## Run it

```
python3 late_fees.py
```

It must be run from the folder that contains `loans.csv`.

## The rules

- A loan is **overdue** only if `days_late` is greater than zero. A loan returned
  on time is not overdue and carries no fine.
- The fine is **50 naira per day late**, capped at **1,500 per loan**. The cap is
  per loan, not per member, so a member with several overdue loans can owe more
  than 1,500 in total.
- A member is a **chronic borrower** if they have **3 or more** overdue loans.
- Members are listed from the largest total owed to the smallest.
- Chronic borrowers are listed alphabetically, separated by a comma and a space,
  or `none` if there are none.

## What it should do

1. Read every row of `loans.csv` (columns: `member,book,days_late`).
2. Work out the fine for each overdue loan, applying the daily rate and the cap.
3. Add the fines up **per member**.
4. Count each member's overdue loans.
5. Print a header line with the number of overdue loans across the whole file.
6. Print one line per member: name, total owed, number of overdue loans.
7. Print the chronic borrowers.
8. Print the grand total of all fines.

Numbers: no thousands separators, no currency symbols.

## Target output

```
Late returns (9 overdue loans)
Bola       2100   2
Dami       1850   2
Ada        1800   3
Chidi       700   2
Chronic borrowers: Ada
Total fines: 6450
```

Column layout, for reference: member name left-aligned in 8 characters, total
right-aligned in 6, loan count right-aligned in 3.

## What it prints now

```
Late returns (8 overdue loans)
Arrow      1500   1
Concubine   1500   1
Country    1500   1
Famished   2000   1
No Longer   2250   1
Ogbon      1500   1
Purple     4550   3
Things Fall   1500   1
Chronic borrowers: none
Total fines: 10
```

## Marking guide

Seven defects, worth about 2 marks each. A good answer explains each one rather
than only patching it, and says which symptom pointed at it.

1. `fine = max(days_late * FINE_PER_DAY, FINE_CAP)` has the cap the wrong way
   round. `max` means every loan is charged at least 1,500, so a four-day loan
   costs the same as a forty-day one. It should be `min`. Symptom: nobody's total
   is below 1,500.
2. `if days_late >= 0` treats a loan returned on time as overdue. Chidi's
   `Arrow` row has 0 days late and still gets charged. It should be `> 0`.
   Symptom: more overdue loans than there are late returns.
3. `totals[row[1]]` uses the book title as the key when it should use
   `row[0]`, the member. Symptom: one row per book instead of per person, and
   three separate `Purple` loans collapse into a single line of 4,550 with a
   count of 3. This is the one that makes every other number meaningless, so it
   is reasonable to fix it first.
4. `sorted(totals)` sorts the member names alphabetically. It needs to sort by
   the amount owed, largest first: `sorted(totals, key=lambda name: totals[name],
   reverse=True)`. Symptom: Arrow, Concubine, Country, in the order the alphabet
   happens to give rather than the biggest debt at the top.
5. `n > CHRONIC_AT` misses a member sitting exactly on 3, so Ada is not flagged.
   It should be `>=`. The brief says "3 or more".
6. The header prints `len(totals)`, which is the number of books in the table.
   It should print the number of overdue loans, `sum(counts.values())`. Symptom:
   8 instead of 9.
7. The total line prints `sum(counts.values())`, which is a count of loans, not
   money. It should sum the fines. Symptom: `Total fines: 10` instead of 6,450.

Two extras worth a mark each: a blank line at the end of the file crashes it with
an `IndexError`, and a negative `days_late` is silently ignored instead of
reported as bad data.

## Tests worth running after the fix

- The real `loans.csv`: must match the target output exactly.
- One member with a single loan of 40 days late: owes 1,500, not 2,000.
- One member with two 40-day loans: owes 3,000, because the cap is per loan.
- A file where nobody is late: header says 0, `Chronic borrowers: none`,
  `Total fines: 0`, and it does not crash.
- A blank line at the end of the file: no crash, no phantom row.
- A row with `abc` in the `days_late` column: skipped with a clear message.
