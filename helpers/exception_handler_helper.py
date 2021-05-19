class ExceptionHandlerHelper:
    def __init__(self):
        pass

    def check_if_exception_smell_switched(self, current_exception_smell_list, new_exception_smell_list):
        switched_exception_smells = []
        exception_smell_switch = {'from': [], 'to': []}
        current_exception_smell_list = current_exception_smell_list
        new_exception_smell_list = new_exception_smell_list

        for i, item in enumerate(current_exception_smell_list):
            if current_exception_smell_list[i] != new_exception_smell_list[i]:
                if i == 0:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("nested try")
                    else:
                        exception_smell_switch['from'].append("nested try")
                if i == 1:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("generic exception")
                    else:
                        exception_smell_switch['from'].append("generic exception")
                if i == 2:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("print statement")
                    else:
                        exception_smell_switch['from'].append("print statement")
                if i == 3:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("exit code")
                    else:
                        exception_smell_switch['from'].append("exit code")
                if i == 4:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("ignored exception")
                    else:
                        exception_smell_switch['from'].append("ignored exception")
                if i == 5:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("raise generic exception")
                    else:
                        exception_smell_switch['from'].append("raise generic exception")
                if i == 6:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_switch['to'].append("break statement")
                    else:
                        exception_smell_switch['from'].append("break statement")

        if len(exception_smell_switch['from']) > 0 and len(exception_smell_switch['to']) > 0:
            switched_exception_smells.append(exception_smell_switch)

        if len(switched_exception_smells) > 0:
            return switched_exception_smells

        return None

    def check_if_exception_added(self, current_exception_smell_list, new_exception_smell_list, current_exception_smell_sum,
                                 new_exception_smell_sum):
        if current_exception_smell_sum == new_exception_smell_sum:
            return False
        exception_smell_added = False

        for i, item in enumerate(current_exception_smell_list):
            if current_exception_smell_list[i] != new_exception_smell_list[i]:

                if current_exception_smell_list[i] < new_exception_smell_list[i]:
                    exception_smell_added = True
                """    
                if i == 0:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 1:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 2:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 3:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 4:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 5:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                if i == 6:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_smell_added = True
                """
        if exception_smell_added:
            return True

        return False

    def check_if_exception_removed(self, current_exception_smell_list, new_exception_smell_list, current_exception_smell_sum,
                                 new_exception_smell_sum):
        if current_exception_smell_sum == new_exception_smell_sum:
            return False

        exception_smell_removed = False

        for i, item in enumerate(current_exception_smell_list):
            if current_exception_smell_list[i] != new_exception_smell_list[i]:
                if current_exception_smell_list[i] > new_exception_smell_list[i]:
                    exception_smell_removed = True
                """"   
                if i == 0:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 1:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 2:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 3:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 4:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 5:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                if i == 6:
                    if current_exception_smell_list[i] > new_exception_smell_list[i]:
                        exception_smell_removed = True
                """
        if exception_smell_removed:
            return True

        return False

    def check_if_switched_exception_smell_robustness(self,current_exception_smell_list, new_exception_smell_list,
                                                     current_robustness, new_robustness):

        exception_handling_switch = dict({'from': [], 'to': []})
        current_exception_smell_list.extend(current_robustness)
        new_exception_smell_list.extend(new_robustness)
        exception_handling_switched = []

        for i, item in enumerate(current_exception_smell_list):
            if current_exception_smell_list[i] != new_exception_smell_list[i]:
                if i == 0:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_nested try")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_nested try")
                if i == 1:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_generic exception")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_generic exception")
                if i == 2:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_print statement")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_print statement")
                if i == 3:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_exit code")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_exit code")
                if i == 4:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_ignored exception")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_ignored exception")
                if i == 5:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_raise generic exception")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_raise generic exception")

                if i == 6:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_break statement")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_break statement")

                if i == 7:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_exception type is not generic")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_exception type is not generic")
                if i == 8:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_raise type exception")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_raise type exception")
                if i == 9:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_return statement")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_return statement")
                if i == 10:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_import from")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_import from")
                if i == 11:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_state recovery")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_state recovery")
                if i == 12:
                    if current_exception_smell_list[i] < new_exception_smell_list[i]:
                        exception_handling_switch['to'].append("in_between_switch_behavior recovery")
                    else:
                        exception_handling_switch['from'].append("in_between_switch_behavior recovery")

        if len(exception_handling_switch['from']) > 0 and len(exception_handling_switch['to']) > 0:
            exception_handling_switched.append(exception_handling_switch)

        if len(exception_handling_switched) > 0:
            return exception_handling_switched

        return None
