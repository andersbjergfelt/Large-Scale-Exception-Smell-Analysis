class Robustness:

    def __init__(self, exception_type_is_not_generic,
                 raise_type_exception, return_statement,
                 import_from,
                 state_recovery, behavior_recovery):
        """
        :param exception_type_is_not_generic
        :param raise_type_exception:
        :param return_statement:
        :param import_from:
        :param state_recovery:
        :param behavior_recovery:
        """
        self.exception_type_is_not_generic = exception_type_is_not_generic
        self.raise_type_exception = raise_type_exception
        self.return_statement = return_statement
        self.import_from = import_from
        self.state_recovery = state_recovery
        self.behavior_recovery = behavior_recovery

    def __eq__(self, other):
        return self.exception_type_is_not_generic == other.exception_type_is_not_generic \
               and self.raise_type_exception == other.raise_type_exception \
               and self.return_statement == other.return_statement \
               and self.import_from == other.import_from \
               and self.state_recovery == other.state_recovery \
               and self.behavior_recovery == other.behavior_recovery
