import argparse


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    parser.add_argument("mode", choices={"game"}, help="mode to launch tetris", default="game")

    args = parser.parse_args()

    if args.mode == "game":
        launch_game()


def launch_game():
    pass


if __name__ == "__main__":
    main()
