import matplotlib.pyplot as plt
def exception_smell_topics_distribution():
    labels = 'Nested try', 'Only Generic Exception', 'Print statement', 'Return code', "Ignored exception"
    sizes = [16299, 118272, 9400, 1032, 175483]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def exception_smell_python_in_a_day_distribution():
    labels = 'Nested try', 'Only Generic Exception', 'Print statement', 'Return code', "Ignored exception"
    sizes = [5182, 37127, 4129, 409, 44493]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

##exception_smell_python_in_a_day_distribution()

def robustness_topics_distribution():
    labels = 'Error reporting', 'State recovery', 'Behavior recovery'
    sizes = [1079433, 359950, 5997]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

def robustness_in_day_of_python_distribution():
    labels = 'Error reporting', 'State recovery', 'Behavior recovery'
    sizes = [174949, 60015, 1002]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

robustness_in_day_of_python_distribution()
##robustness_topics_distribution()