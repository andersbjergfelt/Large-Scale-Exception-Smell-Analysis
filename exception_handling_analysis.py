from evolution.evolution import Evolution
import sys
import argparse
import logging
import time

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#logger = logging.getLogger('upload_bom')

if __name__ == '__main__':
   # parser = argparse.ArgumentParser(description=__doc__)
    #parser.add_argument('-r', '--results', dest='results', type=str, help='path to results')

    #parser = argparse.ArgumentParser(description=__doc__)
   # parser.add_argument('-j', '--j', dest='jsonf', type=str, help='path to results')

   # args = parser.parse_known_args()
   # logger.info('--------------')
    #Evolution().whole_evolution_multiple_repositories(args.results, args.jsonf)

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

