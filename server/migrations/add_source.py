import json
from uuid import uuid4
import datetime
from dateutil import tz
import json

FILENAME = "../calls.json"

updated_entries = []

with open(FILENAME, 'rt') as file:
    existing_entries = json.load(file)
    for entry in existing_entries:
        entry["source"] = "orbies"
        updated_entries.append(entry)

# print(entries)

with open(FILENAME, 'wt') as file:
    file.write(json.dumps(updated_entries, indent=4))