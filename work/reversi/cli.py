def main() -> None:
    import sys
    from .reversi import Reversi
    reversi = Reversi()

    while not reversi.is_end:
        print(reversi.to_string())
        print('石を置く位置を入力してください')
        r, c = receive_input()
        while not reversi.play(r, c):
            print('そこには置けないよ')
            r, c = receive_input()

    print(reversi.to_string())


def receive_input() -> (int, int):
    while True:
        try:
            c, r = input().split()
            c = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'].index(c)
            r = int(r) - 1
            return r, c
        except ValueError:
            print('有効な位置を入力してね')


if __name__ == '__main__':
    main()
