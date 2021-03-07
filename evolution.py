import sys
import os
import ast
import json
from typing import Counter
from git import repo
from pydriller import RepositoryMining, git_repository
from pydriller import GitRepository
import time

REPO_DIR = ''

gitrepository = GitRepository(REPO_DIR)


def is_try(node):
        return hasattr(ast, "Try") and isinstance(node, ast.Try) or \
               hasattr(ast, "TryExcept") and isinstance(node, ast.TryExcept) or \
               hasattr(ast, "TryFinally") and isinstance(node, ast.TryFinally)

def check_for_nested_try(node):
    if is_try(node):
        return True

def check_for_unchecked_exception(node):
    if node.type.id == None or node.type.id == "":
        return True

def check_for_ignored_checked_exception(node):
    if node == isinstance(node, ast.Pass):
        return True    

def check_for_print_statement(node, body):
    ## node.body should be equal to 1 because we want to know whether the print statement is the only statement. == dummy handler
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 1:
        if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "print" or node.value.func.id == "Log" or node.value.func.id == "log":
                return True

def check_for_return_code_code_smell(node, body):
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 1:
         if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "exit" or node.value.func.id == "sys.exit":
                    return True
    elif hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 2:
        if isinstance(node.value.func, ast.Name):
            if body[0].value.func.id == "exit" or node.value.func.id == "sys":
                if  body[1].value.func.id == "print" or node.value.func.id == "log":
                        return True
            elif body[1].value.func.id == "exit" or node.value.func.id == "sys":
                if body[0].value.func.id == "print" or node.value.func.id == "log":
                    return True      
    ### edge case if len(body) > 3. "exit" is still defined as a code smell. 
    if len(body) > 3:
        for b in body:
            if b.value.func.id == "exit":
                return True
    return False            

def check_for_exception(node):
    if node.type.id != None:
        print("G1 - Checked exception")
    return True

def check_for_dummy_handler_with_retrow(node):
    if hasattr(ast, "Raise") == isinstance(node, ast.Raise):
        print("G1 - rethrow exception")
        return True

"""
G0 (you know an exception has been raised; Code Smell
the component has handled it in some undefined way;
and the application is in error and may or may not terminate.)
Also known as Dummy Handler
"""
def find_code_smells(node, body):
    if check_for_print_statement(node, body):
        return True
    if check_for_return_code_code_smell(node, body):
        return True
    if check_for_ignored_checked_exception(node):
        return True

"""
G1 (‘‘error-reporting”) -> reporting an error means throwing an exception; 
for a component at the system boundary, 
the exception may be transcribed into an equivalent message
* Replace error code with exception
* Replace ignored checked exception with unchecked exception 
* Avoid unexpected termination with big outer try block - is this a thing in Python?
* Replace dummy handler with rethrow
"""
def find_G1(node):
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr):
        if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "print" or node.value.func.id == "log":
                print("G1 - error reporting")
                return True
    if hasattr(ast, "Return") == isinstance(node, ast.Return):
        print("G1 - error reporting")
        return True


"""
G2 (‘‘state-recovery”) -> faulting component maintains a correct state to continue running 
and propagates an exception to indicate its failure.
Look for Assign in AST
"""
def find_G2(node):
    if hasattr(ast, "Assign") == isinstance(node, ast.Assign):
        print("G2 - state recovery")
        return True

"""
G3 (‘‘behavior-recovery”) -> After the faulting component finishes handling the exception, 
the application delivers the requested service and continues to run normally retry
"""
"""
If there is a while loop or for loop we must interpret that as recovery. 
"""
def find_G3(node):
    if hasattr(ast, "For") == isinstance(node, ast.For) or hasattr(ast, "While") == isinstance(node, ast.While):
        print("G3 - behavior-recovery")
        return True
    
    if is_try(node) == True:
        for b in node.handlers:
            if hasattr(ast, "For") == isinstance(node, ast.For) or hasattr(ast, "While") == isinstance(node, ast.While):
                print("G3 - behavior-recovery")
                return True


