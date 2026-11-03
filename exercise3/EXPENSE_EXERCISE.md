# Exercise 3: the expense report

A small script that reads `expenses.csv` and prints a summary of October spending.
It runs without crashing, but every number it prints is wrong. Make it match the
target output below.

No API keys, no network, standard library only.

## Run it

```
python3 expense_report.py
```

It must be run from the folder that contains `expenses.csv`.

## What it should do

1. Read every row of `expenses.csv` (columns: `date,category,amount`).
2. Add up the amounts for each category. Amounts are whole naira.
3. Print a header line with the number of expense rows read.
4. Print one line per category: the name, the category total, and that total as a
   percentage of the grand total rounded to the nearest whole number.
5. Sort the category lines from the largest total to the smallest.
6. Print the categories at or above the budget flag of 1,500, in the same
   largest-first order. Print `none` if no category reaches it.
7. Print the grand total.
8. Skip a row that cannot be read, but say which one it was. A blank line is not
   an error and must not be reported.

Numbers: no thousands separators, no currency symbols.

## Target output

```
Expense report (8 rows)
Travel       2450   37%
Software     1899   29%
Equipment    1500   23%
Meals         750   11%
Over budget: Travel, Software, Equipment
Total: 6599
```

Column layout, for reference: category name left-aligned in 10 characters, amount
right-aligned in 6, percentage right-aligned in 4 followed by `%`.

## What it prints now

```
Expense report (7 rows)
Meals         300    0%
Travel        600    0%
Software      900    0%
Equipment    1500    0%
Over budget: none
Total: 3300
```

## Marking guide

Six defects, worth about 2 marks each. The order below is roughly easiest to
hardest; a good answer explains each one rather than only patching it.

1. `rows[:-1]` in `load_rows` throws away the last row of the file. It should be
   `rows` (or, better, loop over the file without loading it twice). Symptom: 7
   rows instead of 8.
2. `totals[category] = amount` overwrites the category instead of adding to it.
   It should be `totals[category] = totals.get(category, 0) + amount`. Symptom:
   Travel shows one expense, 600, instead of 2,450.
3. The sort has no `reverse=True`, so the smallest total comes first.
4. `value // total * 100` is whole-number division, so every percentage is 0.
   It should be `round(value / total * 100)`. Nothing warns you: no error, just
   wrong output.
5. `value > BUDGET_FLAG` misses a category sitting exactly on the flag, so
   Equipment at 1,500 is not listed. It should be `>=`.
6. `except Exception: pass` hides every problem with no message. It should catch
   only what it expects (`IndexError`, `ValueError`) and print the row it skipped.
   This is the one to fix first, because it is what hides the others.

Two extras worth a mark: the script crashes with a divide-by-zero on an empty
file, and nothing rejects a negative amount.

## Tests worth running after the fix

- The real `expenses.csv`: must match the target output exactly.
- A file with one category only: that category should be 100%.
- An empty file apart from the header: should not crash.
- A file with a blank line at the end: should not print a skip message.
- A row with `abc` as the amount: should be skipped with a clear message.
