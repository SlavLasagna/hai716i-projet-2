import sys
import argparse

from tournament import Tournament
from random import seed


def parse_args(argv: list[str]):
    parser = argparse.ArgumentParser(prog="main.py")

    parser.add_argument("-r", "--rounds", help="Number of rounds per game", type=int, default=200)
    parser.add_argument("-g", "--games", help="Number of games per pool", type=int, default = 5)
    parser.add_argument("-s", "--seed", help="Random seed", type=int, default = None)
    parser.add_argument("-n", "--noise", help="Noise percentage", type=float, default = 0.0)
    parser.add_argument("-z", "--horizon", help="Horizon percentage", type=float, default = 0.0)
    parser.add_argument("-p", "--points", help="Points matrix, formatted C,C:C,D:D,C:D,D", type=str, default = "3,3:0,5:5,0:2,2")
    parser.add_argument("-v", "--verbose", help="Verbose mode", type=int, default = 0)

    return parser.parse_args(argv)

def parse_point_matrix(arg: str):
    l = [[],[]]
    split = arg.split(":")
    i = 0
    for s in split:
        points = tuple(map(int,s.split(",")))
        row = int(2*i / len(split))
        l[row].append(points)
        i += 1
    return l

def main(argv: list[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    seed(args.seed)
    point_matrix = parse_point_matrix(args.points)

    tournament = Tournament(args.rounds, args.games, args.noise/100, args.horizon/100, point_matrix)
    tournament.start(args.verbose)
    print(tournament.results())
    return 0

if __name__ == "__main__":
    sys.exit(main())