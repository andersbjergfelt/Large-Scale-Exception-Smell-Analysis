import sys
import os
import ast
import json
from typing import Counter, OrderedDict
from pydriller import GitRepository, RepositoryMining
import time
from operator import itemgetter
from collections import defaultdict
from multiprocessing import Pool 
from multiprocessing import Process, Manager
import ghlinguist as ghl
import os.path
from os import path
from github import Github


def python_in_a_day_on_gh(repo, repo_commits):
    print("Analysing repo ... {}".format(repo))
    is_python = True
    language_found = False
    file = ""
    commits_with_code_smells_dict = dict()
    total_number_of_commits = len(repo_commits)
    ##nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, error_reporting, state_recovery, behavior_recovery = 0,0,0,0,0,0,0,0
    ##robustness_exception_handling, any_code_smell = False, False
    try:
        for commit in RepositoryMining(f"https://github.com/{repo}.git", only_commits=repo_commits, only_modifications_with_file_types=['.py']).traverse_commits():
            """
            if language_found == False:
                langs = ghl.linguist(commit.project_path)
                for language in langs:
                    if language[0] == "Python":
                        is_python = True
                        language_found = True
                    if language[0] == "C#":
                        with open("csharp_repo.txt", "a") as txt_file:
                             txt_file.write(f"{repo}\n")
            """
            if is_python:    
                for modification in commit.modifications:
                
                    if modification.old_path is None:
                        path = modification.new_path
                    else:
                        path = modification.old_path
                    
                    source_code = None
                    file = None
                    if ".py" in str(modification.filename):
                        source_code = modification.source_code
                        file = path
                    else:
                        continue

                    
                    nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, any_code_smell, error_reporting, state_recovery, behavior_recovery, robustness_exception_handling = get_exception_handling_evolution(source_code)

                    code_smell = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}),dict({'CodeSmellAddedOrRemoved': "added"}) ,dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}) , dict({'RobustnessAddedOrRemoved': ""}))
                    robustness = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': ""}), dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}) , dict({'RobustnessAddedOrRemoved': "added"}))
                    removed_code_smell = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': "removed"}) , dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}), dict({'RobustnessAddedOrRemoved': ""}))
                    removed_robustness  = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': ""}), dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}),dict({'RobustnessAddedOrRemoved': "removed"}))
                    both_added = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': "added"}) , dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}), dict({'RobustnessAddedOrRemoved': "added"}))
                    both_removed  = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': "removed"}), dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}),dict({'RobustnessAddedOrRemoved': "removed"}))
                    robustness_added_code_smell_removed = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': "removed"}) , dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}), dict({'RobustnessAddedOrRemoved': "added"}))
                    robustness_removed_code_smell_added = (dict({'Author': commit.author.name}), dict({'Committer Date': commit.committer_date}), dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), dict({'CodeSmellAddedOrRemoved': "added"}) , dict({'error_reporting': error_reporting}), dict({'state_recovery': state_recovery}), dict({'behavior_recovery': behavior_recovery}), dict({'RobustnessAddedOrRemoved': "removed"}))

                    if robustness_exception_handling and commits_with_code_smells_dict.get(file) is None:
                        if any_code_smell:
                            commits_with_code_smells_dict[file] = [both_added]
                        else:
                            commits_with_code_smells_dict[file] = [robustness]

                    elif any_code_smell and commits_with_code_smells_dict.get(file) is None:

                        if robustness_exception_handling:
                            commits_with_code_smells_dict[file] = [both_added]
                        else:
                            commits_with_code_smells_dict[file] = [code_smell]
                    
                    elif any_code_smell and commits_with_code_smells_dict.get(file) is not None:
                        
                        item = commits_with_code_smells_dict.get(file)[-1]

                        if item[2]['nested_try'] < nested_try or item[3]['unchecked_exception'] < unchecked_exception or item[4]['print_statement'] < print_statement or item[5]['return_code'] < return_code or item[6]['ignored_checked_exception'] < ignored_checked_exception:
                            if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                                commits_with_code_smells_dict[file].append(both_added) 

                        elif item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code']  > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception: 
                            if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                                commits_with_code_smells_dict[file].append(robustness_added_code_smell_removed)
                                
                        elif item[2]['nested_try'] < nested_try or item[3]['unchecked_exception'] < unchecked_exception or item[4]['print_statement'] < print_statement or item[5]['return_code'] < return_code or item[6]['ignored_checked_exception'] < ignored_checked_exception:
                                if item[8]['error_reporting'] > error_reporting or item[9]['state_recovery'] > state_recovery or item[10]['behavior_recovery'] > behavior_recovery:
                                    commits_with_code_smells_dict[file].append(robustness_removed_code_smell_added)
                                else:
                                    commits_with_code_smells_dict[file].append(code_smell)
                        
                        elif item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code'] > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception:      
                            commits_with_code_smells_dict[file].append(removed_code_smell)

                        elif robustness_exception_handling:
                            if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                                commits_with_code_smells_dict[file].append(robustness)
                            ##else:
                            ##    commits_with_code_smells_dict[modification.filename].append(removed_robustness)
                        
                    elif robustness_exception_handling and commits_with_code_smells_dict.get(file) is not None:
                        item = commits_with_code_smells_dict.get(file)[-1]
                        
                        if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                            commits_with_code_smells_dict[file].append(robustness)  

                        elif item[8]['error_reporting'] > error_reporting or item[9]['state_recovery'] > state_recovery or item[10]['behavior_recovery'] > behavior_recovery:
                            commits_with_code_smells_dict[file].append(removed_robustness) 

                        elif any_code_smell:
                            if item[2]['nested_try'] < nested_try or item[3]['unchecked_exception'] < unchecked_exception or item[4]['print_statement'] < print_statement or item[5]['return_code'] < return_code or item[6]['ignored_checked_exception'] < ignored_checked_exception:
                                commits_with_code_smells_dict[file].append(both_added)
                        
                            if item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code'] > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception:      
                                commits_with_code_smells_dict[file].append(both_removed)
                        
                    elif any_code_smell == False and commits_with_code_smells_dict.get(file) is not None:
                        
                        item = commits_with_code_smells_dict.get(file)[-1]

                        if item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code']  > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception: 
                            if item[8]['error_reporting'] > error_reporting or item[9]['state_recovery'] > state_recovery or item[10]['behavior_recovery'] > behavior_recovery:
                                commits_with_code_smells_dict[file].append(both_removed)
                            ##else
                            ##  commits_with_code_smells_dict[file].append(robustness_added_code_smell_removed)
                        elif item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code']  > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception:      
                            if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                                commits_with_code_smells_dict[file].append(robustness_added_code_smell_removed)
                        
                        elif robustness_exception_handling:
                            if item[8]['error_reporting'] < error_reporting or item[9]['state_recovery'] < state_recovery or item[10]['behavior_recovery'] < behavior_recovery:
                                commits_with_code_smells_dict[file].append(robustness)  
                        
                        elif item[8]['error_reporting'] > error_reporting or item[9]['state_recovery'] > state_recovery or item[10]['behavior_recovery'] > behavior_recovery:
                            commits_with_code_smells_dict[file].append(removed_robustness)
            else:
                with open("not_python_repo.txt", "a") as txt_file:
                    txt_file.write(f"{repo}\n")
                
                return

    except Exception as e:
        print(str(e))

    if is_python:
        print(f"Writing results for ... {repo}")
        x = repo.replace("/", "_")                  
        filename = f"/Users/bjergfelt/Desktop/Kandidat/pythoncommitsinadayongh_results_python_10_03_21_new_test/{x}_result.json"
        finaldict = dict({'repo': repo, 'total_commits': total_number_of_commits})
        finaldict.update(commits_with_code_smells_dict)
        with open(filename, "w") as json_file:
            json_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=str))
    else:
        with open("not_python_repo.txt", "a") as txt_file:
            txt_file.write(f"{repo}\n")

