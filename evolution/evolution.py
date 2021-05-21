import json
from pydriller import RepositoryMining
from multiprocessing import Pool
from helpers.exception_handler_helper import ExceptionHandlerHelper
from helpers.robustness_helper import RobustnessHelper
from exception_handling_patterns.exception_handler_patterns import ExceptionHandler
from helpers.loc_helper import LOCHelper
import os
from itertools import repeat


class Evolution:

    def __init__(self):
        pass

    def get_deleted_occurrences(self, modification, current_list):
        removed = []
        for file_diff_lineno_key, lineno in modification.diff_parsed.get("deleted"):
            for current_h in current_list:
                if current_h.lineno == file_diff_lineno_key:
                    # new_current_list.remove(current_h)
                    removed.append(current_h)
        return removed

    def get_added_occurrences(self, modification, incoming_occurrences):
        added = []
        for file_diff_lineno_key, lineno in modification.diff_parsed.get("added"):
            for current_h in incoming_occurrences:
                if current_h.lineno == file_diff_lineno_key:
                    added.append(current_h)
        return added

    def whole_evolution_with_try_except_tracking(self, repository, topic):
        print(f"Analysing repo ... {repository} in {topic}")
        commits_with_code_smells_dict = {}
        total_number_of_commits = 0
        try:
            for commit in RepositoryMining(f"https://github.com/{repository}.git",
                                           only_modifications_with_file_types=['.py']).traverse_commits():
                total_number_of_commits += 1

                for modification in commit.modifications:
                    if ".py" in str(modification.filename):
                        source_code = modification.source_code
                        ## can be _None_ if the file is added
                        if modification.old_path is None:
                            file_path = modification.new_path
                        else:
                            file_path = modification.old_path

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

                    # if not "zeeguu/model/user.py" in file:
                    #    continue
                    """
                    If none, the occurrence will be added as commits_with_code_smells_dict[file] = [code_smell]
                    """
                    if commits_with_code_smells_dict.get(file_path) is None:
                        for eh in try_excepts:
                            eh.author = commit.author.name
                            if eh.robustness_exception_handling:
                                eh.robustness_added_or_removed = "added"

                            if eh.any_exception_smell:
                                eh.exception_smell_added_or_removed = "added"

                        commits_with_code_smells_dict[file_path] = [dict(
                            {'date': str(commit.committer_date), 'exception_handlers': try_excepts})]
                        continue

                    if commits_with_code_smells_dict.get(file_path) is not None:
                        handler_changes = False

                        for eh in try_excepts:
                            eh.author = commit.author.name
                        incomings = []
                        current_exception_handlers = commits_with_code_smells_dict.get(file_path)[-1][
                            "exception_handlers"]

                        new_current_list_buffer = []

                        if len(try_excepts) > len(current_exception_handlers):
                            # del new_incoming_list[i]
                            # search for nearest "number"
                            # old_list_lines = [x.lineno for x in current_exception_handlers]
                            # new_list_lines = [x.lineno for x in new_incoming_list]
                            commits_with_code_smells_dict.get(file_path).append(dict(
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

                            commits_with_code_smells_dict.get(file_path).append(dict(
                                {'date': str(commit.committer_date),
                                 'exception_handlers': try_excepts,
                                 'removed': new_current_list_buffer}))
                            continue

                        for (current, incoming) in zip(current_exception_handlers,
                                                       try_excepts):
                            handler_changes, newest_change, = self.process_changes(current, handler_changes, incoming)

                            incomings.append(newest_change)

                        if handler_changes:
                            commits_with_code_smells_dict.get(file_path).append(dict(
                                {'date': str(commit.committer_date),
                                 'exception_handlers': incomings}))

        except Exception as e:
            print(e)

        repo_name = repository.replace("/", "_")
        path_to_results = f'topic_analysis_results/{topic}'
        if not os.path.exists(path_to_results):
            os.makedirs(path_to_results)
        filename = f"{path_to_results}/{repo_name}_result.json"
        finaldict = {'repo': repository, 'total_commits': total_number_of_commits}
        finaldict.update(commits_with_code_smells_dict)
        with open(filename, "w") as result_file:
            result_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=lambda x: x.__dict__))

    def process_changes(self, current, handler_changes, next):

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
        new_exception_smell_list = [next.exception_smell.nested_try,
                                    next.exception_smell.generic_exception,
                                    next.exception_smell.print_statement,
                                    next.exception_smell.exit_code,
                                    next.exception_smell.ignored_exception,
                                    next.exception_smell.raise_generic_exception,
                                    next.exception_smell.break_statement]
        new_robustness_list = [next.robustness.exception_type_is_not_generic,
                               next.robustness.raise_type_exception,
                               next.robustness.return_statement,
                               next.robustness.import_from,
                               next.robustness.state_recovery,
                               next.robustness.behavior_recovery]
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
            if len(next.changes) > 0:
                next.changes.extend(exception_smell_and_robustness_switched_in_between)
            else:
                next.changes = exception_smell_and_robustness_switched_in_between

        if exception_smell_switched is not None and current_exception_smell_list_sum == new_exception_smell_list_sum:
            if len(next.changes) > 0:
                next.changes.extend(exception_smell_switched)
            else:
                next.changes = exception_smell_switched

        if ExceptionHandlerHelper().check_if_exception_added(current_exception_smell_list,
                                                             new_exception_smell_list, current_exception_smell_list_sum
                , new_exception_smell_list_sum):
            next.exception_smell_added_or_removed = "added"

        if ExceptionHandlerHelper().check_if_exception_removed(current_exception_smell_list,
                                                               new_exception_smell_list,
                                                               current_exception_smell_list_sum
                , new_exception_smell_list_sum):
            next.exception_smell_added_or_removed = "removed"

        if robustness_switched is not None and current_robustness_list_sum == new_robustness_list_sum:
            if len(next.changes) > 0:
                next.changes.extend(robustness_switched)
            else:
                next.changes = robustness_switched

        if RobustnessHelper().check_if_robustness_added(current_robustness_list,
                                                        new_robustness_list, current_robustness_list_sum,
                                                        new_robustness_list_sum):
            next.robustness_added_or_removed = "added"
        if RobustnessHelper().check_if_robustness_removed(current_robustness_list,
                                                          new_robustness_list, current_robustness_list_sum,
                                                          new_robustness_list_sum):
            next.robustness_added_or_removed = "removed"

        if next.changes or next.exception_smell_added_or_removed or next.robustness_added_or_removed:
            handler_changes = True

        return handler_changes, next

    def check_if_result_is_present(self, key, topic):
        with open(f'python_repos_for_analysis/repos_for_{topic}.txt', 'r') as txt_file:
            if key in txt_file.read().splitlines():
                return True
            else:
                return False

    def whole_evolution_multiple_repositories(self, topic):
        with open(f'python_repos_for_analysis/{topic}.json') as json_file:
            repos = []
            data = json.load(json_file)
            for p in data:
                if self.check_if_result_is_present(p['repo'], topic):
                    repos.append(p['repo'])

        with Pool(4) as p:
            p.starmap(self.whole_evolution_with_try_except_tracking, zip(repos, repeat(topic)))
            p.terminate()

    def whole_evolution_with_loc(self, repository):
        print("Analysing repo ... {}".format(repository))
        total_lines_of_code = 0
        try:
            for commit in RepositoryMining(f"https://github.com/{repository}.git", order='reverse').traverse_commits():
                project_path = commit.project_path
                total_lines_of_code = LOCHelper().countlines(project_path)
                break
        except Exception as e:
            print(e)

        repo_name = repository.replace("/", "_")
        path_to_results = '/loc-results/Python_api/'
        filename = f"{path_to_results}/{repo_name}_result.json"
        finaldict = {'repo': repository, 'loc': total_lines_of_code}
        with open(filename, "w") as result_file:
            result_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=lambda x: x.__dict__))

    def whole_evolution_loc_multiple_repositories(self):
        with open('python_repos_for_analysis/Python_django.json') as json_file:
            repos = []
            data = json.load(json_file)
            for p in data:
                if self.check_if_result_is_present(p['repo']):
                    repos.append(p['repo'])

        with Pool(4) as p:
            p.map(self.whole_evolution_with_loc, repos)
            p.terminate()


""" 
if __name__ == '__main__':
    start_time = time.time()
   # Evolution().whole_evolution_with_try_except_tracking('alecthomas/flask_injector')
    Evolution().whole_evolution_multiple_repositories()
    end_time = time.time()
    print(end_time - start_time)
"""
