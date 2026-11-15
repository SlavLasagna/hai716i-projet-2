from game import Game

class Tournament:
    def __init__(self, nb_rounds: int, nb_games: int, strategies, noise: float, horizon: float, point_matrix: list[list[tuple[int,int]]]):
        self.nb_rounds = nb_rounds
        self.nb_games = nb_games
        self.noise = noise
        self.horizon = horizon
        self.point_matrix = point_matrix
        self.strategies = strategies
        self.scores = {k: 0 for k,_ in self.strategies.items()}
        self.rounds = {k: 0 for k,_ in self.strategies.items()}

    def play_game(self, s1: str, s2: str, n: int, verbose: int = 0) -> None:
        strategy1, strategy2 = self.strategies[s1], self.strategies[s2]
        game = Game(strategy1(), strategy2(), self.nb_rounds, self.noise, self.horizon, self.point_matrix)
        rounds = game.resolve(verbose)
        self.scores[s1] += game.score1
        self.scores[s2] += game.score2
        self.rounds[s1] += rounds
        self.rounds[s2] += rounds
        if verbose > 0:
            print(f"\tGame {n}: {s1} scored {game.score1} points; {s2} scored {game.score2} points over {rounds} rounds")

    def start(self, verbose: int) -> None:
        keys = list(self.strategies.keys())
        i = 1
        for k1 in keys[:len(keys)-1]:
            for k2 in keys[i:]:
                if (k1 == k2):
                    continue
                if verbose > 0:
                    print(f"Tournament pool: {k1}, {k2}")
                for n in range(self.nb_games):
                    self.play_game(k1, k2, n, verbose)
            i += 1