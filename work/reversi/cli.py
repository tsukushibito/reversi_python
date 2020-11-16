def main() -> None:
    import sys
    from .cli_reversi import CliReversi
    cliReversi = CliReversi()
    cliReversi.run()


if __name__ == '__main__':
    main()
