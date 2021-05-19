import ast
from exception_handling_patterns.exception_handler_patterns import ExceptionHandler
from occurrence.exception_handler_occurrence import ExceptionHandlerOccurrence
from occurrence.exception_smell import ExceptionSmell
from occurrence.robustness import Robustness


class TryVisitor(ast.NodeVisitor):

    def __init__(self):
        self.try_excepts = []

    def visit_Try(self, node):

        exception_smell = ExceptionSmell(nested_try=0, generic_exception=0, print_statement=0, exit_code=0,
                                         ignored_exception=0, raise_generic_exception=0)

        robustness = Robustness(exception_type_is_not_generic=0, raise_type_exception=0, return_statement=0,
                                error_reporting=0
                                , state_recovery=0, behavior_recovery=0)

        exception_handler = ExceptionHandlerOccurrence(author="",
                                                       lineno=node.lineno,
                                                       end_lineno=node.end_lineno,
                                                       exception_smell=exception_smell,
                                                       any_exception_smell=False,
                                                       exception_smell_added_or_removed="",
                                                       robustness=robustness,
                                                       robustness_exception_handling=False,
                                                       robustness_added_or_removed="",
                                                       changes=[])
        for d in node.body:
            if isinstance(d, ast.Try):
                exception_handler.exception_smell.nested_try += 1
                exception_handler.any_exception_smell = True

        for handler in node.handlers:

            if ExceptionHandler().check_for_generic_exception(handler):
                exception_handler.exception_smell.generic_exception += 1
                exception_handler.any_exception_smell = True
                continue
            if ExceptionHandler().check_if_exception_is_not_generic(handler):
                exception_handler.robustness.exception_type_is_not_generic += 1
                exception_handler.robustness_exception_handling = True

            for c in handler.body:
                if ExceptionHandler().check_for_ignored_exception(c, handler.body):
                    exception_handler.exception_smell.ignored_exception += 1
                    exception_handler.any_exception_smell = True
                    continue

                if ExceptionHandler().check_for_print_statement(c, handler.body):
                    exception_handler.exception_smell.print_statement += 1
                    exception_handler.any_exception_smell = True

                if ExceptionHandler().check_for_return_code(c, handler.body):
                    exception_handler.exception_smell.exit_code += 1
                    exception_handler.any_exception_smell = True

                raise_is_generic = ExceptionHandler().check_for_raise_generic_exception(c, handler)

                if raise_is_generic:
                    exception_handler.exception_smell.raise_generic_exception += 1
                    exception_handler.any_exception_smell = True

                if ExceptionHandler().check_for_dummy_handler_with_retrow(c, handler.body) and not raise_is_generic:
                    exception_handler.robustness.raise_type_exception += 1
                    exception_handler.robustness_exception_handling = True

                if ExceptionHandler().find_state_recovery(c, node.body):
                    exception_handler.robustness.state_recovery += 1
                    exception_handler.robustness_exception_handling = True

                if ExceptionHandler().find_behavior_recovery(c):
                    exception_handler.robustness.behavior_recovery += 1
                    exception_handler.robustness_exception_handling = True

                if ExceptionHandler().check_for_return_statement(c):
                    exception_handler.robustness.return_statement += 1
                    exception_handler.robustness_exception_handling = True

        if exception_handler.robustness_exception_handling or exception_handler.any_exception_smell:
            self.try_excepts.append(exception_handler)

        return self.try_excepts
