import sys
import os
import ast
import json
from typing import Counter
from git import repo
from pydriller import RepositoryMining, git_repository
from pydriller import GitRepository
import time

total_commits = 0
nested_try = 0
unchecked_exception = 0
print_statement = 0
return_code = 0
ignored_checked_exception = 0
error_reporting = 0
state_recovery = 0
behavior_recovery = 0
code_smell_added = 0
code_smell_removed = 0
robustness_added = 0
robustness_removed = 0
for root, dir, files in os.walk("repo_results_13-04/Python_topic_machine_learning"):
    for file in files:
        try:     
            path = os.path.join(root, file)
            with open(path) as json_file:
                data = json.load(json_file)
                for key in data.keys():
                    if key == "repo" or key == "total_commits":
                        continue
                    for index in range(len(data.get(key))):
                        #nested_try += data.get(key)[index][2]["nested_try"]
                        #unchecked_exception += data.get(key)[index][3]["unchecked_exception"]   
                        #print_statement += data.get(key)[index][4]["print_statement"]   
                        #return_code += data.get(key)[index][5]["return_code"]   
                        #ignored_checked_exception += data.get(key)[index][6]["ignored_checked_exception"]   
                        #error_reporting += data.get(key)[index][8]["error_reporting"]
                        #state_recovery += data.get(key)[index][9]["state_recovery"] 
                        #behavior_recovery += data.get(key)[index][10]["behavior_recovery"]  
                        if data.get(key)[index][7]["CodeSmellAddedOrRemoved"] == "added":
                            code_smell_added += 1
                            if data.get(key)[index][2]["nested_try"] > 0:
                                nested_try += data.get(key)[index][2]["nested_try"]
                            if data.get(key)[index][3]["unchecked_exception"] > 0:
                                unchecked_exception += data.get(key)[index][3]["unchecked_exception"]
                            if data.get(key)[index][4]["print_statement"] > 0:
                                print_statement += data.get(key)[index][4]["print_statement"]
                            if data.get(key)[index][5]["return_code"] > 0:
                                return_code += data.get(key)[index][5]["return_code"]
                            if data.get(key)[index][6]["ignored_checked_exception"] > 0:
                                ignored_checked_exception += data.get(key)[index][6]["ignored_checked_exception"]
                            
                                                            
                        if data.get(key)[index][7]["CodeSmellAddedOrRemoved"] == "removed":
                            code_smell_removed += 1
                        if data.get(key)[index][11]["RobustnessAddedOrRemoved"] == "added":
                            robustness_added += 1
                            if data.get(key)[index][8]["error_reporting"] > 0:
                                error_reporting += data.get(key)[index][8]["error_reporting"]
                            if data.get(key)[index][9]["state_recovery"] > 0:
                                state_recovery += data.get(key)[index][9]["state_recovery"]
                            if data.get(key)[index][10]["behavior_recovery"] > 0:
                                behavior_recovery += data.get(key)[index][10]["behavior_recovery"]
                        if data.get(key)[index][11]["RobustnessAddedOrRemoved"] == "removed":
                            robustness_removed += 1

                ##print(data["repo"])
                total_commits += data["total_commits"]
                
                ##print(key)
                
        except Exception as e:
            print(str(e))           
print("Total commits: {}".format(total_commits))
print("Nested try count: {}".format(nested_try))
print("Unchecked_exception count: {}".format(unchecked_exception))
print("Print statement count: {}".format(print_statement))
print("Return code count: {}".format(return_code))
print("ignored_checked_exception count: {}".format(ignored_checked_exception) )
print("error_reporting count: {}".format(error_reporting))
print("state_recovery count: {}".format(state_recovery))
print("behavior_recovery count: {}".format(behavior_recovery))
print("code_smell_added count: {}".format(code_smell_added))
print("code_smell_removed count: {}".format(code_smell_removed))
print("robustness_added count: {}".format(robustness_added))
print("robustness_removed count: {}".format(robustness_removed))

"""
try:     
    ##path = os.path.join(root, file)
    with open("zeeguu/zeeguu-ecosystem_Zeeguu-Core_result.json") as json_file:
        data = json.load(json_file)
        for key in data.keys():
            if key == "repo" or key == "total_commits":
                continue
            ##print(key)
            nested_try += data.get(key)[-1][2]["nested_try"]
            unchecked_exception += data.get(key)[-1][3]["unchecked_exception"]   
            print_statement += data.get(key)[-1][4]["print_statement"]   
            return_code += data.get(key)[-1][5]["return_code"]   
            ignored_checked_exception += data.get(key)[-1][6]["ignored_checked_exception"]   
            error_reporting += data.get(key)[-1][8]["error_reporting"]
            state_recovery += data.get(key)[-1][9]["state_recovery"] 
            behavior_recovery += data.get(key)[-1][10]["behavior_recovery"]         
           
                

        ##print(data["repo"])
        total_commits += data["total_commits"]
        
        ##print(key)
        
except Exception as e:
    print(str(e)) 
"""