def check_if_python_project(repo):
    # using an access token
    g = Github("")
    is_python = False
    try:
        if g.get_rate_limit().search.remaining != 0:
            repository = g.get_repo(repo).get_languages()
            repositories = list(repository.keys())
            if len(repository) > 0:
                if 'C#' in repository:
                    with open("csharp_repo.txt", "a") as txt_file:
                            txt_file.write(f"{repo}\n")
                if len(repositories) > 1:
                    if repositories[0] == 'HTML' and repositories[1] == 'Python':
                        is_python = True 
                    else:
                        is_python = False
                    
                    if repositories[0] == 'Jupyter Notebook' and repositories[1] == 'Python':
                        is_python = True 
                    else:
                        is_python = False

                    if repositories[0] == 'JavaScript' and repositories[1] == 'Python':
                        is_python = True 
                    else:
                        is_python = False

                if repositories[0] == 'Python':
                    is_python = True   
                else:
                    is_python = False
            else:  
                is_python = False
        else: 
            print("Limit reached .. try another access token")
            sys.stdout.flush()
            sys.exit()

    except (Exception) as e:
        if '404' in str(e):
            print(f"Processing stopped because of '{str(e)}' the repository doesnt exist") 
            with open("not_python_repo.txt", "a") as txt_file:
                    txt_file.write(f"{repo}\n")
        if '403' in str(e):
            print(f"Processing stopped because of '{str(e)}' rate limit")
            sys.stdout.flush() 
            sys.exit()
    
    if is_python == False:    
        with open("not_python_repo.txt", "a") as txt_file:
                    txt_file.write(f"{repo}\n")
    
    return is_python 



