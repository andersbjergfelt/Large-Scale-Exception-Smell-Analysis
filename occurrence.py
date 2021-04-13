class Occurrence:
    """Class represents a Exception Smell or Robustness occurrence
    Attributes:
    
    """
  
    def __init__(self, author, committer_date, nested_try, unchecked_exception, print_statement, 
                return_code, ignored_checked_exception, code_smell_added_or_removed, error_reporting, 
                state_recovery, behavior_recovery, robustness_added_or_removed, changes):
        """
        :param author:
        :param committer_date:
        :param nested_try:
        :param unchecked_exception:
        :param print_statement:
        :param return_code:
        :param ignored_checked_exception:
        :param code_smell_added_or_removed:
        :param error_reporting:
        :param state_recovery:
        :param behavior_recovery:
        :param robustness_added_or_removed:
        :param changes:
        """        
        self.author = author
        self.committer_date = str(committer_date)
        self.nested_try = nested_try
        self.unchecked_exception = unchecked_exception
        self.print_statement = print_statement
        self.return_code = return_code
        self.ignored_checked_exception = ignored_checked_exception
        self.code_smell_added_or_removed = code_smell_added_or_removed
        self.error_reporting = error_reporting
        self.state_recovery = state_recovery
        self.behavior_recovery = behavior_recovery
        self.robustness_added_or_removed = robustness_added_or_removed
        self.changes = changes