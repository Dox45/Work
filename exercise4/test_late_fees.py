"""Local checks for exercise4/late_fees.py.

Each case builds a small csv, runs the report and compares what was printed.
"""

import io
import os
import sys
import tempfile
import contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import late_fees as report

TARGET = """Late returns (9 overdue loans)
Bola       2100   2
Dami       1850   2
Ada        1800   3
Chidi       700   2
Chronic borrowers: Ada
Total fines: 6450
"""


def run(csv_text):
    handle, path = tempfile.mkstemp(suffix=".csv", dir=".", text=True)
    with os.fdopen(handle, "w", newline="") as opened:
        opened.write(csv_text)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            report.report(path)
    finally:
        os.remove(path)
    return buffer.getvalue()


def case(name, csv_text, expected=None, checks=()):
    got = run(csv_text)
    if expected is not None:
        ok = got == expected
    else:
        ok = all(check in got for check in checks)
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("--- got ---")
        print(got)
    return ok


with open("loans.csv", newline="") as real:
    real_csv = real.read()

results = [
    case("real loans.csv matches target exactly", real_csv, TARGET),
    case(
        "one 40-day loan is capped at 1500, not 2000",
        "member,book,days_late\nAda,One,40\n",
        """Late returns (1 overdue loans)
Ada        1500   1
Chronic borrowers: none
Total fines: 1500
""",
    ),
    case(
        "two 40-day loans owe 3000, cap is per loan",
        "member,book,days_late\nAda,One,40\nAda,Two,40\n",
        """Late returns (2 overdue loans)
Ada        3000   2
Chronic borrowers: none
Total fines: 3000
""",
    ),
    case(
        "nobody late does not crash",
        "member,book,days_late\nAda,One,0\nBola,Two,0\n",
        """Late returns (0 overdue loans)
Chronic borrowers: none
Total fines: 0
""",
    ),
    case(
        "blank line at end is silent",
        "member,book,days_late\nAda,One,10\n\n",
        """Late returns (1 overdue loans)
Ada         500   1
Chronic borrowers: none
Total fines: 500
""",
    ),
    case(
        "abc days_late skipped with a message",
        "member,book,days_late\nAda,One,10\nBola,Two,abc\n",
        checks=("Skipped line 3", "invalid literal", "Total fines: 500"),
    ),
    case(
        "negative days_late reported as bad data",
        "member,book,days_late\nAda,One,10\nBola,Two,-5\n",
        checks=("Skipped line 3", "negative days_late -5", "Total fines: 500"),
    ),
    case(
        "short row is reported, not swallowed",
        "member,book,days_late\nAda,One,10\nBola,Two\n",
        checks=("Skipped line 3", "list index out of range", "Total fines: 500"),
    ),
    case(
        "three overdue loans flag a chronic borrower",
        "member,book,days_late\nAda,One,1\nAda,Two,1\nAda,Three,1\nBola,Four,1\n",
        checks=("Chronic borrowers: Ada", "Total fines: 200"),
    ),
]

print()
print("{}/{} checks passed".format(sum(results), len(results)))
sys.exit(0 if all(results) else 1)
