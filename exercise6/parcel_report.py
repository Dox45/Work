"""Parcel delivery report.

Reads parcels.csv and prints a summary of the week's deliveries.

The output matches the target in PARCEL_REPORT_EXERCISE.md:

    Parcels delivered: 9 of 12
    Zone A: 3 delivered, 23.9 kg
    Zone B: 4 delivered, 12.4 kg
    Zone C: 2 delivered, 4.5 kg
    Heaviest: P006 12.0 kg
    Average weight: 4.5 kg
    Success rate: 75.0%
    Total weight: 40.8 kg
"""

import csv

FILENAME = "parcels.csv"


def load_rows(path):
    """Every data row of the file, in order.

    ``csv.DictReader`` already skips blank lines, so nothing is trimmed here:
    slicing the list would drop a real parcel.
    """
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_weight(text):
    """The weight as a decimal number of kilos, or ValueError if it is not one."""
    weight = float(text.strip())
    if weight < 0:
        raise ValueError("negative weight {}".format(text.strip()))
    return weight


def summarise(rows):
    """Return the totals needed for the report.

    A row that cannot be read is reported by parcel id and skipped, and a parcel
    listed twice is counted once so the totals stay honest. Only the problems we
    expect are caught, so a real bug still shows up instead of being swallowed.
    """
    seen = set()
    zone_count = {}
    zone_weight = {}
    total_weight = 0.0
    delivered = 0
    heaviest_id = ""
    heaviest_weight = 0.0

    for row in rows:
        parcel_id = (row.get("parcel_id") or "").strip()

        if parcel_id and parcel_id in seen:
            print("Skipped parcel {}: listed twice".format(parcel_id))
            continue

        try:
            if not parcel_id:
                raise ValueError("missing parcel_id")
            zone = (row.get("zone") or "").strip()
            if not zone:
                raise ValueError("missing zone")
            weight = parse_weight(row.get("weight_kg") or "")
        except (ValueError, AttributeError) as problem:
            print("Skipped parcel {}: {}".format(parcel_id or "?", problem))
            continue

        seen.add(parcel_id)

        # Only a delivered parcel counts towards any weight, count or average.
        if (row.get("status") or "").strip() != "delivered":
            continue

        delivered += 1
        zone_count[zone] = zone_count.get(zone, 0) + 1
        zone_weight[zone] = zone_weight.get(zone, 0.0) + weight
        total_weight += weight

        # Compare numbers, not text: as text "9.4" would beat "12.0".
        if weight > heaviest_weight:
            heaviest_weight = weight
            heaviest_id = parcel_id

    return {
        "rows": len(rows),
        "delivered": delivered,
        "zone_count": zone_count,
        "zone_weight": zone_weight,
        "total_weight": total_weight,
        "heaviest_id": heaviest_id,
        "heaviest_weight": heaviest_weight,
    }


def report(path):
    data = summarise(load_rows(path))
    delivered = data["delivered"]
    total_rows = data["rows"]

    print("Parcels delivered: {} of {}".format(delivered, total_rows))

    for zone in sorted(data["zone_weight"]):
        print(
            "Zone {}: {} delivered, {:.1f} kg".format(
                zone, data["zone_count"][zone], data["zone_weight"][zone]
            )
        )

    if not delivered:
        print("Heaviest: none")
        print("Average weight: 0.0 kg")
        print("Success rate: 0.0%")
        print("Total weight: 0.0 kg")
        return

    print(
        "Heaviest: {} {:.1f} kg".format(data["heaviest_id"], data["heaviest_weight"])
    )
    print("Average weight: {:.1f} kg".format(data["total_weight"] / delivered))
    share = (delivered / total_rows * 100) if total_rows else 0.0
    print("Success rate: {:.1f}%".format(share))
    print("Total weight: {:.1f} kg".format(data["total_weight"]))


if __name__ == "__main__":
    report(FILENAME)
