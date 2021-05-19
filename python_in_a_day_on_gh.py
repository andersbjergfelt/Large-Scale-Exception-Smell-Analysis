import multiprocessing
import sys
import os
import json
from pydriller import RepositoryMining
import time
from multiprocessing import Pool
from multiprocessing import Manager
import os.path
from github import Github
from helpers.exception_handler_helper import ExceptionHandlerHelper
from helpers.robustness_helper import RobustnessHelper
from exception_handling_patterns.exception_handler_patterns import ExceptionHandler


def process_changes(current, handler_changes, new):
    current_exception_smell_list = [current.exception_smell.nested_try,
                                    current.exception_smell.generic_exception,
                                    current.exception_smell.print_statement,
                                    current.exception_smell.exit_code,
                                    current.exception_smell.ignored_exception,
                                    current.exception_smell.raise_generic_exception,
                                    current.exception_smell.break_statement]
    current_robustness_list = [current.robustness.exception_type_is_not_generic,
                               current.robustness.raise_type_exception,
                               current.robustness.return_statement,
                               current.robustness.import_from,
                               current.robustness.state_recovery,
                               current.robustness.behavior_recovery]
    new_exception_smell_list = [new.exception_smell.nested_try,
                                new.exception_smell.generic_exception,
                                new.exception_smell.print_statement,
                                new.exception_smell.exit_code,
                                new.exception_smell.ignored_exception,
                                new.exception_smell.raise_generic_exception,
                                new.exception_smell.break_statement]
    new_robustness_list = [new.robustness.exception_type_is_not_generic,
                           new.robustness.raise_type_exception,
                           new.robustness.return_statement,
                           new.robustness.import_from,
                           new.robustness.state_recovery,
                           new.robustness.behavior_recovery]
    exception_smell_switched = ExceptionHandlerHelper().check_if_exception_smell_switched(
        current_exception_smell_list,
        new_exception_smell_list)
    robustness_switched = RobustnessHelper().check_if_robustness_switched(
        current_robustness_list,
        new_robustness_list)

    exception_smell_and_robustness_switched_in_between = \
        ExceptionHandlerHelper().check_if_switched_exception_smell_robustness(current_exception_smell_list,
                                                                              new_exception_smell_list,
                                                                              current_robustness_list,
                                                                              new_robustness_list)
    current_exception_smell_list_sum = sum(current_exception_smell_list)
    new_exception_smell_list_sum = sum(new_exception_smell_list)
    current_robustness_list_sum = sum(current_robustness_list)
    new_robustness_list_sum = sum(new_robustness_list)

    if exception_smell_and_robustness_switched_in_between is not None \
            and (current_exception_smell_list_sum \
            == new_exception_smell_list_sum and current_robustness_list_sum == new_robustness_list_sum):
        if len(new.changes) > 0:
            new.changes.extend(exception_smell_and_robustness_switched_in_between)
        else:
            new.changes = exception_smell_and_robustness_switched_in_between

    if exception_smell_switched is not None and current_exception_smell_list_sum == new_exception_smell_list_sum:
        if len(new.changes) > 0:
            new.changes.extend(exception_smell_switched)
        else:
            new.changes = exception_smell_switched

    if ExceptionHandlerHelper().check_if_exception_added(current_exception_smell_list,
                                                         new_exception_smell_list, current_exception_smell_list_sum
            , new_exception_smell_list_sum):
        new.exception_smell_added_or_removed = "added"

    if ExceptionHandlerHelper().check_if_exception_removed(current_exception_smell_list,
                                                           new_exception_smell_list, current_exception_smell_list_sum
            , new_exception_smell_list_sum):
        new.exception_smell_added_or_removed = "removed"

    if robustness_switched is not None and current_robustness_list_sum == new_robustness_list_sum:
        if len(new.changes) > 0:
            new.changes.extend(robustness_switched)
        else:
            new.changes = robustness_switched

    if RobustnessHelper().check_if_robustness_added(current_robustness_list,
                                                    new_robustness_list, current_robustness_list_sum,
                                                    new_robustness_list_sum):
        new.robustness_added_or_removed = "added"
    if RobustnessHelper().check_if_robustness_removed(current_robustness_list,
                                                      new_robustness_list, current_robustness_list_sum,
                                                      new_robustness_list_sum):
        new.robustness_added_or_removed = "removed"

    if new.changes or new.exception_smell_added_or_removed or new.robustness_added_or_removed:
        handler_changes = True

    return handler_changes, new


