class RobustnessHelper:
    def __init__(self):
        pass

    def check_if_robustness_added(self, current_robustness, new_robustness, current_robustness_sum, new_robustness_sum):
        if current_robustness_sum == new_robustness_sum:
            return False
        robustness_added = False

        for i, item in enumerate(current_robustness):
            if current_robustness[i] != new_robustness[i]:
                if current_robustness[i] < new_robustness[i]:
                    robustness_added = True
                """    
                if i == 0:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                if i == 1:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                if i == 2:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                if i == 3:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                if i == 4:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                if i == 5:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_added = True
                """
        if robustness_added:
            return True

        return False

    def check_if_robustness_removed(self, current_robustness, new_robustness, current_robustness_sum, new_robustness_sum):
        if current_robustness_sum == new_robustness_sum:
            return False

        robustness_removed = False

        for i, item in enumerate(current_robustness):
            if current_robustness[i] != new_robustness[i]:
                if current_robustness[i] > new_robustness[i]:
                    robustness_removed = True
                """    
                if i == 0:
                    if current_robustness[i] > new_robustness[i]:
                        robustness_removed = True
                if i == 1:
                    if current_robustness[i] > new_robustness[i]:
                        robustness_removed = True
                if i == 2:
                    if current_robustness[i] > new_robustness[i]:
                        robustness_removed = True

                if i == 3:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_removed = True

                if i == 4:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_removed = True

                if i == 5:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_removed = True
                """

        if robustness_removed:
            return True

        return False

    def check_if_robustness_switched(self, current_robustness, new_robustness):
        switched_robustness = []
        robustness_switch = {'from': [], 'to': []}
        current_robustness = current_robustness
        new_robustness = new_robustness

        for i, item in enumerate(current_robustness):
            if current_robustness[i] != new_robustness[i]:
                if i == 0:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("exception_type_is_not_generic")
                    else:
                        robustness_switch['from'].append("exception_type_is_not_generic")
                if i == 1:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("raise_type_exception")
                    else:
                        robustness_switch['from'].append("raise_type_exception")
                if i == 2:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("return statement")
                    else:
                        robustness_switch['from'].append("return statement")
                if i == 3:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("import from")
                    else:
                        robustness_switch['from'].append("import from")
                if i == 4:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("state recovery")
                    else:
                        robustness_switch['from'].append("state recovery")
                if i == 5:
                    if current_robustness[i] < new_robustness[i]:
                        robustness_switch['to'].append("behavior recovery")
                    else:
                        robustness_switch['from'].append("behavior recovery")

        if len(robustness_switch['from']) > 0 and len(robustness_switch['to']) > 0:
            switched_robustness.append(robustness_switch)

        if len(switched_robustness) > 0:
            return switched_robustness

        return None
