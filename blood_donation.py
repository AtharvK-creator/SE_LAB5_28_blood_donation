"""Blood donation management system demonstration."""

import shutil
import subprocess
import tempfile
from datetime import date, timedelta

donors = []

stock = {
    "A+": 0,
    "A-": 0,
    "B+": 0,
    "B-": 0,
    "O+": 0,
    "O-": 0,
    "AB+": 0,
    "AB-": 0,
}

COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
}


def register_donor(
    donor_name,
    blood_group,
    age,
    last_donation=None,
    notes=None,
):
    """Register a donor after validating blood group and age."""
    if notes is None:
        notes = []

    if blood_group not in stock:
        raise ValueError("Unknown blood group")

    if age < 18 or age > 65:
        notes.append(f"{donor_name} is not eligible because of age")
        return False

    donors.append({
        "name": donor_name,
        "group": blood_group,
        "last": last_donation,
    })
    return True


def can_donate(donor):
    """Check whether a donor can donate again."""
    if donor["last"] is None:
        return True

    return date.today() - donor["last"] >= timedelta(days=90)


def record_donation(donor_name, units=1):
    """Record a donation and update blood-group stock."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True

    return False


def units_for(patient_group):
    """Return available units compatible with a patient's group."""
    if patient_group not in COMPATIBLE:
        return 0

    return sum(
        stock[group]
        for group in COMPATIBLE[patient_group]
    )


def is_universal(blood_group):
    """Check the existing universal blood-group classifications."""
    return blood_group in {"O-", "AB+"}


def low_stock(threshold=2):
    """Return blood groups with stock below the given threshold."""
    return [
        group
        for group, units in stock.items()
        if units < threshold
    ]


def donor_sheet_path():
    """Create a temporary CSV file and return its path."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
    ) as temp_file:
        return temp_file.name


def notify_donors(phone_list):
    """Run the SMS command without invoking a shell."""
    executable = shutil.which("send-sms")

    if executable is None:
        raise FileNotFoundError("The send-sms command was not found.")

    subprocess.run(
        [executable, *phone_list],
        check=True,
        shell=False,
    )


def main():
    """Run the blood donation management demonstration."""
    register_donor("Arjun", "O+", 25)
    register_donor(
        "Priya",
        "A+",
        30,
        date.today() - timedelta(days=30),
    )
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)

    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")

    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())  # Below 2 units

    eligible = [
        donor["name"]
        for donor in donors
        if can_donate(donor)
    ]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