def python_in_a_day_on_gh(repo, repo_commits):
    commits_with_code_smells_dict = dict()
    total_number_of_commits = len(repo_commits)

    try:
        for commit in RepositoryMining(f"https://github.com/{repo}.git", only_commits=repo_commits).traverse_commits():
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
            total_number_of_commits += 1

            for modification in commit.modifications:

                if modification.old_path is None:
                    file_path = modification.new_path
                else:
                    file_path = modification.old_path

                if ".py" in str(modification.filename):
                    source_code = modification.source_code
                    file = file_path
                else:
                    continue

                try_excepts = ExceptionHandler().find_exception_handler_patterns(source_code, commit)
                """

                try:
                    a = ast.parse(source_code)
                except SyntaxError as e:
                    continue
                except ValueError as e:
                    continue

                v = TryVisitor()
                v.visit(a)
                """
                if try_excepts is None:
                    continue

                if len(try_excepts) == 0:
                    continue

                if commits_with_code_smells_dict.get(file) is None:
                    for eh in try_excepts:
                        eh.author = commit.author.name
                        if eh.robustness_exception_handling:
                            eh.robustness_added_or_removed = "added"

                        if eh.any_exception_smell:
                            eh.exception_smell_added_or_removed = "added"

                    commits_with_code_smells_dict[file] = [dict(
                        {'date': str(commit.committer_date), 'exception_handlers': try_excepts})]
                    continue

                if commits_with_code_smells_dict.get(file) is not None:
                    handler_changes = False

                    for eh in try_excepts:
                        eh.author = commit.author.name
                    new_incoming = []
                    current_exception_handlers = commits_with_code_smells_dict.get(file)[-1]["exception_handlers"]

                    new_current_list_buffer = []

                    if len(try_excepts) > len(current_exception_handlers):
                        # del new_incoming_list[i]
                        # search for nearest "number"
                        # old_list_lines = [x.lineno for x in current_exception_handlers]
                        # new_list_lines = [x.lineno for x in new_incoming_list]
                        commits_with_code_smells_dict.get(file).append(dict(
                            {'date': str(commit.committer_date),
                             'exception_handlers': try_excepts}))

                        continue

                        """
                        for file_diff_lineno_key, lineno in modification.diff_parsed.get("added"):
                            for i, current_h in enumerate(new_incoming_list):
                                if current_h.lineno == file_diff_lineno_key:
                                    new_incoming_list_buffer.append(current_h)
                        """
                        """
                        for i, new_change in enumerate(new_incoming_list):

                            for old_change in current_exception_handlers:

                                closest_number = old_list_lines[
                                    min(range(len(old_list_lines)), key=lambda i: abs(
                                        old_list_lines[i] - new_change.lineno))]

                                if old_change.lineno == closest_number:
                                    handler_changes, newest_change, = self.process_changes(old_change,
                                                                                           handler_changes,
                                                                                           new_change)
                                    for i in range(len(new_incoming_list)):
                                        if new_incoming_list[i].lineno == newest_change.lineno:
                                            new_incoming_list[i] = newest_change
                                            continue
                        """

                    if len(try_excepts) < len(current_exception_handlers):
                        for file_diff_lineno_key, lineno in modification.diff_parsed.get("deleted"):
                            for current_hnew in current_exception_handlers:
                                if current_hnew.lineno == file_diff_lineno_key:
                                    new_current_list_buffer.append(current_hnew)

                        commits_with_code_smells_dict.get(file).append(dict(
                            {'date': str(commit.committer_date),
                             'exception_handlers': try_excepts,
                             'removed': new_current_list_buffer}))
                        continue

                    for (current, incoming) in zip(current_exception_handlers,
                                                   try_excepts):
                        handler_changes, newest_change, = process_changes(current, handler_changes, incoming)

                        new_incoming.append(newest_change)

                    if handler_changes:
                        commits_with_code_smells_dict.get(file).append(dict(
                            {'date': str(commit.committer_date),
                             'exception_handlers': new_incoming}))

    except Exception as ex:
        print(str(ex))

    # print(f"Writing results for ... {repo}")
    x = repo.replace("/", "_")
    filename = f"/pythoncommitsinadayongh/{x}_result.json"
    finaldict = dict({'repo': repo, 'total_commits': total_number_of_commits})
    finaldict.update(commits_with_code_smells_dict)
    with open(filename, "w") as result_file:
        result_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=lambda z: z.__dict__))


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
    with open("not_python_repo.txt", "r") as txt_file:
        not_python_repositories_set = set(txt_file.read().splitlines())
        # not_python_repositories = txt_file.readlines()


