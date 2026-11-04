"""Checks for the report card (exercise 9).

Run from this folder: python3 test_results.py

Every check runs the real script on a scratch copy of marks.csv and
subjects.csv, so a check only passes if the printed report is right, not if a
helper function happens to be.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "results.py")
MARKS = os.path.join(HERE, "marks.csv")
SUBJECTS = os.path.join(HERE, "subjects.csv")

TARGET = """\
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
"""


def read(path):
    with open(path) as handle:
        return handle.read()


def run_with(marks_text, subjects_text):
    """Run the script in a scratch folder holding the given two files."""
    work = tempfile.mkdtemp()
    try:
        shutil.copy(SCRIPT, os.path.join(work, "results.py"))
        with open(os.path.join(work, "marks.csv"), "w") as handle:
            handle.write(marks_text)
        with open(os.path.join(work, "subjects.csv"), "w") as handle:
            handle.write(subjects_text)
        result = subprocess.run(
            [sys.executable, "results.py"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr
    finally:
        shutil.rmtree(work)


marks = []


def check(name, passed, detail=""):
    marks.append((name, passed, detail))


def main():
    base = read(MARKS)
    subjects = read(SUBJECTS)

    # 1. The real files must print the target block exactly.
    code, out, err = run_with(base, subjects)
    check("full report matches the brief exactly", out == TARGET,
          repr(out) if out != TARGET else "")
    check("the script still exits cleanly", code == 0 and not err.strip(),
          err.strip()[:200])

    # 2. The header describes the file.
    check("38 marks recorded and 3 absent", "Marks: 38 recorded, 3 absent" in out)

    # 3. Each subject is marked against its own maximum.
    check("Adaeze is 83.4%, not 51.5% (Physics is out of 50, not 100)",
          "Adaeze (JSS2A): 83.4%" in out)
    check("Bola keeps her Biology mark out of 40 (75.1%)",
          "Bola (JSS2A): 75.1%" in out)

    # 4. An absent subject is left out, not counted as zero.
    check("Adaeze's missing Biology does not drag her down",
          "Adaeze (JSS2A): 83.4%, position 1 of 3, pass" in out)
    check("Halima averages the three subjects she sat (76.2%)",
          "Halima (JSS2C): 76.2%" in out)

    # 5. The subject weights decide the average.
    check("the weight column is used, not a plain mean of four subjects",
          "Fatima (JSS2B): 80.9%" in out)

    # 6. A resit counts once, at the better mark.
    check("Chidi's resit does not replace his better mark (49.1%)",
          "Chidi (JSS2A): 49.1%, position 3 of 3, fail" in out)

    # 7. Positions are inside the class.
    check("Adaeze is 1 of 3, not 1 of 10",
          "position 1 of 3" in out and "of 10" not in out)
    check("Fatima is 1 of 4 in JSS2B", "Fatima (JSS2B): 80.9%, position 1 of 4" in out)

    # 8. Equal averages share a position, and the next one skips.
    check("Dami and Emeka both sit at position 2 of 4",
          "Dami (JSS2B): 66.1%, position 2 of 4" in out
          and "Emeka (JSS2B): 66.1%, position 2 of 4" in out)
    check("Ngozi is 4 of 4, not 3 of 4",
          "Ngozi (JSS2B): 57.9%, position 4 of 4" in out)

    # 9. A class average is the mean of its students.
    check("class averages are 69.2, 67.8 and 60.3",
          "Class average JSS2A: 69.2%" in out
          and "Class average JSS2B: 67.8%" in out
          and "Class average JSS2C: 60.3%" in out)

    # 10. The pass mark is applied to the average.
    check("Chidi fails on 49.1 and Ifeanyi on 44.1",
          "Chidi (JSS2A): 49.1%, position 3 of 3, fail" in out
          and "Ifeanyi (JSS2C): 44.1%, position 3 of 3, fail" in out)
    check("eight students pass, two fail",
          out.count(", pass") == 8 and out.count(", fail") == 2, out)

    # 11. A mark written with a decimal point changes nothing.
    decimal = base.replace("Adaeze,JSS2A,Mathematics,88,100",
                           "Adaeze,JSS2A,Mathematics,88.0,100")
    code, out, err = run_with(decimal, subjects)
    check("a mark written 88.0 instead of 88 changes nothing", out == TARGET,
          repr(out) if out != TARGET else "")

    # Report.
    failed = [m for m in marks if not m[1]]
    for name, passed, detail in marks:
        print(("PASS " if passed else "FAIL ") + name + (
            "" if passed or not detail else " <- " + detail))
    print()
    print("{}/{} checks passed".format(len(marks) - len(failed), len(marks)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
