from .board import Board
from .board import Player
from .board import Square


class Reversi:
    def __init__(self):
        self.__board = Board()
        self.__is_end = False
        self.__has_passed = False

    @property
    def is_end(self):
        return self.__is_end

    @property
    def has_passed(self):
        return self.__has_passed

    @property
    def current_player(self) -> Player:
        return self.__board.current_player

    @property
    def board_squares(self) -> list[list[Square]]:
        return self.__board.squares

    @property
    def board_string(self) -> str:
        return self.__board.to_string()

    def reset(self) -> None:
        self.__board.initialize()
        self.__is_end = False
        self.__has_passed = False

    def receive_input(self, row: int, col: int) -> bool:
        if not self.__board.play(row, col):
            return False

        self.__board.change_current_player()
        if len(self.__board.playable_positions) > 0:
            self.__is_end = False
            self.__has_passed = False
        else:
            self.__has_passed = True
            self.__board.change_current_player()
            if len(self.__board.playable_positions) == 0:
                self.__is_end = True

        return True
