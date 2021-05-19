import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10
                     })

def exception_smell_topics_distribution():
    labels = 'Nested try', 'Generic Exception', 'Print statement', 'Exit code', "Ignored exception"
    sizes = [9410, 116085, 17726, 1093, 86258]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def exception_smell_python_in_a_day_distribution():
    labels = 'Nested try', 'Generic Exception', 'Print statement', 'Exit code', "Ignored exception"
    sizes = [6847, 77918, 15839, 560, 54688]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


#exception_smell_python_in_a_day_distribution()

def robustness_topics_distribution():
    labels = 'Error reporting', 'State recovery', 'Behavior recovery'
    sizes = [476435, 59009, 3283]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def robustness_in_day_of_python_distribution():
    labels = 'Error reporting', 'State recovery', 'Behavior recovery'
    sizes = [307677, 37306, 1800]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=0, pctdistance=0.8)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()



#exception_smell_topics_distribution()
robustness_topics_distribution()
#exception_smell_python_in_a_day_distribution()
#robustness_in_day_of_python_distribution()