import itertools
import os
import json
import numpy as np
import statistics

from helpers.exception_handler_helper import ExceptionHandlerHelper
from helpers.robustness_helper import RobustnessHelper
from occurrence.exception_handler_occurrence import ExceptionHandlerOccurrence
from occurrence.exception_smell import ExceptionSmell
from occurrence.robustness import Robustness


class ResultExtraction:

    def __init__(self):
        pass

    def only_ignored_exceptions(self, exception_handlers):
        occurrences = 0
        for exception_handler in exception_handlers:
            smell = exception_handler["exception_smell"]
            if smell["ignored_exception"] > 0:
                """
                and smell["nested_try"] == 0 and smell["generic_exception"] > 0 \
                and smell["print_statement"] == 0 and smell["exit_code"] == 0 and smell["raise_generic_exception"] == 0:
                """
                occurrences += 1

        return occurrences

    def gini(self, array):
        """Calculate the Gini coefficient of a numpy array."""
        # All values are treated equally, arrays must be 1d:
        array = array.flatten()
        if np.amin(array) < 0:
            # Values cannot be negative:
            array -= np.amin(array)
        # Values cannot be 0:
        np.add(array, 0.0000001, out=array, casting="unsafe")
        # Values must be sorted:
        array = np.sort(array)
        # Index per array element:
        index = np.arange(1, array.shape[0] + 1)
        # Number of array elements:
        n = array.shape[0]
        # Gini coefficient:
        return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

    def calculate_gini_coefficient(self):
        exception_handlers_per_file = list()
        for root, dir, files in os.walk(""):

            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        if len(data.keys()) == 2:
                            exception_handlers_per_file.append(0)
                            continue

                        for key in data.keys():
                            if key == "repo" or key == "total_commits":
                                continue
                            if len(data.get(key)[0]["exception_handlers"]) > 0:
                                exception_handlers_per_file.append(1)
                                break

                except Exception as e:
                    print(str(e))

        list_for_gini = np.array(exception_handlers_per_file)

        print(self.gini(list_for_gini))
        print(f"total number of repos{len(list_for_gini)}")
        print(f"number of repos with: {np.count_nonzero(list_for_gini == 1)}")
        print(f"number of repos with no: {np.count_nonzero(list_for_gini == 0)}")

    def calculate_gini_coefficient_for_exception_smells(self, smell, type, path):
        exception_handlers_per_file = list()
        exception_handlers = 0
        for root, dir, files in os.walk(path):
            for file in files:
                total_generic = 0
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        if len(data.keys()) == 2:
                            continue

                        for key in data.keys():
                            if key == "repo" or key == "total_commits":
                                continue
                            last_commit_in_file = data.get(key)[-1]

                            for e in last_commit_in_file["exception_handlers"]:
                                if e[type][smell] > 0:
                                    exception_handlers_per_file.append(1)
                                else:
                                    exception_handlers_per_file.append(0)


                except Exception as e:
                    print(str(e))

        list_for_gini = np.array(exception_handlers_per_file)
        print(f"total exception handlers {exception_handlers}")
        print(self.gini(list_for_gini))
        print(f"total number of repos{len(list_for_gini)}")
        print(f"number of repos with: {np.count_nonzero(list_for_gini != 0)}")
        print(f"number of repos with no: {np.count_nonzero(list_for_gini == 0)}")

    def count_for_exception_smells(self, smell, type, path):
        for root, dir, files in os.walk(path):
            for file in files:
                total_generic = 0
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        if len(data.keys()) == 2:
                            continue

                        for key in data.keys():
                            if key == "repo" or key == "total_commits":
                                continue

                            last_commit_in_file = data.get(key)[-1]

                            for e in last_commit_in_file["exception_handlers"]:
                                if e[type][smell] > 0:
                                    total_generic += e[type][smell]


                except Exception as e:
                    print(str(e))

                repo = data.get("repo")
                repo_name = repo.replace("/", "_")
                path_to_results = ''
                filename = f"{path_to_results}/{repo_name}_result.json"
                finaldict = {'repo': repo, 'total_generic': total_generic}
                with open(filename, "w") as result_file:
                    result_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=lambda x: x.__dict__))

    def number_of_specific_exception_handlers(self,path):
        total_exception_handlers = 0
        total_commits = 0
        nested_try = 0
        generic_exception = 0
        print_statement = 0
        return_code = 0
        ignored_exception = 0
        error_reporting = 0
        state_recovery = 0
        behavior_recovery = 0
        exception_smell_added = 0
        exception_smell_removed = 0
        robustness_added = 0
        robustness_removed = 0
        removed = 0
        added = 0

        """
                :param exception_type_is_not_generic
                :param raise_type_exception:
                :param return_statement:
                :param error_reporting:
                :param state_recovery:
                :param behavior_recovery:
                """

        for root, dir, files in os.walk(path):

            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        for key in data.keys():
                            if key == "repo" or key == "total_commits":
                                continue
                            last_commit_in_file = data.get(key)[-1]
                            total_exception_handlers += len(last_commit_in_file["exception_handlers"])
                            for exception_handler in last_commit_in_file["exception_handlers"]:
                                smell = exception_handler["exception_smell"]
                                robustness = exception_handler["robustness"]
                                ## if smell["exit_code"] > 0:

                                if smell["print_statement"] > 0 and smell["nested_try"] == 0 and smell[
                                    "generic_exception"] == 0 and smell["exit_code"] == 0 and smell[
                                    "raise_generic_exception"] == 0 \
                                        and robustness["exception_type_is_not_generic"] > 0 and robustness[
                                    "raise_type_exception"] > 0 \
                                        and robustness["return_statement"] == 0 and robustness[
                                    "state_recovery"] == 0 and robustness[
                                    "behavior_recovery"] == 0 and robustness[
                                    "return_statement"] == 0:


                                # if smell["generic_exception"] > 0 and robustness["exception_type_is_not_generic"] > 0:
                                        

                                    ignored_exception += 1
                        total_commits += data["total_commits"]

                except Exception as e:
                    print(str(e))
        print(f"Total ignored exception {ignored_exception}")

    def current_state(self, path_to_files):
        total_number_of_exception_handlers = 0
        generic_pattern = 0
        total_exception_handlers = 0
        total_commits = 0
        nested_try = 0
        generic_exception = 0
        print_statement = 0
        return_code = 0
        ignored_exception = 0
        break_statement = 0
        error_reporting = 0
        state_recovery = 0
        behavior_recovery = 0
        import_from = 0
        exception_smell_added = 0
        exception_smell_removed = 0
        robustness_added = 0
        robustness_removed = 0
        removed = 0
        added = 0
        raise_type_exception = 0
        return_statement = 0
        raise_generic_exception = 0
        exception_type_is_not_generic = 0
        total_commits = 0

        for root, dir, files in os.walk(f"{path_to_files}"):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        total_commits += data.get("total_commits")
                        for key in data.keys():
                            if key == "repo" or key == "total_commits":
                                continue
                            last_commit_in_file = data.get(key)[-1]
                            total_exception_handlers += len(last_commit_in_file['exception_handlers'])
                            for exception_handler in last_commit_in_file['exception_handlers']:
                                if exception_handler["exception_smell"]["nested_try"] > 0:
                                    nested_try += exception_handler["exception_smell"]["nested_try"]
                                if exception_handler["exception_smell"]["generic_exception"] > 0:
                                    generic_exception += exception_handler["exception_smell"]["generic_exception"]
                                if exception_handler["exception_smell"]["print_statement"] > 0:
                                    print_statement += exception_handler["exception_smell"]["print_statement"]
                                if exception_handler["exception_smell"]["exit_code"] > 0:
                                    return_code += exception_handler["exception_smell"]["exit_code"]
                                if exception_handler["exception_smell"]["ignored_exception"] > 0:
                                    ignored_exception += exception_handler["exception_smell"]["ignored_exception"]
                                if exception_handler["exception_smell"]["raise_generic_exception"] > 0:
                                    raise_generic_exception += exception_handler["exception_smell"][
                                        "raise_generic_exception"]
                                if exception_handler["exception_smell"]["break_statement"] > 0:
                                    break_statement += exception_handler["exception_smell"]["break_statement"]

                                if exception_handler["robustness"]["exception_type_is_not_generic"] > 0:
                                    exception_type_is_not_generic += exception_handler["robustness"][
                                        "exception_type_is_not_generic"]
                                if exception_handler["robustness"]["raise_type_exception"] > 0:
                                    raise_type_exception += exception_handler["robustness"]["raise_type_exception"]
                                if exception_handler["robustness"]["return_statement"] > 0:
                                    return_statement += exception_handler["robustness"]["return_statement"]
                                if exception_handler["robustness"]["state_recovery"] > 0:
                                    state_recovery += exception_handler["robustness"]["state_recovery"]
                                if exception_handler["robustness"]["behavior_recovery"] > 0:
                                    behavior_recovery += exception_handler["robustness"]["behavior_recovery"]
                                if exception_handler["robustness"]["import_from"] > 0:
                                    import_from += exception_handler["robustness"]["import_from"]


                except Exception as e:
                    print(str(e))
        print(os.path.basename(os.path.normpath(path_to_files)))
        print("Nested try count: {}".format(nested_try))
        print("Generic_exception count: {}".format(generic_exception))
        print("Print statement count: {}".format(print_statement))
        print("Return code count: {}".format(return_code))
        print("ignored_exception count: {}".format(ignored_exception))
        print("raise_generic_exception count: {}".format(raise_generic_exception))
        print(f"break statement count: {break_statement}")
        print("exception_type_is_not_generic count: {}".format(exception_type_is_not_generic))
        print("raise_type_exception count: {}".format(raise_type_exception))
        print(f"import_from statement count: {import_from}")
        print("return_statement count: {}".format(return_statement))
        print("state_recovery count: {}".format(state_recovery))
        print("behavior_recovery count: {}".format(behavior_recovery))
        print(f"total commits: {total_commits}")
        print(f"total number of exception handlers {total_exception_handlers}")
        print('\n')

    def current_state_single_repository(self, repository):
        repo_name = repository.replace("/", "_")
        filename = f"{repo_name}_result.json"
        total_commits = 0
        nested_try = 0
        generic_exception = 0
        print_statement = 0
        return_code = 0
        ignored_exception = 0
        raise_generic_exception = 0
        error_reporting = 0
        state_recovery = 0
        behavior_recovery = 0
        exception_smell_added = 0
        exception_smell_removed = 0
        robustness_added = 0
        robustness_removed = 0

        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for key in data.keys():
                    if key == "repo" or key == "total_commits":
                        continue
                    last_commit_in_file = data.get(key)[-1]

                    if last_commit_in_file["exception_smell_added_or_removed"] == "added":
                        exception_smell_added += 1
                        if last_commit_in_file["nested_try"] > 0:
                            nested_try += last_commit_in_file["nested_try"]
                        if last_commit_in_file["generic_exception"] > 0:
                            generic_exception += last_commit_in_file["generic_exception"]
                        if last_commit_in_file["print_statement"] > 0:
                            print_statement += last_commit_in_file["print_statement"]
                        if last_commit_in_file["return_code"] > 0:
                            return_code += last_commit_in_file["return_code"]
                        if last_commit_in_file["ignored_exception"] > 0:
                            ignored_exception += last_commit_in_file["ignored_exception"]
                        if last_commit_in_file["raise_generic_exception"] > 0:
                            raise_generic_exception += last_commit_in_file["raise_generic_exception"]

                    if last_commit_in_file["exception_smell_added_or_removed"] == "removed":
                        exception_smell_removed += 1
                    if last_commit_in_file["robustness_added_or_removed"] == "added":
                        robustness_added += 1
                        if last_commit_in_file["error_reporting"] > 0:
                            error_reporting += last_commit_in_file["error_reporting"]
                        if last_commit_in_file["state_recovery"] > 0:
                            state_recovery += last_commit_in_file["state_recovery"]
                        if last_commit_in_file["behavior_recovery"] > 0:
                            behavior_recovery += last_commit_in_file["behavior_recovery"]
                    if last_commit_in_file["robustness_added_or_removed"] == "removed":
                        robustness_removed += 1

                total_commits += data["total_commits"]

        except Exception as e:
            print(str(e))
        print(f"Total commits: {total_commits}")
        print("Nested try count: {}".format(nested_try))
        print("Generic_exception count: {}".format(generic_exception))
        print("Print statement count: {}".format(print_statement))
        print("Return code count: {}".format(return_code))
        print("ignored_exception count: {}".format(ignored_exception))
        print("raise_generic_exception count: {}".format(raise_generic_exception))
        print("error_reporting count: {}".format(error_reporting))
        print("state_recovery count: {}".format(state_recovery))
        print("behavior_recovery count: {}".format(behavior_recovery))
        print("exception_smell_added count: {}".format(exception_smell_added))
        print("exception_smell_removed count: {}".format(exception_smell_removed))
        print("robustness_added count: {}".format(robustness_added))
        print("robustness_removed count: {}".format(robustness_removed))

    def get_loc(self, path):
        lines_of_code = []
        for root, dir, files in os.walk(path):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        for key, value in data.items():
                            if 'loc' in key:
                                lines_of_code.append(value)
                except Exception as e:
                    print(str(e))

        lines_of_code = [x for x in lines_of_code if x != 0]
        print(f"Median loc {statistics.median(lines_of_code)}")
        # print(f"Max loc {max(lines_of_code)}")
        # print(f"Min loc {min(lines_of_code)}")

    def get_gini_dist_confirm(self, path):
        generic = []
        for root, dir, files in os.walk(path):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path) as json_file:
                        data = json.load(json_file)
                        for key, value in data.items():
                            if 'total_generic' in key:
                               if value > 0:
                                    generic.append(value)
                except Exception as e:
                    print(str(e))

        print(f"total repos {len(files)}")
        print(f"Average loc {len(generic)}")
        print(sorted(generic))

