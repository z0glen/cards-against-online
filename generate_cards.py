#{
#    "id": "00e7fbf2-a1aa-4df8-9e29-97e8e43d0a69",
#    "text": [
#       "a very tired barkeep"
#    ],
#    "created_at": "2020-04-09T17:32:52+00:00",
#    "nsfw": true
#},

import csv
from uuid import uuid4
import datetime
from dateutil import tz
import json

entries = []

with open('testcsv.csv', 'r') as file:
    reader = csv.reader(file, delimiter='_')
    for row in reader:
        # print(row)
        entry = {
            "id": str(uuid4()),
            "text": row,
            "created_at": datetime.datetime.now(tz.tzlocal()).strftime("%Y-%m-%dT%H:%M:%S%z"),
            "nsfw": "true"
        }
        entries.append(entry)

# print(entries)

with open('test_output.json', 'w') as file:
    file.write(json.dumps(entries, indent=3))
