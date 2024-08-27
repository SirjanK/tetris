import argparse
from typing import Optional

from game.game import Mode, Game


def launch_game(mode: Mode, id: str, log_keystroke_delta: bool = False, human_benchmark_time: Optional[float] = None): 
    """
    Launch a game session.

    :param mode: mode to launch tetris
    :param id: id for the game used in outputting metrics
    :param log_keystroke_delta: whether to log the keystroke delta
    :param human_benchmark_time: time period to log the score and reset the game
    """

    def restart_fn():
        game = Game(
            mode=mode,
            id=id,
            restart_fn=restart_fn,
            log_keystroke_delta=log_keystroke_delta, 
            human_benchmark_time=human_benchmark_time,
        )
        game.start()
    
    restart_fn()


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    parser.add_argument("--mode", choices=[mode.name for mode in Mode], help="mode to launch tetris", default=Mode.HUMAN.name)
    parser.add_argument("--id", type=str, help="id for the game used in outputting metrics", default="default", required=False)
    parser.add_argument("--log_keystroke_delta", action="store_true", help="log the keystroke time delta; only works in human mode", default=False)
    parser.add_argument("--human_benchmark_time", type=float, help="during human mode, log score after each game and reset each game after this time period in seconds", default=None, required=False)
    args = parser.parse_args()

    mode = Mode[args.mode]
    launch_game(
        mode=mode,
        id=args.id,
        log_keystroke_delta=args.log_keystroke_delta,
        human_benchmark_time=args.human_benchmark_time,
    )


if __name__ == "__main__":
    main()
