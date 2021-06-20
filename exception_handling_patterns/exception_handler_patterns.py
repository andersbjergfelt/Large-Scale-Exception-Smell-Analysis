import ast
from occurrence.exception_handler_occurrence import ExceptionHandlerOccurrence
from occurrence.exception_smell import ExceptionSmell
from occurrence.better_handling_exception_pattern import BetterHandlingExceptionPattern


class ExceptionHandler:
    LOGGER_LOG = 'log'
    LOGGER_DEBUG = 'debug'
    LOGGER_INFO = 'info'
    LOGGER_WARNING = 'warning'
    LOGGER_ERROR = 'error'
    LOGGER_CRITICAL = 'critical'
    PRINT_STATEMENT = 'print'
    TRACEBACK_TB = 'print_tb'
    TRACEBACK_EXCEPTION = 'print_exception'
    TRACEBACK_EXC = 'print_exc'
    TRACEBACK_LAST = 'print_last'
    TRACEBACK_STACK = 'print_stack'
    STDOUT = 'stdout'
    STDERR = 'stderr'

    EXIT = 'exit'

    print_statements = [
        LOGGER_LOG,
        LOGGER_DEBUG,
        LOGGER_INFO,
        LOGGER_WARNING,
        LOGGER_ERROR,
        LOGGER_CRITICAL,
        PRINT_STATEMENT,
        TRACEBACK_TB,
        TRACEBACK_EXCEPTION,
        TRACEBACK_EXC,
        TRACEBACK_LAST,
        TRACEBACK_STACK,
        STDOUT,
        STDERR
    ]

    exit_statements = [
        EXIT
    ]

    def __init__(self):
        pass

    def is_try(self, node):
        return isinstance(node, ast.Try)

    """
    G0 (you know an exception has been raised; Code Smell
    the component has handled it in some undefined way;
    and the application is in error and may or may not terminate.)
    Also known as Dummy Handler
    """

    def check_for_nested_try(self, node):
        if self.is_try(node):
            return True

    def check_for_generic_exception(self, node):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                return True
            if isinstance(node.type, ast.Name):
                if node.type.id == "" or node.type.id == 'Exception' or node.type.id == 'BaseException':
                    return True

    def check_for_ignored_exception(self, node, except_body):
        if isinstance(node, ast.Pass) and len(except_body) == 1:
            return True

    def check_for_throwing_generic_exception(self, node, except_body):
        if isinstance(except_body.type, ast.Name):
            if except_body.type.id == 'Exception':
                if isinstance(node, ast.Raise):
                    if isinstance(node.exc, ast.Name):
                        return True
                    if isinstance(node.exc, ast.Call):
                        if isinstance(node.exc.func, ast.Name):
                            if node.exc.func.id == 'Exception':
                                return True

        if isinstance(node, ast.Raise):
            if isinstance(node.exc, ast.Call):
                if isinstance(node.exc.func, ast.Name):
                    if node.exc.func.id == 'Exception':
                        return True
        return False

    def check_for_import_from_statement(self, node, body):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            if len(body) == 1:
                return True

    def check_for_break_statement(self, node, body):
        if isinstance(node, ast.Break):
            if len(body) == 1:
                return True



    def check_for_print_statement(self, node, body):
        # and len(body) == 1
        if isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Attribute):
                    if node.value.func.attr in self.print_statements:
                        return True
                    elif isinstance(node.value.func.value, ast.Attribute):
                        if node.value.func.value.attr in self.print_statements:
                            return True
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id in self.print_statements:
                        return True

        if len(body) == 2:
            possible_print_statement = body[1]
            if isinstance(body[0], ast.Import):
                if isinstance(possible_print_statement, ast.Expr):
                    if isinstance(possible_print_statement.value, ast.Call):
                        if isinstance(possible_print_statement.value.func, ast.Attribute):
                            if possible_print_statement.value.func.attr in self.print_statements:
                                return True

    def check_for_return_statement(self, node):
        if isinstance(node, ast.Return):
            return True

    def check_for_exit_code(self, node, except_body):

        if not isinstance(node, ast.Expr):
            return False

        if isinstance(node, ast.Expr) and len(except_body) == 1:
            if isinstance(node.value, ast.Call):
                if isinstance(node.value.func, ast.Name):
                    if node.value.func.id in self.exit_statements:
                        return True

        if isinstance(node, ast.Expr) and len(except_body) == 2:
            if isinstance(except_body[0], ast.Expr) and isinstance(except_body[1], ast.Expr):
                if isinstance(except_body[0].value, ast.Call) and isinstance(except_body[1].value, ast.Call):
                    if isinstance(except_body[0].value.func, ast.Name) and isinstance(except_body[1].value.func,
                                                                                      ast.Name):
                        if except_body[0].value.func.id in self.exit_statements:
                            if except_body[1].value.func.id in self.print_statements:
                                return True
                        if except_body[1].value.func.id in self.exit_statements:
                            if except_body[0].value.func.id in self.print_statements:
                                return True
                                # edge case if len(body) > 3. "exit" is still defined as a code smell.

        if isinstance(node, ast.Expr) and len(except_body) > 3:
            for e_node in except_body:
                if isinstance(e_node, ast.Expr):
                    if isinstance(e_node.value, ast.Call):
                        if isinstance(e_node.value.func, ast.Name):
                            if e_node.value.func.id in self.exit_statements:
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

    def check_for_throw_typed(self, node):
        if isinstance(node, ast.Raise):
            return True

    def check_if_typed_exception(self, node):
        if isinstance(node, ast.ExceptHandler):
            if isinstance(node.type, ast.Name):
                if node.type.id != "Exception" and node.type.id != "BaseException":
                    return True
            if isinstance(node.type, ast.BoolOp):
                if isinstance(node.type.values[0], ast.Name) and isinstance(node.type.values[1], ast.Name):
                    if node.type.values[0].id != 'Exception' and node.type.values[1].id != 'Exception'\
                            and node.type.values[0].id != 'BaseException' and node.type.values[1].id != 'BaseException':
                        return True

            if isinstance(node.type, ast.Attribute):
                if node.type.attr != 'Exception' and node.type.attr != 'BaseException':
                    return True

    """
    G2 (‘‘state-recovery”) -> faulting component maintains a correct state to continue running 
    and propagates an exception to indicate its failure.
    Look for Assign in AST
    Look for the assignment in both the try body and except.
    """

    def check_if_state_recovery(self, node, try_body):
        assignment_targets = []
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignment_targets.append(target.id)
                elif isinstance(target, ast.Attribute):
                    assignment_targets.append(target.attr)

        if assignment_targets:
            for statement in try_body:
                if isinstance(statement, ast.Assign):
                    for target in statement.targets:
                        if isinstance(target, ast.Name):
                            if target.id in assignment_targets:
                                return True
                        elif isinstance(target, ast.Attribute):
                            if target.attr in assignment_targets:
                                return True

    """
    G3 (‘‘behavior-recovery”) -> After the faulting component finishes handling the exception, 
    the application delivers the requested service and continues to run normally retry
    """
    """
    If there is a while loop or for loop we must interpret that as recovery. 
    """

    def check_if_retry_pattern(self, node):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            return True

        if self.is_try(node):
            for handler in node.handlers:
                if isinstance(handler, ast.For) or isinstance(handler, ast.While):
                    return True

    def find_exception_handler_patterns(self, source_code, commit):
        try_excepts = []

        try:

            if not source_code:
                return None

            try:
                user_ast = ast.parse(source_code)
            except SyntaxError as e:
                return None
            except ValueError as e:
                return None

            if user_ast is not None:
                for a in ast.walk(user_ast):
                    if self.is_try(a):
                        exception_smell = ExceptionSmell(nested_try=0, catch_generic_exception=0, print_statement=0,
                                                         exit_code=0,
                                                         ignored_exception=0, throw_generic_exception=0,
                                                         break_statement=0)

                        better_handling_exception_pattern = BetterHandlingExceptionPattern(catch_typed_exception=0, throw_typed_exception=0,
                                                return_statement=0,
                                                import_from=0, state_recovery=0, retry=0)

                        exception_handler = ExceptionHandlerOccurrence(author=commit.author.name,
                                                                       lineno=a.lineno,
                                                                       end_lineno=a.end_lineno,
                                                                       exception_smell=exception_smell,
                                                                       any_exception_smell=False,
                                                                       exception_smell_added_or_removed="",
                                                                       better_handling_exception_pattern=better_handling_exception_pattern,
                                                                       robustness_exception_handling=False,
                                                                       robustness_added_or_removed="",
                                                                       changes=[])
                        exception_handler.lineno = a.lineno
                        exception_handler.end_lineno = a.end_lineno

                        for d in a.body:
                            if isinstance(d, ast.Try):
                                exception_handler.exception_smell.nested_try += 1
                                exception_handler.any_exception_smell = True

                        for b in a.handlers:

                            if ExceptionHandler().check_for_generic_exception(b):
                                exception_handler.exception_smell.catch_generic_exception += 1
                                exception_handler.any_exception_smell = True

                            if ExceptionHandler().check_if_typed_exception(b):
                                exception_handler.better_handling_exception_pattern.catch_typed_exception += 1
                                exception_handler.better_handling = True

                            for c in b.body:
                                if ExceptionHandler().check_for_ignored_exception(c, b.body):
                                    exception_handler.exception_smell.ignored_exception += 1
                                    exception_handler.any_exception_smell = True

                                if ExceptionHandler().check_for_print_statement(c, b.body):
                                    exception_handler.exception_smell.print_statement += 1
                                    exception_handler.any_exception_smell = True

                                if ExceptionHandler().check_for_exit_code(c, b.body):
                                    exception_handler.exception_smell.exit_code += 1
                                    exception_handler.any_exception_smell = True

                                raise_is_generic = ExceptionHandler().check_for_throwing_generic_exception(c, b)

                                if raise_is_generic:
                                    exception_handler.exception_smell.throw_generic_exception += 1
                                    exception_handler.any_exception_smell = True

                                if ExceptionHandler().check_for_throw_typed(c) and not raise_is_generic:
                                    exception_handler.better_handling_exception_pattern.throw_typed_exception += 1
                                    exception_handler.better_handling = True

                                if ExceptionHandler().check_for_break_statement(c, b.body):
                                    exception_handler.exception_smell.break_statement += 1
                                    exception_handler.any_exception_smell = True

                                if ExceptionHandler().check_if_state_recovery(c, a.body):
                                    exception_handler.better_handling_exception_pattern.state_recovery += 1
                                    exception_handler.better_handling = True

                                if ExceptionHandler().check_if_retry_pattern(c):
                                    exception_handler.better_handling_exception_pattern.retry += 1
                                    exception_handler.better_handling = True

                                if ExceptionHandler().check_for_return_statement(c):
                                    exception_handler.better_handling_exception_pattern.return_statement += 1
                                    exception_handler.better_handling = True

                                if ExceptionHandler().check_for_import_from_statement(c, b.body):
                                    exception_handler.better_handling_exception_pattern.import_from += 1
                                    exception_handler.better_handling = True


                        if exception_handler.robustness_exception_handling or exception_handler.any_exception_smell:
                            try_excepts.append(exception_handler)

        except Exception as e:
            print(e)

        return try_excepts
