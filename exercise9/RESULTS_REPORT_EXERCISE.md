# Exercise 9: the end-of-term report card

`results.py` reads two files and prints the end-of-term report for a junior
school: `marks.csv`, every mark recorded for the term, and `subjects.csv`, the
weight each subject carries.

The script runs without any error. It just prints the wrong report.

This is the last exercise, and it brings together what the earlier ones
practised: reading two files, matching rows to a table, turning marks into
percentages, weighting subjects, grouping students into classes, and ranking
them. The arithmetic is easier than exercise 7. The thinking is harder.

## How to run it

In this folder:

```
python3 results.py
```

Nothing to install. It only uses the standard library.

`test_results.py` is there if you want a check while you work. Run
`python3 test_results.py` and it prints PASS or FAIL for each rule below. It
fails on the script as it stands, which is the point. Try not to read the test
file as a set of answers; use it to confirm what you have already worked out.

## What it must print

Exactly this, no more and no less:

```
Term results: First term 2026/2027
Marks: 38 recorded, 3 absent
Adaeze (JSS2A): 83.4%, position 1 of 3, pass
Bola (JSS2A): 75.1%, position 2 of 3, pass
Chidi (JSS2A): 49.1%, position 3 of 3, fail
Fatima (JSS2B): 80.9%, position 1 of 4, pass
Dami (JSS2B): 66.1%, position 2 of 4, pass
Emeka (JSS2B): 66.1%, position 2 of 4, pass
Ngozi (JSS2B): 57.9%, position 4 of 4, pass
Halima (JSS2C): 76.2%, position 1 of 3, pass
Grace (JSS2C): 60.6%, position 2 of 3, pass
Ifeanyi (JSS2C): 44.1%, position 3 of 3, fail
Class average JSS2A: 69.2%
Class average JSS2B: 67.8%
Class average JSS2C: 60.3%
```

The rules behind that output:

1. A subject percentage is the mark divided by that subject's maximum, times
 100. The maxima are not all the same: Mathematics and English are out of
 100, Physics is out of 50, Biology out of 40. A 42 in Physics is 84%, not
 42%.
2. Each subject has a weight in `subjects.csv`. A student's term average is
 the weighted mean of the percentages of the subjects **they actually sat**:
 multiply each percentage by that subject's weight, add them up, and divide
 by the weights you used. Mathematics counts three times, English and Physics
 twice, Biology once.
3. A blank mark means the student did not sit that subject. It is left out of
 the average completely, and the weights are renormalised: a student who
 missed Biology is averaged over Mathematics, English and Physics only.
