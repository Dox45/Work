"""Parcel delivery report.

Reads parcels.csv and prints a summary of the week's deliveries.

THIS VERSION IS BROKEN ON PURPOSE. See PARCEL_REPORT_EXERCISE.md for what it
is supposed to print.
"""

import csv

FILENAME = "parcels.csv"


def load_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    rows = load_rows(FILENAME)

    # The file ends with an empty line in the editor, so drop the last one.
    rows = rows[:-1]

    zone_count = {}
    zone_weight = {}
    total_weight = 0
    delivered = 0
    heaviest_id = ""
    heaviest_weight = ""

    for row in rows:
        zone = row["zone"]
        zone_count[zone] = zone_count.get(zone, 0) + 1

        if row["status"] == "returned":
            continue

        delivered = delivered + 1
        weight = int(float(row["weight_kg"]))
        zone_weight[zone] = zone_weight.get(zone, 0) + weight
        total_weight = total_weight + weight

        if row["weight_kg"] > heaviest_weight:
            heaviest_weight = row["weight_kg"]
            heaviest_id = row["parcel_id"]

    print("Parcels delivered: " + str(delivered) + " of " + str(len(rows)))

    for zone in sorted(zone_weight):
        print(
            "Zone " + zone + ": " + str(zone_count.get(zone, 0))
            + " delivered, " + "{:.1f}".format(zone_weight[zone]) + " kg"
        )

    print("Heaviest: " + heaviest_id + " " + heaviest_weight + " kg")
    print("Average weight: " + "{:.1f}".format(total_weight / len(zone_weight)) + " kg")
    print("Success rate: " + "{:.1f}".format(delivered / len(rows)) + "%")
    print("Total weight: " + "{:.1f}".format(total_weight) + " kg")


if __name__ == "__main__":
    main()
