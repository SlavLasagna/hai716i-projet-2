from abc import ABC, abstractmethod
from random import random


def noised_move(move: str, noise: float):
    if random() > (1-noise):
        return 'D' if move == 'C' else 'C'
    return move

class Strategy(ABC):
    def __init__(self):
        self.last_move = ''

    @abstractmethod
    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        pass


class AllD(Strategy):
    """
    Always plays 'D'
    """
    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        self.last_move = noised_move('D', noise)

class Random(Strategy):
    """
    Plays 'C' or 'D' randomly
    """
    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        self.last_move = 'D' if random() > 0.50 else 'C'
        self.last_move = noised_move(self.last_move, noise)


class TFT(Strategy):
    """
    Tit-For-Tat:
    Plays 'C' on the first round, then plays the opponent's last move
    """
    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        self.last_move = 'C' if round_n == 0 else o_last_move
        self.last_move = noised_move(self.last_move, noise)

class Tester(Strategy):
    """
    Tests if the opponent is aggressive:
    Plays 'D' on the first round. If the opponents riposts, plays like Tit-for-Tat, else repeats 'C' 'C' 'D' pattern.
    """
    def __init__(self):
        super().__init__()
        self.repeat = 0
        self.retaliated = False

    def apply(self, round_n, o_last_move, noise: float) -> None:
        if round_n == 0:
            self.last_move = 'D'
        elif self.retaliated:
            self.last_move = o_last_move
        elif round_n >= 2 and o_last_move == 'D':
            self.retaliated = True
            self.last_move = 'C'
        else:
            self.last_move = 'D' if (round_n - 1) % 3 == 2 else 'C'
        self.last_move = noised_move(self.last_move, noise)

class Joss(Strategy):
    """
    Tit-for-Tat, but replaces 'C' by 'D' every tenth occurrence.
    """
    def __init__(self):
        super().__init__()
        self.c_occurrences = 1

    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        move = 'C' if round_n == 0 else o_last_move
        self.last_move = 'D' if move == 'C' and random() < 0.1 else move
        self.last_move = noised_move(self.last_move, noise)

class AllC(Strategy):
    """
    Always plays 'C'.
    """
    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        self.last_move = 'C'
        self.last_move = noised_move(self.last_move, noise)

class TF2T(Strategy):
    """
    Tit-for-2-tats:
    Plays 'D' only if the opponent played 'D' on its last two rounds, else plays 'C'.
    """
    def __init__(self):
        super().__init__()
        self.o_prev = ''  # coup adverse vu au tour précédent

    def apply(self, round_n: int, o_last_move: str, noise: float) -> None:
        self.last_move = 'D' if o_last_move == 'D' and self.o_prev == 'D' else 'C'
        self.o_prev = o_last_move
        self.last_move = noised_move(self.last_move, noise)