4. One student sat a resit, so their name and subject appear twice in
 `marks.csv` (Chidi's Mathematics, the last line of the file). The **better**
 of the two marks counts, once.
5. A student's average is printed to one decimal place, and the position is
 decided on that reported average. Two students with the same average to one
 decimal place share a position, and the number they share is then skipped:
 the ranking runs 1, 2, 2, 4. It is not 1, 2, 3, 4 and not 1, 2, 2, 3.
6. Positions are inside the class. Each line reads `position 2 of 4` for a
 class of four, never `position 2 of 10` for the whole year group.
7. `pass` if the average is 50.0 or more, otherwise `fail`. A student sitting
 exactly on 50.0 passes.
8. Students are printed class by class, classes in alphabetical order, and
 within a class by position, then by name.
9. `Marks:` shows the number of marks actually recorded, then the number of
 blank rows. Added together they must come to the number of rows in the file.
10. `Class average` is the mean of the students' reported averages in that
 class, to one decimal place, one line per class in alphabetical order.

## What it prints now

```
Term results: First term 2026/2027
Marks: 41 recorded, 3 absent
Fatima (JSS2B): 56.2%, position 1 of 10, pass
Bola (JSS2A): 55.2%, position 2 of 10, pass
Adaeze (JSS2A): 51.5%, position 3 of 10, pass
Dami (JSS2B): 48.5%, position 4 of 10, fail
Emeka (JSS2B): 48.2%, position 5 of 10, fail
Halima (JSS2C): 45.5%, position 6 of 10, fail
Ngozi (JSS2B): 42.5%, position 7 of 10, fail
Grace (JSS2C): 38.5%, position 8 of 10, fail
Chidi (JSS2A): 34.0%, position 9 of 10, fail
Ifeanyi (JSS2C): 32.8%, position 10 of 10, fail
Class average JSS2A: 46.9%
Class average JSS2B: 48.9%
Class average JSS2C: 38.9%
```

Every line after the title is wrong.

## Marking guide

Eight points, one per fault. None of them repeats a fault from exercises 5, 6,
7 or 8, though the last one is the same kind of slip as the header counts in
those reports: it counts the wrong rows.

1. **Every subject is marked as if it were out of 100.** `percent()` returns
 the score itself, because of the comment that says every subject is out of
 100. It is not: `max_score` is in the file and different for each subject.
 Physics is out of 50, so 42 becomes 42% instead of 84%, and Biology out of
 40, so 33 becomes 33% instead of 82.5%. The score has to be divided by that
 subject's maximum. This is the first fault to fix, because it changes every
 number in the report.

2. **A blank mark becomes a zero and is counted.** `float(row["score"] or 0)`
 turns the empty cell into 0, and the subject is stored anyway, so it is
 averaged in and counts towards the divisor. Adaeze missed Biology and reads
 51.5% instead of 83.4%. A blank has to be skipped, and the average taken over
 the subjects actually sat, with their weights added up separately. This is
 the fault that makes the biggest difference to the top of the class.

3. **A resit keeps the last mark instead of the better one.** `marks[key] =
 percent(row)` overwrites whatever was there, and the resit row is the last
 line of the file, so Chidi's 47 replaces his 54. The rule is that the better
 attempt counts, so the line has to keep the larger of the two, not the later
 one. Note that this is not a duplicate to be deleted: both rows are real, and
 the pair has to collapse to one mark.

4. **The weights are never used.** `subjects.csv` is opened, but only for its
 subject names; the weight column is never read. The average is a plain mean
 of four subjects, so Biology counts as much as Mathematics. With the weights
 applied, Fatima scores 96 in Mathematics, which counts three times, and 22 out
 of 40 in Biology, which counts once: a plain mean gives her 75.8%, the
 weighted mean gives 80.9%. The weighted mean is the sum of percentage times weight,
 divided by the sum of the weights used.

5. **Positions are ranked across the whole year group.** `ordered` holds every
 student in the school, so each line says `of 10` and Adaeze is third when she
 is first in her class. The ranking has to happen inside each class, which
 also fixes the `of N`: three in JSS2A, four in JSS2B, three in JSS2C.

6. **Students level on the same average get different positions.** The place
 comes from `enumerate(..., start=1)` over the sorted list, so Dami and Emeka,
 both on 66.1%, are given 2 and 3. Equal averages share a position, and the
 next student skips the number that was used twice. Watch the two ways this
 can go wrong with this data: numbering the sorted list gives Emeka third,
 and sharing the number but then carrying on counting gives Ngozi third. The
 right answer is 1, 2, 2, 4: Emeka second, Ngozi fourth.

7. **The class average is the mean of the marks, not of the students.** The
 class totals add up every subject percentage and divide by the number of
 marks. Once blanks are skipped that gives a student who sat four subjects
 more say than one who sat three, and it ignores the weights entirely. It
 should be the mean of the students' reported averages: 69.2, 67.8 and 60.3.

8. **`recorded` counts every row, blanks included.** There are 41 rows in
 `marks.csv` and 3 of them are blank, so `41 recorded, 3 absent` contradicts
 itself: three blank rows among 41 leaves 38 marks, not 41. The recorded count
 is the rows with a mark in them, 38.

Leave the class averages until last. Each one is built from every student in
that class, so it only comes right once the student lines do, and a class
average can look almost plausible while every line above it is wrong. While you
work, compare student lines, not class averages.

### Bonus, 2 points

- **Two students with the same name merge into one.** Add a line
 `Grace,JSS2A,Mathematics,70,100` to `marks.csv` and run the report. There is
 still only one Grace: her JSS2C marks and the new one become a single set,
 with Mathematics taking the 70 rather than the 60, and she is printed as
 `Grace (JSS2A): 64.9%, position 3 of 4` because JSS2A is the class last seen
 for her name. JSS2C drops to two students. Nothing checks whether two rows
 are the same person. A student needs an identity that is not just a name: a
 student number, or at least the class plus the name.
- **A mark above the maximum is accepted without complaint.** Change
 Ifeanyi's Biology from `15` to `55` out of 40 and run it. He becomes
 `56.6%, position 3 of 3, pass`, up from 44.1% and a fail, on a mark that
 cannot exist. Nothing checks the mark against the maximum. A report that
 quietly turns a fail into a pass because of a typing error is worse than one
 that stops and names the row.

Two things that look like traps and are not, both tested:

- A mark written `88.0` instead of `88` changes nothing. Converting the text
 to a decimal number is right either way; only blank cells need special care.
- A subject listed in `subjects.csv` that nobody takes changes nothing. It is
 simply never looked up. Only a subject that appears in `marks.csv` and is
 missing from `subjects.csv` is a problem, and that is not what this file
 does.

## A suggested order of work

Start with the maximum score, because every percentage depends on it and the
fix is one line. Then skip the blanks, which is also where the divisor starts
to matter. Then the weights, which is the only change that needs both files at
once. Check the ten student lines against the target before touching the
positions: if the averages are right, the ranking is a separate, smaller
problem. Do the class grouping and the tie rule together, since both live in
the same few lines. Finish with the class averages and the recorded count,
which are the two lines that describe the report rather than a student. Run
the script after each change and compare one line at a time.
