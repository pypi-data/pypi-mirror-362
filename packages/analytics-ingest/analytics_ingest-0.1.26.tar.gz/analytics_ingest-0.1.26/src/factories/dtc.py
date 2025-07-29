import random
from datetime import datetime, timezone, timedelta
from faker import Faker

fake = Faker()


def random_hex_status():
    return f"{random.randint(0, 255):02X}"  # e.g., "AF"


def dtc_factory(num_entries=10):
    base_time = datetime.now(timezone.utc)
    dtc_data = []

    for i in range(num_entries):
        entry_time = (base_time + timedelta(seconds=i)).isoformat()

        entry = {
            "dtcId": f"P{random.randint(1000, 9999)}-{random.randint(10, 99)}",
            "value": random.choice(["ACTIVE", "PASSIVE"]),
            "status": random_hex_status(),
            "description": fake.sentence(nb_words=6),
            "time": entry_time,
            "extension": [],
            "snapshot": [],
        }

        if random.choice([True, False]):
            entry["extension"].append(
                {
                    "bytes": fake.hexify(text="^" * 8),
                }
            )

        if random.choice([True, False]):
            entry["snapshot"].append(
                {
                    "bytes": fake.hexify(text="^" * 8),
                }
            )

        dtc_data.append(entry)

    return {"data": dtc_data}
