class ExceptionSmell:

    def __init__(self, nested_try, catch_generic_exception, print_statement,
                 exit_code, ignored_exception, throw_generic_exception, break_statement):
        """
                :param nested_try:
                :param catch_generic_exception:
                :param print_statement:
                :param exit_code:
                :param ignored_exception:
                :param throw_generic_exception:
                :param break_statement:
        """
        self.nested_try = nested_try
        self.catch_generic_exception = catch_generic_exception
        self.print_statement = print_statement
        self.exit_code = exit_code
        self.ignored_exception = ignored_exception
        self.throw_generic_exception = throw_generic_exception
        self.break_statement = break_statement

    def __eq__(self, other):
        return self.nested_try == other.nested_try \
               and self.catch_generic_exception == other.catch_generic_exception \
               and self.print_statement == other.print_statement \
               and self.exit_code == other.exit_code \
               and self.ignored_exception == other.ignored_exception \
               and self.throw_generic_exception == other.throw_generic_exception \
               and self.break_statement == other.break_statement
