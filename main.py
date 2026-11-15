import sys
import argparse

from tournament import Tournament
from random import seed
from strategy import *

def parse_args(argv: list[str]):
    parser = argparse.ArgumentParser(prog="main.py")

    parser.add_argument("-r", "--rounds", help="Number of rounds per game", type=int, default=200)
    parser.add_argument("-g", "--games", help="Number of games per pool", type=int, default = 5)
    parser.add_argument("-s", "--seed", help="Random seed", type=int, default = 0xDEADBEEF)
    parser.add_argument("-n", "--noise", help="Noise percentage", type=float, default = 0.0)
    parser.add_argument("-z", "--horizon", help="Horizon percentage", type=float, default = 0.0)
    parser.add_argument("-p", "--points", help="Points matrix, formatted C,C:C,D:D,C:D,D", type=str, default = "3,3:0,5:5,0:2,2")
    parser.add_argument("-v", "--verbose", help="Verbose mode", type=int, default = 0)
    parser.add_argument("-t", "--tournaments", help="Number of tournaments", type=int, default = 200)

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

def results(scores, strategies, rounds):
    s = "Average points per round :\n"
    l = zip(scores.values(), strategies.keys(), rounds.values())
    sorted_l = sorted(l, key=lambda x: x[0] / x[2], reverse=True)
    for i, (score, strategy, rounds) in enumerate(sorted_l):
        s += f"{i + 1}. {strategy}: {round(score / rounds, 3)}\n"
    return s

def main(argv: list[str] | None = None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    strategies = {
            "AllD": AllD,
            "Random": Random,
            "TFT": TFT,
            "Tester": Tester,
            "Joss": Joss,
            "AllC": AllC,
            "TF2T": TF2T,
    }
    scores = {k: 0 for k,_ in strategies.items()}
    rounds = {k: 0 for k,_ in strategies.items()}

    seed(args.seed)
    point_matrix = parse_point_matrix(args.points)

    for _ in range(args.tournaments):
        tournament = Tournament(args.rounds, args.games, strategies, args.noise / 100, args.horizon / 100, point_matrix)
        tournament.start(args.verbose)
        for k,_ in scores.items():
            scores[k] += tournament.scores[k]
            rounds[k] += tournament.rounds[k]

    print(results(scores, strategies, rounds))
    return 0

if __name__ == "__main__":
    sys.exit(main())