not_python_repositories = []
not_python_repositories_set = set()

txt_file_exists = os.path.exists("not_python_repo.txt")
if txt_file_exists:
    with open("not_python_repo.txt","r") as txt_file:
        not_python_repositories_set = set(txt_file.read().splitlines())
            #not_python_repositories = txt_file.readlines()


def check_if_not_python_project(repo):
    ##new_line_repo = f"{repo}\n" 
    new_line_repo = f"{repo}"      
    if new_line_repo in not_python_repositories_set:
        return True  
    return False 

def check_if_result_is_present(key):           
    x = key.replace("/", "_")                  
    exists = os.path.isfile(f"pythoncommitsinadayongh_results_python_10_03_21_new_test/{x}_result.json")
    if exists:
        return True
    else: 
        return False

def process_item(repo):

    key = repo[0]
    value = repo[1]

    if "linux" in repo[0] or "Linux" in repo[0]:
        return ""

    if "AutoApiSecret" in repo[0] or "AutoApiS" in repo[0]:
        return ""    

    """
    if "dotnet" in key:
        print(f"{key} no dotnet")
        return ""
    """
    if len(value) == 0:
        return ""

    if check_if_result_is_present(key):
        return "result is already present"
    
    if len(value) > 100:
        return ""    

    if check_if_not_python_project(key):
        return ""
    
    if check_if_python_project(key) == True:
        python_in_a_day_on_gh(key, value)
        print(f"Done analysing ... {key}")
        return "key"
    else:
        return ""

if __name__ == '__main__':
    t0 = time.time()
    repo_with_commits = dict()
    for i in range(0, 24):
        try:
            with open(f"pythoncommitsinadayongh_10_03_21/hour_{i}_push_events.json") as json_file:
                data = json.load(json_file)
                for event in data:
                    if repo_with_commits.get(event['repo']['name']) is not None:
                        for commit in event['payload']['commits']:
                            
                            if commit['author']['name'] != "Github Actions" and commit['author']['name'] != "Upptime Bot" and commit['author']['name'] != "dotnet-maestro[bot]" and commit['author']['name'] != "dependabot[bot]" and "[bot]" not in commit['author']['name']:
                                repo_with_commits.get(event['repo']['name']).append(commit['sha'])
                            ##commit_sha_array.append(commit['sha'])
                    else:
                        sha_array = []
                        for commit in event['payload']['commits']:
                            if commit['author']['name'] != "Github Actions" and commit['author']['name'] != "Upptime Bot" and commit['author']['name'] != "dependabot[bot]" and "[bot]" not in commit['author']['name']:
                                sha_array.append(commit['sha'])       
                        if len(sha_array) > 0:
                            repo_dict = dict({event['repo']['name']: sha_array})
                            repo_with_commits.update(repo_dict)
                        
        except Exception as e:
            print(str(e))

    remaining_files_to_analyse = dict()

    print(f"Size of repo with commits is {len(repo_with_commits.items())}")

    ### pre analysis

    for item in repo_with_commits.items():
        if check_if_not_python_project(item[0]) == False and check_if_result_is_present(item[0]) == False:
            repo_dict = dict({item[0]: item[1]})
            remaining_files_to_analyse.update(repo_dict)

    print(f"{len(remaining_files_to_analyse)} repos remain")
    manager = Manager()
    d = manager.dict()
    d['repo_commits'] = remaining_files_to_analyse
##multiprocessing.cpu_count()
    with Pool(10) as p:
        p.map(process_item, d['repo_commits'].items())
        p.terminate()

    t1 = time.time()
    total = t1-t0   
    print(total)