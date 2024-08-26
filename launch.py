import argparse

from game.game import launch_game


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    parser.add_argument("--mode", choices={"game"}, help="mode to launch tetris", default="game")
    parser.add_argument("--log_keystroke_delta", action="store_true", help="log the keystroke time delta; only works in game mode", default=False)

    args = parser.parse_args()

    if args.mode == "game":
        launch_game(
            log_keystroke_delta=args.log_keystroke_delta,
        )


if __name__ == "__main__":
    main()
