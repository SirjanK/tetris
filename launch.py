import argparse

from game.game import launch_game


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    parser.add_argument("--mode", choices={"game"}, help="mode to launch tetris", default="game")
    parser.add_argument("--log_keystroke_delta", action="store_true", help="log the keystroke time delta; only works in game mode", default=False)
    parser.add_argument("--human_benchmark_time", type=float, help="during game mode, log score after each game and reset each game after this time period in seconds", default=None, required=False)

    args = parser.parse_args()

    if args.mode == "game":
        launch_game(
            log_keystroke_delta=args.log_keystroke_delta,
            human_benchmark_time=args.human_benchmark_time,
        )


if __name__ == "__main__":
    main()
