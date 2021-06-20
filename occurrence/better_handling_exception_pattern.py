class BetterHandlingExceptionPattern:

    def __init__(self, catch_typed_exception,
                 throw_typed_exception, return_statement,
                 import_from,
                 state_recovery, retry):
        """
        :param catch_typed_exception
        :param throw_typed_exception:
        :param return_statement:
        :param import_from:
        :param state_recovery:
        :param retry:
        """
        self.catch_typed_exception = catch_typed_exception
        self.throw_typed_exception = throw_typed_exception
        self.return_statement = return_statement
        self.import_from = import_from
        self.state_recovery = state_recovery
        self.retry = retry

    def __eq__(self, other):
        return self.catch_typed_exception == other.catch_typed_exception \
               and self.throw_typed_exception == other.throw_typed_exception \
               and self.return_statement == other.return_statement \
               and self.import_from == other.import_from \
               and self.state_recovery == other.state_recovery \
               and self.retry == other.retry
