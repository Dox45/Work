"""Local checks for exercise6/parcel_report.py.

Each case builds a small csv, runs the report and compares what was printed.
"""

import io
import os
import sys
import tempfile
import contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parcel_report as report

TARGET = """Parcels delivered: 9 of 12
Zone A: 3 delivered, 23.9 kg
Zone B: 4 delivered, 12.4 kg
Zone C: 2 delivered, 4.5 kg
Heaviest: P006 12.0 kg
Average weight: 4.5 kg
Success rate: 75.0%
Total weight: 40.8 kg
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


with open("parcels.csv", newline="") as real:
    real_csv = real.read()

results = [
    case("real parcels.csv matches target exactly", real_csv, TARGET),
    case(
        "only delivered parcels count",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,2.5,delivered\nP002,A,1.5,returned\nP003,B,3.0,failed\n",
        """Parcels delivered: 1 of 3
Zone A: 1 delivered, 2.5 kg
Heaviest: P001 2.5 kg
Average weight: 2.5 kg
Success rate: 33.3%
Total weight: 2.5 kg
""",
    ),
    case(
        "weights keep their decimals",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,2.5,delivered\nP002,A,0.5,delivered\n",
        """Parcels delivered: 2 of 2
Zone A: 2 delivered, 3.0 kg
Heaviest: P001 2.5 kg
Average weight: 1.5 kg
Success rate: 100.0%
Total weight: 3.0 kg
""",
    ),
    case(
        "heaviest is compared as a number, 12.0 beats 9.4",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,9.4,delivered\nP002,A,12.0,delivered\n",
        """Parcels delivered: 2 of 2
Zone A: 2 delivered, 21.4 kg
Heaviest: P002 12.0 kg
Average weight: 10.7 kg
Success rate: 100.0%
Total weight: 21.4 kg
""",
    ),
    case(
        "last parcel in the file is not dropped",
        "parcel_id,zone,weight_kg,status\n"
        "P001,B,1.0,delivered\nP002,B,2.0,delivered\n",
        checks=("2 of 2", "Zone B: 2 delivered, 3.0 kg"),
    ),
    case(
        "blank line at end adds no parcel",
        "parcel_id,zone,weight_kg,status\nP001,A,2.5,delivered\n\n",
        checks=("Parcels delivered: 1 of 1", "Total weight: 2.5 kg"),
    ),
    case(
        "empty weight is reported, the report still finishes",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,2.5,delivered\nP002,A,,delivered\n",
        checks=("Skipped parcel P002", "Parcels delivered: 1 of 2", "Total weight: 2.5 kg"),
    ),
    case(
        "a parcel listed twice is counted once",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,2.5,delivered\nP001,A,2.5,delivered\n",
        checks=("listed twice", "Parcels delivered: 1 of 2", "Total weight: 2.5 kg"),
    ),
    case(
        "nothing delivered does not crash",
        "parcel_id,zone,weight_kg,status\nP001,A,2.5,returned\n",
        """Parcels delivered: 0 of 1
Heaviest: none
Average weight: 0.0 kg
Success rate: 0.0%
Total weight: 0.0 kg
""",
    ),
    case(
        "negative weight reported as bad data",
        "parcel_id,zone,weight_kg,status\n"
        "P001,A,2.5,delivered\nP002,A,-1,delivered\n",
        checks=("Skipped parcel P002", "negative weight -1", "Total weight: 2.5 kg"),
    ),
]

print()
print("{}/{} checks passed".format(sum(results), len(results)))
sys.exit(0 if all(results) else 1)
