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


class Reversi:
    @classmethod
    def is_valid_position(cls, row: int, col: int):
        return not (row < 0 or row >= 8 or col < 0 or col >= 8)

    @classmethod
    def distance(cls, row1: int, col1: int, row2: int, col2: int) -> int:
        dr = abs(row1 - row2)
        dc = abs(col1 - col2)
        return dr if dr > 0 else dc

    def __init__(self):
        self.__board = [[Square.EMPTY] * 8 for i in range(8)]
        self.__has_passed = False
        self.__is_end = False
        self.initialize()

    @property
    def is_end(self):
        return self.__is_end

    @property
    def has_passed(self):
        return self.__has_passed

    @property
    def board(self) -> list[list[Square]]:
        return deepcopy(self.__board)

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
        for row in self.__board:
            score += row.count(Square.WHITE)
        return score

    @property
    def black_score(self) -> int:
        score = 0
        for row in self.__board:
            score += row.count(Square.BLACK)
        return score

    @property
    def playable_positions(self) -> list[(int, int)]:
        ps = []
        for r in range(8):
            for c in range(8):
                if self.is_playable(r, c):
                    ps.append((r, c))

        return ps

    @property
    def empty_positions(self) -> list[(int, int)]:
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.EMPTY:
                    ps.append((r, c))

    @property
    def black_positions(self) -> list[(int, int)]:
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.BLACK:
                    ps.append((r, c))

        return ps

    @property
    def white_positions(self) -> list[(int, int)]:
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.WHITE:
                    ps.append((r, c))

    def initialize(self):
        self.__has_passed = False
        self.__is_end = False

        for row in self.__board:
            for i, _ in enumerate(row):
                row[i] = Square.EMPTY

        self.__board[3][3] = Square.BLACK
        self.__board[4][4] = Square.BLACK
        self.__board[3][4] = Square.WHITE
        self.__board[4][3] = Square.WHITE

        self.__current_player = Player.BLACK

    def is_playable(self, row: int, col: int, out_playable_dirs: list = None) -> bool:
        if not Reversi.is_valid_position(row, col):
            return False

        if self.__board[row][col] != Square.EMPTY:
            return False

        playable = False
        for dir in Dir:
            d = dir.value
            r_it = row + d[1]
            c_it = col + d[0]
            while Reversi.is_valid_position(r_it, c_it) \
                    and self.__board[r_it][c_it] == self.opposing_square:
                r_it += d[1]
                c_it += d[0]

            if Reversi.is_valid_position(r_it, c_it) \
                    and Reversi.distance(row, col, r_it, c_it) > 1\
                    and self.__board[r_it][c_it] == self.current_player_square:
                playable = True
                if out_playable_dirs != None:
                    out_playable_dirs.append(dir)

        return playable

    def play(self, row: int, col: int) -> bool:
        playable_dirs = []
        if not self.is_playable(row, col, playable_dirs):
            return False

        self.__board[row][col] = self.current_player_square

        for dir in playable_dirs:
            d = dir.value
            r_it = row + d[1]
            c_it = col + d[0]
            while self.__board[r_it][c_it] == self.opposing_square:
                self.__board[r_it][c_it] = self.current_player_square
                r_it += d[1]
                c_it += d[0]

        self.__change_current_player()
        if len(self.playable_positions) > 0:
            self.__has_passed = False
            self.__is_end = False
        else:
            self.__change_current_player()
            self.__has_passed = True
            if len(self.playable_positions) == 0:
                self.__is_end = True

        return True

    def to_string(self) -> str:
        string = f'Current Player: {self.current_player} \n'
        string += f'Black: {self.black_score} \n'
        string += f'White: {self.white_score} \n'
        string += '   |-A-|-B-|-C-|-D-|-E-|-F-|-G-|-H-|\n'
        for i, row, in enumerate(self.__board):
            string += f' {i + 1} |'
            for square in row:
                s = ''
                if square == Square.WHITE:
                    s += ' ○  '
                elif square == Square.BLACK:
                    s += ' ●  '
                elif square == Square.EMPTY:
                    s += '    '
                string += s
            string += '\n'
        return string

    def __change_current_player(self):
        self.__current_player = Player.WHITE if self.current_player == Player.BLACK else Player.BLACK
