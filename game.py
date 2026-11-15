from strategy import Strategy
from random import random


class Game:
    def __init__(self, s1: Strategy, s2: Strategy, nb_rounds: int, noise: float, horizon: float, point_matrix: list[list[tuple[int,int]]]):
        self.strategy1, self.strategy2 = s1, s2
        self.nb_rounds = nb_rounds
        self.noise = noise
        self.horizon = horizon
        self.point_matrix = point_matrix
        self.current_round = 0
        self.score1, self.score2 = 0, 0

    def calculate_scores(self, last_move: str, o_last_move: str):
        return self.point_matrix[ord(last_move) - ord('C')][ord(o_last_move) - ord('C')]

    def play_round(self, verbose: int):
        last_move_1 = self.strategy1.last_move
        last_move_2 = self.strategy2.last_move
        self.strategy1.apply(self.current_round, last_move_2, self.noise)
        self.strategy2.apply(self.current_round, last_move_1, self.noise)
        scores = self.calculate_scores(self.strategy1.last_move, self.strategy2.last_move)
        self.score1 += scores[0]
        self.score2 += scores[1]
        if verbose > 1:
            print(f"\t\t{self.strategy1.__class__.__name__}: {self.strategy1.last_move} (+{scores[0]})")
            print(f"\t\t{self.strategy2.__class__.__name__}: {self.strategy2.last_move} (+{scores[1]})")

    def resolve(self, verbose: int):
        for i in range(self.nb_rounds):
            if random() > (1-self.horizon):
                if verbose > 0:
                    print(f"\tHorizon reached at round {i}")
                break
            if verbose > 1:
                print(f"\tRound {i}:")
            self.play_round(verbose)
            self.current_round += 1