import argparse

from game.game import launch_game


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    parser.add_argument("--mode", choices={"game"}, help="mode to launch tetris", default="game")

    args = parser.parse_args()

    if args.mode == "game":
        launch_game()


if __name__ == "__main__":
    main()
