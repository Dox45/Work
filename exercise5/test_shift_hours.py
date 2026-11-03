"""Local checks for exercise5/shift_hours.py.

Each case builds a small csv, runs the report and compares what was printed.
"""

import contextlib
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shift_hours as report

HERE = os.path.dirname(os.path.abspath(__file__))


def row(name, hours):
    """One line of the table exactly as the brief lays it out."""
    return name.ljust(8) + " " + "{:.1f}".format(hours).rjust(4)


def table(shifts, rows, long_shifts, total):
    lines = ["Shifts logged: " + str(shifts)]
    lines += [row(name, hours) for name, hours in rows]
    lines.append("Long shifts: " + long_shifts)
    lines.append("Total hours: " + "{:.1f}".format(total))
    return "\n".join(lines) + "\n"


TARGET = table(
    9,
    [("Dami", 14.0), ("Ada", 11.5), ("Bola", 9.0), ("Chidi", 7.0)],
    "Chidi",
    41.5,
)


def run(csv_text):
    handle, path = tempfile.mkstemp(suffix=".csv", dir=HERE, text=True)
    with os.fdopen(handle, "w", newline="") as opened:
        opened.write(csv_text)
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            report.report(path)
    finally:
        os.remove(path)
    return out.getvalue(), err.getvalue()


def case(name, csv_text, expected=None, checks=(), warnings=()):
    got, err = run(csv_text)
    problems = []
    if expected is not None and got != expected:
        problems.append("printed output did not match")
    for check in checks:
        if check not in got:
            problems.append("output is missing: " + check)
    for warning in warnings:
        if warning not in err:
            problems.append("not reported: " + warning)
    ok = not problems
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("--- got ---")
        print(got)
        print("--- errors ---")
        print(err)
        for problem in problems:
            print("  " + problem)
    return ok


with open("shifts.csv", newline="") as real:
    real_csv = real.read()

results = [
    case("real shifts.csv matches the target exactly", real_csv, TARGET),
    case("a blank line at the end is ignored, not a crash", real_csv + "\n", TARGET),
    case(
        "a blank line in the middle is ignored",
        "volunteer,date,start,end\n"
        "Ada,2026-10-04,09:00,14:30\n"
        "\n"
        "Bola,2026-10-05,10:00,16:00\n",
        table(2, [("Bola", 6.0), ("Ada", 5.5)], "none", 11.5),
    ),
    case(
        "minutes are divided by 60, so 09:00-15:30 is 6.5 hours",
        "volunteer,date,start,end\nAda,2026-10-04,09:00,15:30\n",
        table(1, [("Ada", 6.5)], "none", 6.5),
    ),
    case(
        "a volunteer's shifts are added up, not overwritten",
        "volunteer,date,start,end\n"
        "Dami,2026-10-03,09:00,15:30\n"
        "Dami,2026-10-10,08:00,12:00\n",
        table(2, [("Dami", 10.5)], "none", 10.5),
    ),
    case(
        "the table is ordered largest first",
        "volunteer,date,start,end\n"
        "Ada,2026-10-04,09:00,10:00\n"
        "Bola,2026-10-05,09:00,14:00\n"
        "Chidi,2026-10-06,09:00,12:00\n",
        table(3, [("Bola", 5.0), ("Chidi", 3.0), ("Ada", 1.0)], "none", 9.0),
    ),
    case(
        "exactly 7.0 hours counts as a long shift",
        "volunteer,date,start,end\nChidi,2026-10-06,08:00,15:00\n",
        table(1, [("Chidi", 7.0)], "Chidi", 7.0),
    ),
    case(
        "six hours fifty-nine is not a long shift",
        "volunteer,date,start,end\nChidi,2026-10-06,08:00,14:59\n",
        table(1, [("Chidi", 6.98)], "none", 6.98),
    ),
    case(
        "several long shifts are listed alphabetically",
        "volunteer,date,start,end\n"
        "Dami,2026-10-03,07:00,15:30\n"
        "Ada,2026-10-04,07:00,16:00\n"
        "Bola,2026-10-05,09:00,12:00\n",
        table(3, [("Ada", 9.0), ("Dami", 8.5), ("Bola", 3.0)], "Ada, Dami", 20.5),
    ),
    case(
        "shifts logged counts rows, not people",
        "volunteer,date,start,end\n"
        "Ada,2026-10-04,09:00,10:00\n"
        "Ada,2026-10-05,09:00,10:00\n"
        "Ada,2026-10-06,09:00,10:00\n",
        table(3, [("Ada", 3.0)], "none", 3.0),
    ),
    case(
        "a shift that ends before it starts is rejected, not shown as negative",
        "volunteer,date,start,end\n"
        "Ada,2026-10-20,15:00,11:00\n"
        "Bola,2026-10-05,09:00,12:00\n",
        table(1, [("Bola", 3.0)], "none", 3.0),
        warnings=("line 2", "ends before it starts"),
    ),
    case(
        "a non-numeric time is reported on its line",
        "volunteer,date,start,end\nAda,2026-10-20,nine,11:00\n",
        table(0, [], "none", 0.0),
        warnings=("line 2", "HH:MM"),
    ),
    case(
        "a row with too few fields is reported, not silently dropped",
        "volunteer,date,start,end\nAda,2026-10-20,09:00\n",
        table(0, [], "none", 0.0),
        warnings=("line 2", "expected 4 fields"),
    ),
]

passed = sum(1 for ok in results if ok)
print("")
print(str(passed) + "/" + str(len(results)) + " checks passed")
