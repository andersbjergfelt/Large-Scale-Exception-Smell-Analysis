from logging import exception
from occurrence import Occurrence
from exception_patterns import ExceptionPatterns
import ast
import json
from pydriller import RepositoryMining
import time
from multiprocessing import Pool 
from os import path
import traceback


def is_try(node):
    return isinstance(node, ast.Try)

"""
G0 (you know an exception has been raised; Code Smell
the component has handled it in some undefined way;
and the application is in error and may or may not terminate.)
Also known as Dummy Handler
"""
def check_for_nested_try(node):
    if is_try(node):
        return True


def check_for_generic_exception(node):
    if isinstance(node, ast.ExceptHandler):
        if isinstance(node.type, ast.Name):
            if node.type.id == "" or node.type.id == "Exception" or node.type is None:
                return True
    

def check_for_ignored_checked_exception(node,body):
    if isinstance(node, ast.Pass) and len(body) == 1:
        return True    


def check_for_print_statement(node, body):
    ## node.body should be equal to 1 because we want to know whether the print statement is the only statement. == dummy handler
    if isinstance(node, ast.Expr) and len(body) == 1:
        if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "print" or node.value.func.id == "Log" or node.value.func.id == "log":
                return True


def check_for_return_code_code_smell(node, body):
    if not isinstance(node, ast.Expr):
        return False
    if isinstance(node, ast.Expr) and len(body) == 1:
        if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "exit" or node.value.func.id == "sys.exit":
                    return True
    if isinstance(node, ast.Expr) and len(body) == 2:
        if isinstance(node.value.func, ast.Name):
            if body[0].value.func.id == "exit" or node.value.func.id == "sys":
                if  body[1].value.func.id == "print" or node.value.func.id == "log":
                        return True
            elif body[1].value.func.id == "exit" or node.value.func.id == "sys":
                if body[0].value.func.id == "print" or node.value.func.id == "log":
                    return True      
    ### edge case if len(body) > 3. "exit" is still defined as a code smell. 
    if isinstance(node, ast.Expr) and len(body) > 3:
        for b in body:
            if isinstance(b.value.func, ast.Name):
                if b.value.func.id == "exit":
                    return True
    return False            


"""
G1 (‘‘error-reporting”) -> reporting an error means throwing an exception; 
for a component at the system boundary, 
the exception may be transcribed into an equivalent message
* Replace error code with exception
* Replace ignored checked exception with unchecked exception 
* Avoid unexpected termination with big outer try block - is this a thing in Python?
* Replace dummy handler with rethrow
"""

def check_for_dummy_handler_with_retrow(node):
    if isinstance(node, ast.Raise):
        return True

def check_for_exception(node):
    if isinstance(node, ast.ExceptHandler):
        if isinstance(node.type, ast.Name):
            if node.type.id != "Exception":
                return True

"""
G2 (‘‘state-recovery”) -> faulting component maintains a correct state to continue running 
and propagates an exception to indicate its failure.
Look for Assign in AST
"""
def find_G2(node):
    if isinstance(node, ast.Assign):
        return True

"""
G3 (‘‘behavior-recovery”) -> After the faulting component finishes handling the exception, 
the application delivers the requested service and continues to run normally retry
"""
"""
If there is a while loop or for loop we must interpret that as recovery. 
"""
def find_G3(node):
    if isinstance(node, ast.For) or isinstance(node, ast.While):
        return True
    
    if is_try(node) == True:
        for b in node.handlers:
            if isinstance(b, ast.For) or isinstance(b, ast.While):
                return True


