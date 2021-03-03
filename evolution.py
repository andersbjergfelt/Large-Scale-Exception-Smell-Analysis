import sys
import ast
from git import repo
import datetime

from pydriller import RepositoryMining, git_repository
from pydriller import GitRepository

REPO_DIR = ''

gitrepository = GitRepository(REPO_DIR)



def is_try(node):
        return hasattr(ast, "Try") and isinstance(node, ast.Try) or \
               hasattr(ast, "TryExcept") and isinstance(node, ast.TryExcept) or \
               hasattr(ast, "TryFinally") and isinstance(node, ast.TryFinally)



 

def check_for_nested_try(node):
    if is_try(node):
        print("Nested try - code smell")
        return True

def check_for_unchecked_exception(node):
    if node.type.id == None or node.type.id == "":
        print("Unchecked exception")

def check_for_ignored_checked_exception(node):
    if node == isinstance(node, ast.Pass):
        print("Code Smell - ignored checked exception")        

def check_for_print_statement(node, body):
    ## node.body should be equal to 1 because we want to know whether the print statement is the only statement. == dummy handler
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 1:
        if isinstance(node.value.func, ast.Name):
            if node.value.func.id == "print" or node.value.func.id == "print":
                print("Print - Code Smell")
                return True

def check_for_return_code_code_smell(node, body):
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 1:
       if node.value.func.id == "exit" or node.value.func.id == "sys.exit":
                print("Return Code - Code Smell")
                return True
    if hasattr(ast, "Expr") == isinstance(node, ast.Expr) and len(body) == 2:
        if body[0].value.func.id == "exit" or node.value.func.id == "sys" and body[1].value.func.id == "print" or node.value.func.id == "log":
                    print("Return Code - Code Smell")
                    return True
        if body[1].value.func.id == "exit" or node.value.func.id == "sys" and body[0].value.func.id == "print" or node.value.func.id == "log":
                    print("Return Code - Code Smell")
                    return True      
    ### edge case if len(body) > 3. "exit" is still defined as a code smell. 
    for b in body:
        if b.value.func.id == "exit":
            return True

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



def get_code_smells_evolution(gitrepository):
    numberOfCodeSmells = 0
    for file in gitrepository.files():
        try:
            if ".py" in str(file):
                f = open(file)
                user_ast = ast.parse(f.read())
                for a in ast.walk(user_ast):
                    if is_try(a) == True:
                        for d in a.body:
                            if check_for_nested_try(d):
                                numberOfCodeSmells += 1
                                print(file)
                        for b in a.handlers:
                            if check_for_unchecked_exception(b):
                                    print(file)
                                    numberOfCodeSmells += 1
                                    break
                            for c in b.body:
                                if check_for_print_statement(c, b.body):
                                    print(file)
                                    numberOfCodeSmells += 1
                                    break
                                if check_for_return_code_code_smell(c, b.body):
                                    print(file)
                                    numberOfCodeSmells += 1
                                    break
                                if check_for_ignored_checked_exception(c):
                                    print(file)
                                    numberOfCodeSmells += 1
                                    break
        except Exception as e:
            pass
    
    print(
        " numberOfCodeSmells {}".format(numberOfCodeSmells)
    )


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



"""
if find_G2(c): 
                                    numberOfG2 += 1
                                    break
                                if find_G3(c): 
                                    numberOfG3 += 1
                                    break
"""

def get_exceptionhandling_evolution_test(gitrepository):
    numberOfG0 = 0
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
                        for d in a.body:
                            if is_try(d):
                                print("Nested Try")
                        for b in a.handlers:
                                for c in b.body:
                                  ##if check_for_return_code_code_smell(c, b.body):
                                  ##    print(file)  
                                  ##check_for_print_statement(c, b.body)
                                  print(c)
                                  check_for_ignored_checked_exception(c)
        except Exception as e:
            pass




##get_code_smells_evolution(gitrepository=gitrepository)
##get_G1_evolution(gitrepository=gitrepository)
##get_G2_evolution(gitrepository=gitrepository)
##get_G3_evolution(gitrepository=gitrepository)

def whole_evolution():
    newest_hash = gitrepository.get_head().hash
    for commit in gitrepository.get_list_commits():
        print("Date is: {}".format(commit.committer_date))
        gitrepository.checkout(commit.hash)
        get_code_smells_evolution(gitrepository=gitrepository)
        ##get_G1_evolution(gitrepository=gitrepository)
        ##get_G2_evolution(gitrepository=gitrepository)
        ##get_G3_evolution(gitrepository=gitrepository)
    gitrepository.checkout(newest_hash)


whole_evolution()

##print(gitrepository.get_head().hash)

##029b2c90437ebbe244baaf0cce4017fbb7fd2872
