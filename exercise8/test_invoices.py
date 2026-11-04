"""Checks for the invoice run (exercise 8).

Run from this folder:  python3 test_invoices.py

Every check runs the real script on a scratch copy of billing.csv and
rates.csv, so a check only passes if the printed invoice is right, not if a
helper function happens to be.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "invoices.py")
BILLING = os.path.join(HERE, "billing.csv")
RATES = os.path.join(HERE, "rates.csv")

TARGET = """\
Invoice period: 02/11/2026 to 15/11/2026
Sessions: 18 logged, 15 billable
Chidi: 7.0 h x 5200.00 = 36400.00
Dami: 6.0 h x 5600.00 = 33600.00
Ada: 6.0 h x 4500.00 = 27000.00
Bola: 3.5 h x 4200.00 = 14700.00
Subtotal: 111700.00
VAT at 7.5%: 8377.50
Total due: 120077.50
First session: 02/11/2026
Last session: 15/11/2026
"""


def read(path):
    with open(path) as handle:
        return handle.read()


def run_with(billing_text, rates_text):
    """Run the script in a scratch folder holding the given two files."""
    work = tempfile.mkdtemp()
    try:
        shutil.copy(SCRIPT, os.path.join(work, "invoices.py"))
        with open(os.path.join(work, "billing.csv"), "w") as handle:
            handle.write(billing_text)
        with open(os.path.join(work, "rates.csv"), "w") as handle:
            handle.write(rates_text)
        result = subprocess.run(
            [sys.executable, "invoices.py"],
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


def tutor_lines(out):
    return [line.split(":")[0] for line in out.splitlines()
            if " h x " in line]


def main():
    base = read(BILLING)
    rates = read(RATES)

    # 1. The real files must print the target block exactly.
    code, out, err = run_with(base, rates)
    check("full invoice matches the brief exactly", out == TARGET,
          repr(out) if out != TARGET else "")
    check("the script still exits cleanly", code == 0 and not err.strip(),
          err.strip()[:200])

    # 2. The billable count describes the same sessions the money does.
    check("the count is 15 billable, not 16", "18 logged, 15 billable" in out)
    check("S18 (16/11/2026) is outside the period and not billed",
          "Ada: 6.0 h" in out)

    # 3. Both ends of the period count.
    check("Monday 02/11 is billed (Ada 6.0 h, not 4.5 h)", "Ada: 6.0 h" in out)
    check("Monday 02/11 is billed for Bola too (3.5 h, not 2.5 h)",
          "Bola: 3.5 h" in out)
    check("first session is 02/11/2026", "First session: 02/11/2026" in out)

    # 4. Dates are compared as dates, not as text.
    check("last session is 15/11/2026, not 9/11/2026",
          "Last session: 15/11/2026" in out)

    # 5. The unpaid break is taken off long sessions, and only long ones.
    check("Chidi's 7.0 h has the three half-hour breaks off (not 8.0 h)",
          "Chidi: 7.0 h" in out)
    check("a session of exactly 2 hours does get the break",
          "Chidi: 7.0 h x 5200.00 = 36400.00" in out)

    # 6. Each tutor is paid their own rate.
    check("Chidi is paid 5200.00, not 4500.00", "x 5200.00" in out)
    check("Bola is paid 4200.00, not 4500.00", "x 4200.00" in out)
    check("Ada and Dami are paid their own rates too",
          "x 4500.00" in out and "x 5600.00" in out)

    # 7. Fractions of an hour are kept.
    check("Bola's 45-minute session is billed (3.5 h, not 1.0 h)",
          "Bola: 3.5 h" in out)

    # 8. VAT is a percentage of the subtotal.
    check("VAT is 8377.50, not 641250.00", "VAT at 7.5%: 8377.50" in out)

    # 9. Total due includes the VAT.
    check("total due is subtotal plus VAT (120077.50)",
          "Total due: 120077.50" in out)

    # 10. Biggest amount owed first.
    check("tutors are ordered by amount, biggest first",
          tutor_lines(out) == ["Chidi", "Dami", "Ada", "Bola"],
          str(tutor_lines(out)))

    # 11. Bonus: a session that runs past midnight must not go negative.
    midnight = base.replace(
        "S05,Ada,04/11/2026,16:00,17:30,completed",
        "S05,Ada,04/11/2026,23:00,00:00,completed",
    )
    code, out, err = run_with(midnight, rates)
    check("a session past midnight does not crash",
          code == 0 and not err.strip(), err.strip()[:200])
    check("a session past midnight is 1.0 h, not -23.0 h",
          "Ada: 5.5 h x 4500.00 = 24750.00" in out, out)
    check("no tutor line goes negative", "-" not in out.replace(" ", ""), out)

    # 12. Bonus: a tutor with no rate row must not stop the invoice.
    without_dami = "\n".join(
        line for line in rates.splitlines() if not line.startswith("Dami")
    ) + "\n"
    code, out, err = run_with(base, without_dami)
    check("a missing rate row does not crash the script",
          code == 0 and not err.strip(), err.strip()[:200])
    check("the missing tutor is named in the output",
          "Missing rate: Dami" in out, out)
    check("the other tutors are still billed",
          "Chidi: 7.0 h x 5200.00 = 36400.00" in out, out)
    check("the missing tutor is never billed at someone else's rate",
          "Dami: " not in out, out)

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
