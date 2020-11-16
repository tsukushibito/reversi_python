from reversi.board import Board
from reversi.board import Square


def test_init():
    board = Board()
    squares = board.squares
    for r in range(8):
        for c in range(8):
            s = Square.EMPTY
            if (r == 3 and c == 3) or (r == 4 and c == 4):
                s = Square.BLACK
            elif (r == 4 and c == 3) or (r == 3 and c == 4):
                s = Square.WHITE
            assert squares[r][c] == s


def test_is_valid_position():
    board = Board()

    is_valid = board.is_valid_position(0, 0)
    assert is_valid == True

    is_valid = board.is_valid_position(8, 0)
    assert is_valid == False


def test_is_playable():
    board = Board()

    assert board.is_playable(0, 0) == False
    assert board.is_playable(4, 2) == True
    assert board.is_playable(5, 3) == True
    assert board.is_playable(3, 3) == False
    assert board.is_playable(4, 5) == False


def test_play():
    board = Board()

    board.play(4, 2)
    squares = board.squares
    assert squares[4][2] == squares[3][3] == squares[4][3] == squares[4][4] == Square.BLACK
    assert squares[3][4] == Square.WHITE


def test_score():
    board = Board()

    assert board.white_score == 2
    assert board.black_score == 2
