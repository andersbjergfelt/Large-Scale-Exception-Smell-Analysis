from evolution.evolution import Evolution
import argparse


def run():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--repository', action='store', type=str, required=True)
    args = parser.parse_args()
    path_to_repo = args.repo
    topic = path_to_repo.split("/")
    Evolution().whole_evolution_with_try_except_tracking(path_to_repo, topic[1])


if __name__ == '__main__':
    run()
