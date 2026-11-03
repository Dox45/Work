# Exercise 6: the parcel delivery report

`parcel_report.py` reads `parcels.csv`, which holds twelve parcels for one
delivery week, and prints a summary of what was delivered.

The script runs without any error. It just prints the wrong numbers.

## How to run it

In this folder:

```
python3 parcel_report.py
```

Nothing to install. It only uses the standard library.

## What it must print

Exactly this, no more and no less:

```
Parcels delivered: 9 of 12
Zone A: 3 delivered, 23.9 kg
Zone B: 4 delivered, 12.4 kg
Zone C: 2 delivered, 4.5 kg
Heaviest: P006 12.0 kg
Average weight: 4.5 kg
Success rate: 75.0%
Total weight: 40.8 kg
```

The rules behind that output:

1. Only parcels whose status is `delivered` count. `returned` and `failed`
   parcels are left out of every weight, count and average.
2. `Parcels delivered` is followed by the number of parcels in the whole file,
   delivered or not.
3. One `Zone` line per zone that has delivered parcels, in alphabetical order.
   The number after the zone letter is how many of that zone's parcels were
   delivered, then a comma, then their combined weight to one decimal place.
4. `Heaviest` names the single heaviest delivered parcel by its `parcel_id` and
   its weight to one decimal place.
5. `Average weight` is the total delivered weight divided by the number of
   delivered parcels, to one decimal place.
6. `Success rate` is delivered parcels divided by all parcels in the file,
   written as a percentage with one decimal place and a `%` sign.
7. `Total weight` is every delivered parcel added together, to one decimal
   place.

## What it prints now

```
Parcels delivered: 10 of 11
Zone A: 5 delivered, 24.0 kg
Zone B: 3 delivered, 5.0 kg
Zone C: 3 delivered, 4.0 kg
Heaviest: P003 9.4 kg
Average weight: 11.0 kg
Success rate: 0.9%
Total weight: 33.0 kg
```

Every line is wrong.

## Marking guide

Ten points, one per fault, plus the two bonuses.

1. **The last parcel is thrown away.** `rows = rows[:-1]` was meant to drop a
   blank line at the end of the file, but `csv.DictReader` already skips empty
   lines, so this deletes `P012` instead. That is why the header says "of 11"
   when the file holds twelve parcels, and why Zone B is one parcel short.
2. **Failed deliveries are counted as delivered.** The loop only skips
   `returned`. `failed` parcels fall through and get added to the weights and
   the delivered count. The test should be `status == "delivered"`, not
   "anything except returned".
3. **Weights are cut down to whole kilos.** `int(float(row["weight_kg"]))`
   reads 2.5 kg as 2 kg, so every total is too small. The weight needs to stay a
   decimal number.
4. **The per-zone counts include parcels that never arrived.** `zone_count` is
   increased before the `continue`, so returned and failed parcels are counted
   as delivered in the table. Zone A shows 5 when only 3 of its parcels were
   delivered.
5. **The heaviest parcel is picked by comparing text.** `row["weight_kg"] >
   heaviest_weight` compares strings rather than numbers, and `"9.4"` beats
   `"12.0"` because `"9"` sorts after `"1"`. That is why P003 is named instead
   of P006.
6. **The average is divided by the wrong number.** It divides the total weight
   by the number of zones, three, instead of the number of delivered parcels,
   nine.
7. **The success rate is printed as a fraction.** Ten delivered out of eleven
   rows is 0.909, and the script prints `0.9%`. It needs multiplying by 100
   before printing.

### Bonus, 2 points

- **A parcel with no weight stops the script dead.** Blank the weight on any
  row that is not the last line and run it: you get a `ValueError` saying
  `could not convert string to float: ''`, with no friendly message and nothing
  printed before it. A real report should report the bad row and carry on.
- **A parcel listed twice is counted twice.** Add `P004,C,1.5,delivered` as a
  second row and Zone C goes from 3 to 4 delivered and the total weight rises by
  1.5 kg. Nothing checks whether a `parcel_id` has already been seen.

## A suggested order of work

Start with the slice, because it changes every number in the report and it is
one line. Then fix the filter so only delivered parcels get through, then the
weight conversion, then the counts, then the heaviest parcel, the average and
the percentage. Run the script after each change and compare against the target
above, one line at a time.
