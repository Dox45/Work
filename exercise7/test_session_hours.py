"""Checks for the tutoring hours report (exercise 7).

Run from this folder:  python3 test_session_hours.py

Every check runs the real script on a copy of sessions.csv, so a check only
passes if the printed report is right, not if a helper function happens to be.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "session_hours.py")
DATA = os.path.join(HERE, "sessions.csv")

TARGET = """\
Sessions logged: 14
Completed: 10 (71.4%)
Chidi: 3 sessions, 5.0 h, avg 1.7 h
Ada: 3 sessions, 4.8 h, avg 1.6 h
Dami: 2 sessions, 3.5 h, avg 1.8 h
Bola: 2 sessions, 2.8 h, avg 1.4 h
Longest session: S03 2.5 h
Total hours: 16.0 h
"""


def run_with(csv_text):
    """Run the script in a scratch folder holding the given CSV."""
    work = tempfile.mkdtemp()
    try:
        shutil.copy(SCRIPT, os.path.join(work, "session_hours.py"))
        with open(os.path.join(work, "sessions.csv"), "w") as handle:
            handle.write(csv_text)
        result = subprocess.run(
            [sys.executable, "session_hours.py"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr
    finally:
        shutil.rmtree(work)


def read_csv():
    with open(DATA) as handle:
        return handle.read()


marks = []


def check(name, passed, detail=""):
    marks.append((name, passed, detail))


def main():
    base = read_csv()

    # 1. The real file must print the target block exactly.
    code, out, err = run_with(base)
    check("full report matches the brief exactly", out == TARGET,
          repr(out) if out != TARGET else "")

    # 2. No slice: all fourteen rows are counted, S01 is not thrown away.
    check("all fourteen sessions are logged", "Sessions logged: 14" in out)
    check("the first session (S01) is no longer dropped",
          "Ada: 3 sessions" in out)

    # 3. Minutes are turned into fractions of an hour.
    check("half hours are kept (S03 = 2.5 h)", "Longest session: S03 2.5 h" in out)
    check("quarter hours are kept (Ada 4.8 h, not 4.0 h)",
          "Ada: 3 sessions, 4.8 h" in out)

    # 4. Only completed sessions count.
    check("the ten completed sessions are counted", "Completed: 10" in out)
    check("cancelled sessions are left out (Dami has 2, not 3)",
          "Dami: 2 sessions" in out)
    check("no-show sessions are left out (Bola has 2, not 3)",
          "Bola: 2 sessions" in out)
    check("total hours covers completed sessions only",
          "Total hours: 16.0 h" in out)

    # 5. The percentage uses the number of rows, not the number of tutors.
    check("percentage is 71.4%, not 275.0%", "Completed: 10 (71.4%)" in out)

    # 6. Tutors are ordered by hours, most first.
    tutors = [line.split(":")[0] for line in out.splitlines()
              if line and ":" in line and not line.startswith(
                  ("Sessions", "Completed", "Longest", "Total"))]
    check("tutors are ordered by hours, most first",
          tutors == ["Chidi", "Ada", "Dami", "Bola"], str(tutors))

    # 7. The average divides by completed sessions, not every row with the name.
    check("Ada's average is 1.6 h, not 1.0 h",
          "Ada: 3 sessions, 4.8 h, avg 1.6 h" in out)
    check("Dami's average is 1.8 h",
          "Dami: 2 sessions, 3.5 h, avg 1.8 h" in out)

    # 8. The longest session is picked by length, not by finish time.
    check("longest session is S03, not S12 (which merely ends latest)",
          "Longest session: S03 2.5 h" in out)

    # 9. Bonus: a time written without a leading zero must not crash.
    code, out, err = run_with(base.replace("09:00,10:00", "9:00,10:00", 1))
    check("a time like 9:00 does not crash the script",
          code == 0 and not err.strip(), err.strip()[:200])
    check("a time like 9:00 still gives the same report", out == TARGET,
          repr(out) if out != TARGET else "")

    # 10. Bonus: a trailing space in a tutor name must not split the tutor.
    code, out, err = run_with(base.replace("S07,Dami,", "S07,Dami ,"))
    check("a trailing space in a name keeps one Dami line",
          out.count("Dami:") == 1, out)
    check("a trailing space in a name keeps Dami's 3.5 h",
          "Dami: 2 sessions, 3.5 h, avg 1.8 h" in out, out)
    check("a trailing space does not change the percentage",
          "Completed: 10 (71.4%)" in out, out)

    # Report.
    failed = [m for m in marks if not m[1]]
    for name, passed, detail in marks:
        print(("PASS  " if passed else "FAIL  ") + name + (
            "" if passed or not detail else "  <- " + detail))
    print()
    print("{}/{} checks passed".format(len(marks) - len(failed), len(marks)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
