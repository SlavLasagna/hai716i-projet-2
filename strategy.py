from abc import ABC, abstractmethod
from utils import *

class Strategy(ABC):
    def __init__(self):
        self.last_move = ''

    @abstractmethod
    def apply(self, round_n: int, o_last_move: str) -> str:
        pass


class AllD(Strategy):
    def apply(self, round_n: int, o_last_move: str) -> str:
        self.last_move = 'D'
        return self.last_move

class Random(Strategy):
    def apply(self, round_n: int, o_last_move: str) -> str:
        self.last_move = 'D' if random() > 0.50 else 'C'
        return self.last_move


class TFT(Strategy):
    def apply(self, round_n: int, o_last_move: str) -> str:
        self.last_move = 'C' if round_n == 0 else o_last_move
        return self.last_move

class Tester(Strategy):
    def __init__(self):
        super().__init__()
        self.repeat = 0

    def apply(self, round_n: int, o_last_move: str) -> str:
        self.repeat += 1
        if round_n == 0 or o_last_move == 'D':
            self.last_move = 'D'
        elif self.repeat%3 == 0:
            self.last_move = 'D'
        else:
            self.last_move = 'C'
        return self.last_move

class Joss(Strategy):
    def apply(self, round_n: int, o_last_move: str) -> str:
        if round_n == 0:
            self.last_move = 'C'
        elif o_last_move == 'C' and random() > 0.90:
            self.last_move = 'D'
        else:
            self.last_move = o_last_move
        return self.last_move