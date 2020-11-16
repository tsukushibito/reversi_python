from .board import Board
from .board import Player
from .board import Square
import os


class CliReversi:

    def __init__(self):
        self.__board = Board()
        self.reset()

    def run(self):
        is_end = False
        is_passed = False
        while not is_end:
            os.system('cls')
            print(self.__board.to_string())

            if not self.__board.has_valid_move:
                if is_passed:
                    is_end = True
                    break

                print('石を置ける場所が無いのでパス！')
                self.__board.change_current_player()
                is_passed = True

            print('石を置く位置を入力してください')
            r, c = self.receive_input()
            while not self.__board.play(r, c):
                print('そこには置けないよ')
                r, c = self.receive_input()

            self.__board.change_current_player()
            is_passed = False

            empty_count = 0
            for row in self.__board.squares:
                empty_count += row.count(Square.EMPTY)
            if empty_count == 0:
                is_end = True
                break

        print(self.__board.to_string())

    def receive_input(self) -> (int, int):
        while True:
            try:
                c, r = input().split()
                c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].index(c)
                r = int(r) - 1
                return r, c
            except ValueError:
                print('有効な位置を入力してね')

    def reset(self):
        self.__board.initialize()
