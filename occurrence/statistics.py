class Statistics:
    def __init__(self, exception_handlers_added,
                 exception_handlers_removed):
        """
        :param added
        lists of exception handlers added to the file
        :param removed:
        lists of exception handlers removed from the file.
        """
        self.exception_handlers_added = exception_handlers_added
        self.exception_handlers_removed = exception_handlers_removed
