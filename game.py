from strategy import Strategy


POINT_MATRIX = [
    [(3,3),(0,5)],
    [(5,0),(2,2)]
]


class Game:
    def __init__(self, s1: Strategy, s2: Strategy, nb_rounds: int):
        self.strategy1, self.strategy2 = s1, s2
        self.nb_rounds = nb_rounds
        self.current_round = 0
        self.score1, self.score2 = 0, 0

    def calculate_score(self):
        self.score1 += POINT_MATRIX[ord(self.strategy1.last_move)-ord('C')][ord(self.strategy2.last_move)-ord('C')][0]
        self.score2 += POINT_MATRIX[ord(self.strategy1.last_move)-ord('C')][ord(self.strategy2.last_move)-ord('C')][1]

    def play_round(self):
        last_move_1 = self.strategy1.last_move
        last_move_2 = self.strategy2.last_move
        self.strategy1.apply(self.current_round, last_move_2)
        self.strategy2.apply(self.current_round, last_move_1)
        self.calculate_score()

    def resolve(self):
        for i in range(self.nb_rounds):
            self.play_round()
            self.current_round += 1