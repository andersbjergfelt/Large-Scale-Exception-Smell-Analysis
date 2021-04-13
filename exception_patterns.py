import ast
class ExceptionPatterns():
    def __init__(self) -> None:
        pass

    def is_try(self,node):
        return isinstance(node, ast.Try)

    """
    G0 (you know an exception has been raised; Code Smell
    the component has handled it in some undefined way;
    and the application is in error and may or may not terminate.)
    Also known as Dummy Handler
    """
    def check_for_nested_try(self,node):
        if self.is_try(node):
            return True


    def check_for_generic_exception(self,node):
        if isinstance(node, ast.ExceptHandler):
            if isinstance(node.type, ast.Name):
                if node.type.id == "" or node.type.id == "Exception" or node.type is None:
                    return True
        

    def check_for_ignored_checked_exception(self,node,body):
        if isinstance(node, ast.Pass) and len(body) == 1:
            return True    


    def check_for_print_statement(self, node, body):
        ## node.body should be equal to 1 because we want to know whether the print statement is the only statement. == dummy handler
        if isinstance(node, ast.Expr) and len(body) == 1:
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "print" or node.value.func.id == "Log" or node.value.func.id == "log":
                    return True
    

    def check_for_return_code_code_smell(self, node, body):
        if isinstance(node, ast.Expr) and len(body) == 1:
            if isinstance(node.value.func, ast.Name):
                if node.value.func.id == "exit" or node.value.func.id == "sys.exit":
                        return True
        elif isinstance(node, ast.Expr) and len(body) == 2:
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

    def check_for_dummy_handler_with_retrow(self,node):
        if isinstance(node, ast.Raise):
            return True

    def check_for_exception(self, node):
        if isinstance(node, ast.ExceptHandler):
            if isinstance(node.type, ast.Name):
                if node.type.id != "Exception":
                    return True


    """
    G2 (‘‘state-recovery”) -> faulting component maintains a correct state to continue running 
    and propagates an exception to indicate its failure.
    Look for Assign in AST
    """
    def find_G2(self,node):
        if isinstance(node, ast.Assign):
            return True

    """
    G3 (‘‘behavior-recovery”) -> After the faulting component finishes handling the exception, 
    the application delivers the requested service and continues to run normally retry
    """
    """
    If there is a while loop or for loop we must interpret that as recovery. 
    """
    def find_G3(self, node):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            return True
        
        if self.is_try(node) == True:
            for b in node.handlers:
                if isinstance(b, ast.For) or isinstance(b, ast.While):
                    return True
