import os
import json
from datetime import date, datetime
import numpy as np
import pandas as pd
import statistics

"""
RQ2 - How does exception handling code evolve ?
how often does one kind of handler transform into another
how often the bad patterns get fixed?
after how much time? 

check if "CodeSmellAddedOrRemoved": "" or "removed" and look for changes in robustness. We must assume that a removal and a addition in robustness is a change for the better. 

"""

evolution = dict()

def get_times():
    for root, dir, files in os.walk(""):
        for file in files:
            try:     
                path = os.path.join(root, file)
                with open(path) as json_file:
                    data = json.load(json_file)
                    for key in data.keys():
                        if key == "repo" or key == "total_commits":
                            continue
                        for v in data.get(key):
                            for ex in v["exception_handlers"]:
                                if ex["exception_smell_added_or_removed"] == "added":
                                    d3 = datetime.fromisoformat(v['date'])
                                    evolution[key] = []
                                    evolution[key].append(dict({'CS_Added':d3}))

                                if evolution.get(key) is not None:
                                    if ex["exception_smell_added_or_removed"] == "removed":
                                        d4 = datetime.fromisoformat(v['date'])
                                        evolution[key].append(dict(CS_Removed=d4))

            except Exception as e:
                print(str(e))           


get_times()

def Average(lst):
    return sum(lst) / len(lst)

times = []
fixed = 0
notfixed = 0
for k ,v in evolution.items():
    if len(v) == 2: 
        d1 = v[0]['CS_Added']
        d2 = v[1]['CS_Removed']
        delta = abs(d2-d1)
        times.append(delta.days)
        fixed +=1
        continue

    notfixed += 1
##print(times) 
times.sort()
print(fixed+notfixed)
print(f"Median {statistics.median(times)}")
print("Average time to fix {}".format(Average(times)))
print("Number that has been fixed {}".format(fixed))
print("Number that has not been fixed {}".format(notfixed))
print("Average that has been fixed {}".format(fixed / (fixed+notfixed) * 100))
print("Average that has not been fixed {}".format(notfixed / (fixed+notfixed) * 100))
print("Highest number of days before fix {}".format(times[-1]))
print("Lowest number of days before fix {}".format(times[0]))

x = np.array(times)
pd.DataFrame(x).to_csv("robustness_corroboration_results.csv")
