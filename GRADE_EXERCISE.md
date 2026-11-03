# Exercise: fix the class report script

`grade_report.py` reads `scores.csv` and prints one line per student plus the class
average. It runs, but the output is wrong.

Run it from this folder:

```
python3 grade_report.py
```

It currently prints this:

```
Skipping a row that could not be read.
Femi: 39 (F)
Class average: 63
```

That is not what it should print. The script has five real defects. Fix them so the
output matches the target below exactly, character for character.

## Target output

```
Ada: 90 (A)
Bola: 88 (B)
Chidi: 75 (C)
Dara: 63 (D)
Emeka: 50 (E)
Femi: 39 (F)
Class average: 67.5
```

## The rules the script has to follow

1. `scores.csv` has a header row (`Name,Score`) and then one student per row. The
   header is not a student.
2. Every student in the file must get a line, in file order.
3. Letter grades: A is 90 and above, B is 80 to 89, C is 70 to 79, D is 60 to 69,
   E is 50 to 59, F is below 50. The boundaries are inclusive, so exactly 90 is an A
   and exactly 50 is an E.
4. The class average is the mean score, printed to one decimal place. So 67.5, not
   67, and not 68.
5. Blank lines are normal and must be ignored silently, no message. For a row that
   is genuinely broken (missing a score, or a score that is not a number), skip that
   student and print one clear message that names the line number. Do not let a bad
   row hide the reason it was bad, and do not let one bad row stop the run.
6. The script must also not crash on an empty class (header only, no students).
   Print the average line as `Class average: 0.0` in that case.

## Notes

- Standard library only. There is nothing to install.
- Keep the two functions (`grade_for`, `load_scores`) and `main()`; fix them in place.
- Do not change `scores.csv`. It is the test data, including its quirks.
- A good order of work: run it, read the traceback or the odd output, fix the smallest
  thing that gets you closer to the target, run it again. Compare against the target
  output every time.
