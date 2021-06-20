class ExceptionHandlerOccurrence:

    def __init__(self, author, lineno, end_lineno, exception_smell, exception_smell_added_or_removed,
                 any_exception_smell, better_handling_exception_pattern, better_handling,
                 better_handling_added_or_removed, changes):
        """
        :param author:
        :param lineno
        :param end_lineno
        :param exception_smell
        :param exception_smell_added_or_removed:
        :param any_exception_smell:
        :param better_handling_exception_pattern:
        :param better_handling_added_or_removed:
        :param changes:
        """
        self.author = author
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.exception_smell = exception_smell
        self.exception_smell_added_or_removed = exception_smell_added_or_removed
        self.any_exception_smell = any_exception_smell
        self.better_handling_exception_pattern = better_handling_exception_pattern
        self.better_handling = better_handling
        self.better_handling_added_or_removed = better_handling_added_or_removed
        self.changes = changes

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
