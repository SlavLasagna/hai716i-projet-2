import sys
import argparse

from tournament import Tournament
from random import seed


def parse_args(argv: list[str]):
    parser = argparse.ArgumentParser(prog="main.py")

    parser.add_argument("-r", "--rounds", help="Number of rounds per game", type=int, default=200)
    parser.add_argument("-g", "--games", help="Number of games per pool", type=int, default = 5)
    parser.add_argument("-s", "--seed", help="Random seed", type=int, default = None)
    parser.add_argument("-v", "--verbose", help="Verbose mode", type=int, default = 0)

    return parser.parse_args(argv)

def main(argv: list[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    seed(args.seed)

    tournament = Tournament(args.rounds, args.games)
    tournament.start(args.verbose)
    print(tournament.results())
    return 0

if __name__ == "__main__":
    sys.exit(main())