def get_exception_handling_evolution(source_code):
    nested_try = 0
    unchecked_exception = 0
    print_statement = 0
    return_code = 0
    ignored_checked_exception = 0
    any_code_smell = False
    error_reporting = 0
    state_recovery = 0
    behavior_recovery = 0
    robustness_exception_handling = False
    try:
        if not source_code:
            return (nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, any_code_smell, error_reporting, state_recovery, behavior_recovery, robustness_exception_handling) 
        user_ast = ast.parse(source_code)
        for a in ast.walk(user_ast):
            if is_try(a) == True:
                for d in a.body:
                    if check_for_nested_try(d):
                        nested_try += 1  
                        any_code_smell = True

                for b in a.handlers:
                    if check_for_exception(b):
                        error_reporting += 1
                        robustness_exception_handling = True
                       
                    if check_for_generic_exception(b):
                        unchecked_exception += 1 
                        any_code_smell = True
                         
                for c in b.body:
                    if check_for_dummy_handler_with_retrow(c):
                        error_reporting += 1
                        robustness_exception_handling = True
                        
                    if check_for_ignored_checked_exception(c,b.body):
                        ignored_checked_exception += 1
                        any_code_smell = True
                        
                    if find_G2(c):
                        state_recovery += 1
                        robustness_exception_handling = True
                        
                    if find_G3(c):
                        behavior_recovery += 1
                        robustness_exception_handling = True

                    if check_for_print_statement(c, b.body):
                        print_statement += 1
                        any_code_smell = True
                        
                    if check_for_return_code_code_smell(c, b.body):
                        return_code += 1
                        any_code_smell = True
                                              
    except Exception as e:
        pass

    return (nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, any_code_smell, error_reporting, state_recovery, behavior_recovery, robustness_exception_handling) 

def check_if_exception_smell_switched(current_exception_smell_list, new_exception_smell_list):
    switched_exception_smells = []   
    exception_smell_switch = dict()
    for i in range(0, len(current_exception_smell_list) - 1):
       
        if (current_exception_smell_list[i] != new_exception_smell_list[i]):
            if(i == 0):
                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_switch['to'] = "nested try"
                else:
                     exception_smell_switch['from'] = "nested try"  
            if(i == 1):
                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_switch['to'] = "unchecked exception"
                else:
                     exception_smell_switch['from'] = "unchecked exception"   
            if(i == 2):
                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_switch['to'] = "print statement"
                else:
                     exception_smell_switch['from'] = "print statement"    
            if(i == 3):
                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_switch['to'] = "return code"
                else:
                     exception_smell_switch['from'] = "return code"         
            if(i == 4):
                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_switch['to'] = "ignored checked exception"
                else:
                     exception_smell_switch['from'] = "ignored checked exception"    
    
    if exception_smell_switch:
        switched_exception_smells.append(exception_smell_switch)   
    
    if len(switched_exception_smells) > 0:
        return switched_exception_smells            

    return None                
                    

