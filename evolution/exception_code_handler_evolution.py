import os
import json
from typing import Counter
from collections import Counter

"""
RQ2 - How does exception handling code evolve ?
how often does one kind of handler transform into another
how often the bad patterns get fixed?
after how much time? 

"""


def get_times():
    evolution = dict()
    for root, dir, files in os.walk("/results/all_results"):
        for file in files:
            path = os.path.join(root, file)
            with open(path) as json_file:
                data = json.load(json_file)
                for key in data.keys():
                    try:
                        if key == "repo" or key == "total_commits":
                            continue
                        loop = data.get(key)
                        for index, i in enumerate(loop):
                            for ex in i["exception_handlers"]:
                                if len(ex['changes']) > 0:

                                    for change in ex['changes']:
                                        if evolution.get(change['from'][0]) is None:
                                            evolution[change['from'][0]] = [change["to"][0]]
                                        else:
                                            evolution.get(change['from'][0]).append(change['to'][0])

                    except IndexError as e:
                        print(e)

    for key in evolution.keys():
        print(f'from:{key}')
        print(f'to:{Counter(evolution[key])}')

    # df = pd.DataFrame.from_dict(evolution.items())
    # freq = Counter(changes)


get_times()