def get_G1_evolution(gitrepository):
    numberOfCodeSmells = 0
    numberOfG1 = 0
    numberOfG2 = 0
    numberOfG3 = 0
    for file in gitrepository.files():
        try:
            if ".py" in str(file):
                f = open(file)
                user_ast = ast.parse(f.read())
                for a in ast.walk(user_ast):
                    if is_try(a) == True:
                        for b in a.handlers:
                            if check_for_exception(b):
                                numberOfG1 += 1
                            for c in b.body:
                                if check_for_dummy_handler_with_retrow(c):
                                     numberOfG1 += 1
        except Exception as e:
            pass
    
    print(
        " Exception Handlers {}".format(numberOfCodeSmells+numberOfG1+numberOfG2+numberOfG3),
    )
    print(
        " numberOfCodeSmells {}".format(numberOfCodeSmells),
        " G1 {}".format(numberOfG1),
        " G2 {}".format(numberOfG2),
        " G3 {}".format(numberOfG3)
    ) 


def get_G2_evolution(gitrepository):
    numberOfCodeSmells = 0
    numberOfG1 = 0
    numberOfG2 = 0
    numberOfG3 = 0
    for file in gitrepository.files():
        try:
            if ".py" in str(file):
                f = open(file)
                user_ast = ast.parse(f.read())
                for a in ast.walk(user_ast):
                    if is_try(a) == True:
                        for b in a.handlers:
                            for c in b.body:
                                if find_G2(c):
                                    numberOfG2 += 1
                                    break
        except Exception as e:
            pass
    
    print(
        " Exception Handlers {}".format(numberOfCodeSmells+numberOfG1+numberOfG2+numberOfG3),
    )
    print(
        " numberOfCodeSmells {}".format(numberOfCodeSmells),
        " G1 {}".format(numberOfG1),
        " G2 {}".format(numberOfG2),
        " G3 {}".format(numberOfG3)
    )    


def get_G3_evolution(gitrepository):
    numberOfCodeSmells = 0
    numberOfG1 = 0
    numberOfG2 = 0
    numberOfG3 = 0
    for file in gitrepository.files():
        try:
            if ".py" in str(file):
                f = open(file)
                user_ast = ast.parse(f.read())
                for a in ast.walk(user_ast):
                    if is_try(a) == True:
                        for b in a.handlers:
                            for c in b.body:
                                if find_G3(c):
                                    numberOfG3 += 1
                                    print(file)
                                    break
        except Exception as e:
            pass
    
    print(
        " Exception Handlers {}".format(numberOfCodeSmells+numberOfG1+numberOfG2+numberOfG3),
    )
    print(
        " numberOfCodeSmells {}".format(numberOfCodeSmells),
        " G1 {}".format(numberOfG1),
        " G2 {}".format(numberOfG2),
        " G3 {}".format(numberOfG3)
    )    

def get_code_smells_evolution_test(path):
    nested_try = 0
    unchecked_exception = 0
    print_statement = 0
    return_code = 0
    ignored_checked_exception = 0
    any_code_smell = False
    try:
        f = open(path)
        user_ast = ast.parse(f.read())
        for a in ast.walk(user_ast):
            if is_try(a) == True:
                for d in a.body:
                    if check_for_nested_try(d):
                        nested_try += 1        
                for b in a.handlers:
                    if check_for_unchecked_exception(b):
                        unchecked_exception += 1
                
                for c in b.body:
                    if check_for_print_statement(c, b.body):
                        print_statement += 1
                            
                    if check_for_return_code_code_smell(c, b.body):
                        return_code += 1
                            
                    if check_for_ignored_checked_exception(c):
                        ignored_checked_exception += 1
                            
    except Exception as e:
        pass 

    if nested_try > 0 or unchecked_exception > 0 or print_statement > 0 or return_code > 0 or ignored_checked_exception > 0:
        any_code_smell = True
        return (nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, any_code_smell) 

    return (nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, False)  

