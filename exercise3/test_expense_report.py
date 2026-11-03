"""Local checks for exercise3/expense_report.py.

Each case builds a small csv, runs the report and compares what was printed.
"""

import io
import os
import sys
import tempfile
import contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expense_report as report

TARGET = """Expense report (8 rows)
Travel       2450   37%
Software     1899   29%
Equipment    1500   23%
Meals         750   11%
Over budget: Travel, Software, Equipment
Total: 6599
"""


def run(csv_text):
    handle, path = tempfile.mkstemp(suffix=".csv", dir=".", text=True)
    with os.fdopen(handle, "w", newline="") as opened:
        opened.write(csv_text)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            report.build_report(path)
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


with open("expenses.csv", newline="") as real:
    real_csv = real.read()

results = [
    case("real expenses.csv matches target exactly", real_csv, TARGET),
    case(
        "one category only = 100%",
        "date,category,amount\n2026-10-02,Travel,100\n2026-10-03,Travel,150\n",
        """Expense report (2 rows)
Travel        250  100%
Over budget: none
Total: 250
""",
    ),
    case(
        "header only does not crash",
        "date,category,amount\n",
        """Expense report (0 rows)
Over budget: none
Total: 0
""",
    ),
    case(
        "blank line at end is silent",
        "date,category,amount\n2026-10-02,Travel,1200\n\n",
        """Expense report (1 rows)
Travel       1200  100%
Over budget: none
Total: 1200
""",
    ),
    case(
        "abc amount skipped with a message",
        "date,category,amount\n2026-10-02,Travel,1200\n2026-10-03,Meals,abc\n",
        checks=("Skipped line 3", "invalid literal", "Total: 1200"),
    ),
    case(
        "negative amount rejected",
        "date,category,amount\n2026-10-02,Travel,1200\n2026-10-03,Meals,-500\n",
        checks=("Skipped line 3", "negative amount -500", "Total: 1200"),
    ),
    case("empty file does not crash", "", checks=("Expense report (0 rows)", "Total: 0")),
    case(
        "short row is reported, not swallowed",
        "date,category,amount\n2026-10-02,Travel,1200\n2026-10-03,Meals\n",
        checks=("Skipped line 3", "list index out of range", "Total: 1200"),
    ),
]

print()
print("{}/{} checks passed".format(sum(results), len(results)))
sys.exit(0 if all(results) else 1)
