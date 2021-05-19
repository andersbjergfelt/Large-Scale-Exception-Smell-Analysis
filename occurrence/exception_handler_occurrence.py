class ExceptionHandlerOccurrence:

    def __init__(self, author, lineno, end_lineno, exception_smell, exception_smell_added_or_removed,
                 any_exception_smell, robustness, robustness_exception_handling,
                 robustness_added_or_removed, changes):
        """
        :param author:
        :param lineno
        :param end_lineno
        :param exception_smell
        :param exception_smell_added_or_removed:
        :param any_exception_smell:
        :param robustness_exception_handling:
        :param robustness_added_or_removed:
        :param changes:
        """
        self.author = author
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.exception_smell = exception_smell
        self.exception_smell_added_or_removed = exception_smell_added_or_removed
        self.any_exception_smell = any_exception_smell
        self.robustness = robustness
        self.robustness_exception_handling = robustness_exception_handling
        self.robustness_added_or_removed = robustness_added_or_removed
        self.changes = changes

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
