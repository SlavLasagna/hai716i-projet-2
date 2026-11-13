from game import Game
from strategy import *

class Tournament:
    def __init__(self, nb_rounds, nb_games):
        self.nb_rounds = nb_rounds
        self.nb_games = nb_games
        self.strategies = {
            "AllD": AllD(),
            "Random": Random(),
            "TFT": TFT(),
            "Tester": Tester(),
            "Joss": Joss()
        }
        self.scores = {k: 0 for k,_ in self.strategies.items()}

    def play_game(self, s1: str, s2: str) -> None:
        strategy1, strategy2 = self.strategies[s1], self.strategies[s2]
        game = Game(strategy1, strategy2, self.nb_rounds)
        game.resolve()
        self.scores[s1] += game.score1
        self.scores[s2] += game.score2

    def start(self, verbose: bool) -> None:
        keys = list(self.strategies.keys())
        for k1 in keys:
            for k2 in keys:
                if k1 != k2:
                    for _ in range(self.nb_games):
                        self.play_game(k1, k2)

    def results(self) -> str:
        s = "Average points per round :\n"
        l = zip(self.scores.values(), self.strategies.keys())
        sorted_l = sorted(l, key=lambda x: x[0], reverse=True)
        for score, strategy in sorted_l:
            s += f"{strategy}: {score/(self.nb_games*self.nb_rounds*len(self.strategies))}\n"
        return s