from enum import Enum
from copy import deepcopy


class Square(Enum):
    """マス目の状態
    """
    WHITE = 0
    BLACK = 1
    EMPTY = 2


class Player(Enum):
    """プレイヤー
    """
    WHITE = 0
    BLACK = 1


class Dir(Enum):
    """方向を表すタプル (行,列)
    """
    UP_LEFT = (-1, -1)
    UP = (0, -1)
    UP_RIGHT = (1, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN_LEFT = (-1, 1)
    DOWN = (0, 1)
    DOWN_RIGHT = (1, 1)


class Reversi:
    """リバーシクラス
    """

    @classmethod
    def is_valid_position(cls, row: int, col: int):
        """有効な場所か判定

        Args:
            row (int): 行の位置
            col (int): 列の位置

        Returns:
            bool: ボード内の位置（行、列共に0以上8未満）であればTrue、そうでなければFalse
        """
        return not (row < 0 or row >= 8 or col < 0 or col >= 8)

    @classmethod
    def distance(cls, row1: int, col1: int, row2: int, col2: int) -> int:
        """指定の2位置間の距離（行同士、列同士を比較して長い方を2点間の距離としています）

        Args:
            row1 (int): 位置1の行
            col1 (int): 位置1の列
            row2 (int): 位置2の行
            col2 (int): 位置2の列

        Returns:
            int: 距離
        """
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
        'ゲームが終了した状態か'
        return self.__is_end

    @property
    def has_passed(self):
        'パスされたか'
        return self.__has_passed

    @property
    def board(self) -> list[list[Square]]:
        'ボード（ディープコピーを返します）'
        return deepcopy(self.__board)

    @property
    def current_player(self) -> Player:
        '現在のプレイヤー'
        return self.__current_player

    @property
    def current_player_square(self) -> Square:
        '現在のプレイヤーに対応するマス目の状態（石の色）'
        return Square.WHITE if self.current_player == Player.WHITE else Square.BLACK

    @property
    def opposing_square(self) -> Square:
        '現在のプレイヤーの相手に対応するマス目の状態（石の色）'
        return Square.WHITE if self.current_player == Player.BLACK else Square.BLACK

    @property
    def white_score(self) -> int:
        '白のスコア'
        score = 0
        for row in self.__board:
            score += row.count(Square.WHITE)
        return score

    @property
    def black_score(self) -> int:
        '黒のスコア'
        score = 0
        for row in self.__board:
            score += row.count(Square.BLACK)
        return score

    @property
    def playable_positions(self) -> list[(int, int)]:
        """配置可能な位置

        Returns:
            list[(int, int)]: 配置可能な位置(行,列)のタプルのリスト
        """
        ps = []
        for r in range(8):
            for c in range(8):
                if self.is_playable(r, c):
                    ps.append((r, c))

        return ps

    @property
    def empty_positions(self) -> list[(int, int)]:
        """空の位置

        Returns:
            list[(int, int)]: 空の位置(行,列)のタプルのリスト
        """
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.EMPTY:
                    ps.append((r, c))

        return ps

    @property
    def black_positions(self) -> list[(int, int)]:
        """黒の位置

        Returns:
            list[(int, int)]: 黒の位置(行,列)のタプルのリスト
        """
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.BLACK:
                    ps.append((r, c))

        return ps

    @property
    def white_positions(self) -> list[(int, int)]:
        """白の位置

        Returns:
            list[(int, int)]: 白の位置(行,列)のタプルのリスト
        """
        ps = []
        for r in range(8):
            for c in range(8):
                if self.__board[r][c] == Square.WHITE:
                    ps.append((r, c))

    def initialize(self):
        '初期化'
        self.__has_passed = False
        self.__is_end = False

        # 一度空で埋める
        for row in self.__board:
            for i, _ in enumerate(row):
                row[i] = Square.EMPTY

        # 初期配置
        self.__board[3][3] = Square.BLACK
        self.__board[4][4] = Square.BLACK
        self.__board[3][4] = Square.WHITE
        self.__board[4][3] = Square.WHITE

        # 先手は黒
        self.__current_player = Player.BLACK

    def is_playable(self, row: int, col: int, out_playable_dirs: list = None) -> bool:
        """配置可能かどうか

        Args:
            row (int): 行
            col (int): 列
            out_playable_dirs (list, optional): 石を返す方向を出力するリスト. Defaults to None.

        Returns:
            bool: 配置可能であればTrue、そうでなければFalse
        """
        if not Reversi.is_valid_position(row, col):
            return False

        if self.__board[row][col] != Square.EMPTY:
            return False

        playable = False
        # 全方向に対して
        for dir in Dir:
            d = dir.value

            # 特定方向にずらした位置
            r_it = row + d[1]
            c_it = col + d[0]

            # 相手の石が置かれていないorボード外になるまでずらしていく
            while Reversi.is_valid_position(r_it, c_it) \
                    and self.__board[r_it][c_it] == self.opposing_square:
                r_it += d[1]
                c_it += d[0]

            # ずらされた位置がボード内and自分の石and距離が1より大きいならば、配置可能
            if Reversi.is_valid_position(r_it, c_it) \
                    and Reversi.distance(row, col, r_it, c_it) > 1\
                    and self.__board[r_it][c_it] == self.current_player_square:
                playable = True
                # 出力引数があれば判定している方向を追加
                if out_playable_dirs != None:
                    out_playable_dirs.append(dir)

        return playable

    def play(self, row: int, col: int) -> bool:
        """プレイヤーの石を配置し、反転される石は反転し、プレイヤーを交代。
        交代した結果、配置可能な箇所がなければパスし(has_passedをTrueとし)、さらにターンを進める。
        両者共パスならゲーム終了とする。(is_endがTrueとなる)

        Args:
            row (int): 行
            col (int): 列

        Returns:
            bool: 配置できたらTrue、できなかったらFalse
        """
        # 配置可能か判定しつつ、反転方向も取得
        playable_dirs = []
        if not self.is_playable(row, col, playable_dirs):
            return False

        # 配置
        self.__board[row][col] = self.current_player_square

        # 反転
        for dir in playable_dirs:
            d = dir.value
            r_it = row + d[1]
            c_it = col + d[0]
            while self.__board[r_it][c_it] == self.opposing_square:
                self.__board[r_it][c_it] = self.current_player_square
                r_it += d[1]
                c_it += d[0]

        # プレイヤー交代
        self.__change_current_player()

        if len(self.playable_positions) > 0:
            # 配置可能な場所があればそのまま継続
            self.__has_passed = False
            self.__is_end = False
        else:
            # 配置可能な場所がないので再度プレイヤーを交代しパスフラグをTrueにする
            self.__change_current_player()
            self.__has_passed = True
            if len(self.playable_positions) == 0:
                # 交代後も配置可能な場所がなければ両者とも配置不可能なのでゲーム終了
                self.__is_end = True

        return True

    def to_string(self) -> str:
        """現在の状態を文字列で表示

        Returns:
            str: 文字列
        """
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
