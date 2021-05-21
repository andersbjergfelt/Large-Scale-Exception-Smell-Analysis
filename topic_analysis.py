from evolution.evolution import Evolution
import time

if __name__ == '__main__':
    start_time = time.time()
    Evolution().whole_evolution_multiple_repositories('Python_api')
    Evolution().whole_evolution_multiple_repositories('Python_application')
    Evolution().whole_evolution_multiple_repositories('Python_artificial-intelligence')
    Evolution().whole_evolution_multiple_repositories('Python_database')
    Evolution().whole_evolution_multiple_repositories('Python_django')
    Evolution().whole_evolution_multiple_repositories('Python_flask')
    Evolution().whole_evolution_multiple_repositories('Python_library')
    Evolution().whole_evolution_multiple_repositories('Python_machine_learning')

    end_time = time.time()
    print(end_time - start_time)
