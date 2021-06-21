class ExceptionSmell:

    def __init__(self, nested_try, generic_exception, print_statement,
                 exit_code, ignored_exception, raise_generic_exception, break_statement):
        """
                :param nested_try:
                :param generic_exception:
                :param print_statement:
                :param exit_code:
                :param ignored_exception:
                :param raise_generic_exception:
                :param break_statement:
        """
        self.nested_try = nested_try
        self.generic_exception = generic_exception
        self.print_statement = print_statement
        self.exit_code = exit_code
        self.ignored_exception = ignored_exception
        self.raise_generic_exception = raise_generic_exception
        self.break_statement = break_statement

    def __eq__(self, other):
        return self.nested_try == other.nested_try \
               and self.generic_exception == other.generic_exception \
               and self.print_statement == other.print_statement \
               and self.exit_code == other.exit_code \
               and self.ignored_exception == other.ignored_exception \
               and self.raise_generic_exception == other.raise_generic_exception \
               and self.break_statement == other.break_statement