def check_if_not_python_project(repo):
    ##new_line_repo = f"{repo}\n" 
    new_line_repo = f"{repo}"
    if new_line_repo in not_python_repositories_set:
        return True
    return False


def check_if_result_is_present(key):
    x = key.replace("/", "_")
    exists = os.path.isfile(
        f"/pythoncommitsinadayongh_results_python_10_03_21_new_test/{x}_result.json")
    if exists:
        return True
    else:
        return False

def already_processed(key):
    x = key.replace("/", "_")
    exists = os.path.isfile(
        f"pythoncommitsinadayongh/{x}_result.json")
    if exists:
        return True
    else:
        return False


"""
    if "dotnet" in key:
        print(f"{key} no dotnet")
        return ""
"""
"""
def process_item(repo):
    key = repo[0]
    value = repo[1]

    if "linux" in repo[0] or "Linux" in repo[0]:
        return ""

    if "AutoApiSecret" in repo[0] or "AutoApiS" in repo[0]:
        return ""

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
"""


def process_item(repo):
    key = repo[0]
    value = repo[1]
    python_in_a_day_on_gh(key, value)
    print(f"Done analysing ... {key}")

def process_items(repo):
    key = repo[0]
    value = repo[1]
    python_in_a_day_on_gh(key, value)
    print(f"Done analysing ... {key}")


if __name__ == '__main__':
    t0 = time.time()
    repo_with_commits = dict()
    for i in range(0, 24):
        try:
            with open(
                    f"pythoncommitsinadayongh_10_03_21/hour_{i}_push_events.json") as json_file:
                data = json.load(json_file)
                for event in data:
                    if repo_with_commits.get(event['repo']['name']) is not None:
                        for commit in event['payload']['commits']:

                            if commit['author']['name'] != "Github Actions" and commit['author'][
                                'name'] != "Upptime Bot" and commit['author']['name'] != "dotnet-maestro[bot]" and \
                                    commit['author']['name'] != "dependabot[bot]" and "[bot]" not in commit['author'][
                                'name']:
                                repo_with_commits.get(event['repo']['name']).append(commit['sha'])
                            ##commit_sha_array.append(commit['sha'])
                    else:
                        sha_array = []
                        for commit in event['payload']['commits']:
                            if commit['author']['name'] != "Github Actions" and commit['author'][
                                'name'] != "Upptime Bot" and commit['author'][
                                'name'] != "dependabot[bot]" and "[bot]" not in commit['author']['name']:
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
        ## if check_if_not_python_project(item[0]) is False and check_if_result_is_present(item[0]) is False:
        if check_if_result_is_present(item[0]):
            repo_dict = dict({item[0]: item[1]})
            remaining_files_to_analyse.update(repo_dict)

    print(f"{len(remaining_files_to_analyse)} repos remain")
    manager = Manager()
    d = manager.dict()
    d['repo_commits'] = remaining_files_to_analyse

    # for repo in d['repo_commits'].items():
    #    process_items(repo)

    with Pool(3) as p:
        p.map(process_item, d['repo_commits'].items())
        p.terminate()

    t1 = time.time()
    total = t1 - t0
    print(total)
