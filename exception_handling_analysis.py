from evolution.evolution import Evolution
from result_extraction import ResultExtraction
import argparse


def run():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--repository', action='store', type=str, required=True)
    args = parser.parse_args()
    path_to_repo = args.repository
    topic = path_to_repo.split("/")
    path_to_results = f'topic_analysis_results/{topic[1]}'
    Evolution().whole_evolution_with_try_except_tracking(path_to_repo, topic[1])
    ResultExtraction().current_state(path_to_results)


if __name__ == '__main__':
    run()