def whole_evolution(repo):
    print("Analysing repo ... {}".format(repo))
    commits_with_code_smells_dict = dict()
    total_number_of_commits = 0

    try:
        for commit in RepositoryMining(f"https://github.com/{repo}.git").traverse_commits():
            total_number_of_commits += 1
                    
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
                
                if commits_with_code_smells_dict.get(file) is None:
                    if robustness_exception_handling:
                        if any_code_smell:
                            both_added = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "added", [])
                            commits_with_code_smells_dict[file] = [both_added]
                        else:
                            robustness = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "added", [])
                            commits_with_code_smells_dict[file] = [robustness]
                    elif any_code_smell:
                        code_smell = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "", [])
                        commits_with_code_smells_dict[file] = [code_smell]
                
                if commits_with_code_smells_dict.get(file) is not None:
                    current_occurrence = commits_with_code_smells_dict.get(file)[-1]
                    current_nested_try = current_occurrence.nested_try
                    current_unchecked_exception = current_occurrence.unchecked_exception
                    current_print_statement = current_occurrence.print_statement
                    current_return_code = current_occurrence.return_code
                    current_ignored_checked_exception = current_occurrence.ignored_checked_exception
                    current_error_reporting = current_occurrence.error_reporting
                    current_state_recovery = current_occurrence.state_recovery
                    current_behavior_recovery = current_occurrence.behavior_recovery
                    current_exception_smell_list = [current_nested_try, current_unchecked_exception, current_print_statement, current_return_code, current_ignored_checked_exception]
                    current_exception_smell_list_sum = sum(current_exception_smell_list)
                    current_robustness = [current_error_reporting, current_state_recovery, current_behavior_recovery]
                    current_robustness_sum = sum(current_robustness)

                    new_exception_smell_list = [nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception]
                    new_exception_smell_list_sum = sum(new_exception_smell_list)
                    new_robustness = [error_reporting, state_recovery, behavior_recovery]
                    new_robustness_sum = sum(new_robustness)

                    if any_code_smell == True and robustness_exception_handling == False:
                        if current_exception_smell_list_sum > new_exception_smell_list_sum: 
                            removed_code_smell = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "removed", error_reporting, state_recovery,  behavior_recovery, "", [])
                            commits_with_code_smells_dict[file].append(removed_code_smell)

                        if (current_exception_smell_list_sum > 0 and new_exception_smell_list_sum > 0) and current_exception_smell_list_sum == new_exception_smell_list_sum:
                            if check_if_exception_smell_switched(current_exception_smell_list, new_exception_smell_list) is not None:
                                changes = check_if_exception_smell_switched(current_exception_smell_list, new_exception_smell_list)
                                exception_smell_switch = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "", changes)
                                commits_with_code_smells_dict[file].append(exception_smell_switch)
                        
                        if current_exception_smell_list_sum < new_exception_smell_list_sum:
                            if current_robustness_sum > 0 and new_robustness_sum == 0:
                                robustness_removed_code_smell_added = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "removed", [])
                                commits_with_code_smells_dict[file].append(robustness_removed_code_smell_added)
                            else:
                                code_smell = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "", [])
                                commits_with_code_smells_dict[file].append(code_smell)

                    if robustness_exception_handling == True and any_code_smell == False:
                        if current_robustness_sum < new_robustness_sum:
                            if current_exception_smell_list_sum > 0 and new_exception_smell_list_sum == 0:
                                robustness_added_code_smell_removed = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "removed", error_reporting, state_recovery,  behavior_recovery, "added", [])
                                commits_with_code_smells_dict[file].append(robustness_added_code_smell_removed)
                            else:
                                robustness = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "added", [])
                                commits_with_code_smells_dict[file].append(robustness)     

                        if current_robustness_sum > new_robustness_sum:
                            removed_robustness = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "removed", [])
                            commits_with_code_smells_dict[file].append(removed_robustness) 

                    if any_code_smell == False and robustness_exception_handling == False:
                        if (new_robustness_sum + new_exception_smell_list_sum) == 0 and (current_exception_smell_list_sum > 0 and current_robustness_sum > 0):
                            both_removed = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "removed", error_reporting, state_recovery,  behavior_recovery, "removed", [])
                            commits_with_code_smells_dict[file].append(both_removed)

                        if (new_robustness_sum + new_exception_smell_list_sum) == 0 and (current_exception_smell_list_sum > 0):
                                removed_code_smell = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "removed", error_reporting, state_recovery,  behavior_recovery, "", [])
                                commits_with_code_smells_dict[file].append(removed_code_smell)

                        elif (new_robustness_sum + new_exception_smell_list_sum) == 0 and (current_robustness_sum > 0):
                            removed_robustness = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "removed", [])
                            commits_with_code_smells_dict[file].append(removed_robustness)

                    if any_code_smell == True and robustness_exception_handling == True:
                        if ((new_exception_smell_list_sum > current_exception_smell_list_sum) and (new_robustness_sum > current_robustness_sum)):
                            both_added = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "added", [])
                            commits_with_code_smells_dict[file].append(both_added)
                            continue

                        if ((new_exception_smell_list_sum == current_exception_smell_list_sum) and (new_robustness_sum > current_robustness_sum)):
                            robustness = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "", error_reporting, state_recovery,  behavior_recovery, "added", [])
                            commits_with_code_smells_dict[file].append(robustness)
                            continue

                        if ((new_exception_smell_list_sum > current_exception_smell_list_sum) and (new_robustness_sum == current_robustness_sum)):
                            code_smell = Occurrence(commit.author.name, commit.committer_date, nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, "added", error_reporting, state_recovery,  behavior_recovery, "", [])
                            commits_with_code_smells_dict[file].append(code_smell)
                            continue
 

    except Exception as e:
        print(str(e))

    x = repo.replace("/", "_")                  
    filename = f"/Users/bjergfelt/Desktop/Kandidat/new/Python_api_topic_python/{x}_result.json"
    finaldict = dict({'repo': repo, 'total_commits': total_number_of_commits})
    finaldict.update(commits_with_code_smells_dict)
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(finaldict, indent=4, sort_keys=False, default=lambda x: x.__dict__))


t0 = time.time()
for repo in set(
        [
            "zeeguu-ecosystem/Zeeguu-Core"
        ]
    ):
    whole_evolution(repo)
t1 = time.time()
total = t1-t0   
print(total)

"""
if __name__ == '__main__':
    t0 = time.time()
    with open('') as json_file:
        repos = []
        data = json.load(json_file)
        for p in data:
            repos.append(p['repo'])
  
        with Pool(1) as p:
            p.map(whole_evolution, repos)
            p.terminate()

    t1 = time.time()
    total = t1-t0   
    print(total)
"""