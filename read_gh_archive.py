import sys
import os
import ast
import json

commits = []
for i in range(0, 24):
    events = []
    push_events = []
    for line in open(f"events/2021-03-10-{i}.json", 'r'):
        events.append(json.loads(line))

    for event in events:
        if event['type'] == "PushEvent":
            push_events.append(event)
            commits.append(event['payload']['commits'])

    filename = f"hour_{i}_push_events.json"
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(push_events, indent=4))

print(len(commits))