def whole_evolution(repo):
    print("Analysing repo ... {}".format(repo))
    commits_with_code_smells_dict = dict()
    total_number_of_commits = 0
    path = None
    for commit in RepositoryMining(f"https://github.com/{repo}.git").traverse_commits():
        total_number_of_commits += 1
        for modification in commit.modifications:
            if ".py" in str(modification.filename):
                for root, dir, files in os.walk(gitrepository.path):
                    if modification.filename in files:
                        path = os.path.join(root, modification.filename)
                if path is not None:

                    nested_try, unchecked_exception, print_statement, return_code, ignored_checked_exception, any_code_smell = get_code_smells_evolution_test(path)
                    
                    if any_code_smell and commits_with_code_smells_dict.get(modification.filename) == None:
                        commits_with_code_smells_dict[modification.filename] = [(commit.author.name, commit.committer_date, dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), "added")]

                    if  any_code_smell and commits_with_code_smells_dict.get(modification.filename) is not None:
                        item = commits_with_code_smells_dict.get(modification.filename)[-1]

                        if item[2]['nested_try'] < nested_try or item[3]['unchecked_exception'] < unchecked_exception or item[4]['print_statement'] < print_statement or item[5]['return_code'] < return_code or item[6]['ignored_checked_exception'] < ignored_checked_exception:
                            commits_with_code_smells_dict[modification.filename].append((commit.author.name, commit.committer_date, dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), "added"))
                        
                        if item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code'] > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception:      
                            commits_with_code_smells_dict[modification.filename].append((commit.author.name, commit.committer_date, dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), "removed"))

                    elif not any_code_smell and commits_with_code_smells_dict.get(modification.filename) is not None:
                        item = commits_with_code_smells_dict.get(modification.filename)[-1]

                        if item[2]['nested_try'] > nested_try or item[3]['unchecked_exception'] > unchecked_exception or item[4]['print_statement'] > print_statement or item[5]['return_code']  > return_code or item[6]['ignored_checked_exception'] > ignored_checked_exception:
                            commits_with_code_smells_dict[modification.filename].append((commit.author.name, commit.committer_date, dict({'nested_try': nested_try}), dict({'unchecked_exception': unchecked_exception }), dict({'print_statement':print_statement}), dict({'return_code': return_code}), dict({'ignored_checked_exception': ignored_checked_exception}), "removed"))

    x = repo.replace("/", "_")                  
    filename = f"{x}_result.json"
    
    with open(filename, "w") as json_file:
        json_file.write(json.dumps(commits_with_code_smells_dict, indent=4, sort_keys=True, default=str))


"""
    for key in commits_with_code_smells_dict.keys():
        for item in commits_with_code_smells_dict.get(key):
            print(
                    "Repo {}".format(repo),
                    "Total number of commits in repo: {}".format(total_number_of_commits),
                    "Author {}".format(item[0]),
                    "Modified {}".format(item[1]),
                    "File {}".format(key),
                    "Code smells {}. nested_try: {}, unchecked_exception: {}, print_statement: {}, return_code: {}, ignored_checked_exception: {}  ".format(item[6], item[1]['nested_try'], item[2]['unchecked_exception'], item[3]['print_statement'], item[4]['return_code'], item[5]['ignored_checked_exception']),
                )
"""

t0 = time.time()
"""
with open('Pythonrepos.json') as json_file:
    data = json.load(json_file)
    for p in data:
        whole_evolution(p['repo'])
"""
for repo in set(
        [
            "zeeguu-ecosystem/Zeeguu-API",
            "zeeguu-ecosystem/Zeeguu-Core",
        ]
    ):
    whole_evolution(repo)
t1 = time.time()
total = t1-t0
print(total)

"""
or repo in set(
        [
            
        ]
    ):
"""