from enum import Enum
from copy import deepcopy


class Square(Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2


class Player(Enum):
    WHITE = 0
    BLACK = 1


class Dir(Enum):
    UP_LEFT = (-1, -1)
    UP = (0, -1)
    UP_RIGHT = (1, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN_LEFT = (-1, 1)
    DOWN = (0, 1)
    DOWN_RIGHT = (1, 1)


class Board:
    @classmethod
    def is_valid_position(cls, row: int, col: int):
        return not (row < 0 or row >= 8 or col < 0 or col >= 8)

    @classmethod
    def distance(cls, row1: int, col1: int, row2: int, col2: int) -> int:
        dr = abs(row1 - row2)
        dc = abs(col1 - col2)
        return dr if dr > 0 else dc

    def __init__(self):
        self.__squares = [[Square.EMPTY] * 8 for i in range(8)]
        self.initialize()
        string = repr(self.__squares)
        print(string)

    @property
    def squares(self) -> list[list[Square]]:
        return deepcopy(self.__squares)

    @property
    def current_player(self) -> Player:
        return self.__current_player

    @property
    def current_player_square(self) -> Square:
        return Square.WHITE if self.current_player == Player.WHITE else Square.BLACK

    @property
    def opposing_square(self) -> Square:
        return Square.WHITE if self.current_player == Player.BLACK else Square.BLACK

    @property
    def white_score(self) -> int:
        score = 0
        for row in self.__squares:
            score += row.count(Square.WHITE)
        return score

    @property
    def black_score(self) -> int:
        score = 0
        for row in self.__squares:
            score += row.count(Square.BLACK)
        return score

    def initialize(self):

        for row in self.__squares:
            for i, _ in enumerate(row):
                row[i] = Square.EMPTY

        self.__squares[3][3] = Square.BLACK
        self.__squares[4][4] = Square.BLACK
        self.__squares[3][4] = Square.WHITE
        self.__squares[4][3] = Square.WHITE

        self.__current_player = Player.BLACK

    def is_playable(self, row: int, col: int, out_playable_dirs: list = None) -> bool:
        if not Board.is_valid_position(row, col):
            return False

        if self.__squares[row][col] != Square.EMPTY:
            return False

        playable = False
        for dir in Dir:
            d = dir.value
            r_it = row + d[1]
            c_it = col + d[0]
            while Board.is_valid_position(r_it, c_it) \
                    and self.__squares[r_it][c_it] == self.opposing_square:
                r_it += d[1]
                c_it += d[0]

            if Board.is_valid_position(r_it, c_it) \
                    and Board.distance(row, col, r_it, c_it) > 1\
                    and self.__squares[r_it][c_it] == self.current_player_square:
                playable = True
                if out_playable_dirs != None:
                    out_playable_dirs.append(dir)

        return playable

    def play(self, row: int, col: int) -> bool:
        playable_dirs = []
        if not self.is_playable(row, col, playable_dirs):
            return False

        self.__squares[row][col] = self.current_player_square

        for dir in playable_dirs:
            d = dir.value
            r_it = row + d[1]
            c_it = col + d[0]
            while self.__squares[r_it][c_it] == self.opposing_square:
                self.__squares[r_it][c_it] = self.current_player_square
                r_it += d[1]
                c_it += d[0]

        self.__current_player = Player.WHITE if self.current_player == Player.BLACK else Player.WHITE

        return True

    def to_string(self) -> str:
        pass
