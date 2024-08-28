import argparse
from typing import Optional
from agent.repository import AgentType, get_agent
from game.game import Game
from game.mode import Mode


# Default simulation parameters
DEFAULT_SIMULATION_DELTA_T = 0.1
DEFAULT_NUM_SIMULATIONS = 100


def launch_game(
        mode: Mode, 
        id: str, 
        duration: Optional[float] = None,
        agent_type: Optional[AgentType] = None, 
        num_simulations: Optional[int] = None,
        simulation_delta_t: Optional[float] = None, 
        log_keystroke_delta: bool = False, 
        num_human_benchmark_games: Optional[int] = None,
    ): 
    """
    Launch a game session.

    :param mode: mode to launch tetris
    :param id: id for the game used in outputting metrics
    :param duration: duration of the game in seconds
    :param agent_type: type of agent to play the game
    :param num_simulations: number of simulations to run
    :param simulation_delta_t: time period to wait between simulation actions
    :param log_keystroke_delta: whether to log the keystroke delta
    :param num_human_benchmark_games: number of games to play in human benchmark mode
    """

    def init_game() -> Game:
        return Game(
            mode=mode,
            id=id,
            duration=duration,
            agent=get_agent(agent_type=agent_type) if agent_type is not None else None,
            simulation_delta_t=simulation_delta_t,
            log_keystroke_delta=log_keystroke_delta, 
        )

    if mode == Mode.HUMAN:
        if num_human_benchmark_games is None:
            continue_game = True
            while continue_game:
                game = init_game()
                continue_game = game.run()
        else:
            for _ in range(num_human_benchmark_games):
                game = init_game()
                game.run()
    else:
        for _ in range(num_simulations):
            game = init_game()
            game.run()


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    # Game mode and id arguments
    parser.add_argument("--mode", choices=[mode.name for mode in Mode], help="mode to launch tetris", default=Mode.HUMAN.name)
    parser.add_argument("--id", type=str, help="id for the game used in outputting metrics", default="default", required=False)
    parser.add_argument("--duration", type=float, help="duration of the game in seconds", required=False)
    # Human mode arguments
    parser.add_argument("--log_keystroke_delta", action="store_true", help="log the keystroke time delta; only works in human mode", default=False)
    parser.add_argument("--num_human_benchmark_games", type=int, help="number of games to play in human benchmark mode", required=False)
    # Simulation mode arguments - these are required in simulation mode
    parser.add_argument("--agent_type", type=str, help="type of agent to play the game", choices=[agent_type.name for agent_type in AgentType], default=None, required=False)
    parser.add_argument("--simulation_delta_t", type=float, help="time period to wait between simulation actions", default=DEFAULT_SIMULATION_DELTA_T, required=False)
    parser.add_argument("--num_simulations", type=int, help="number of simulations to run", default=DEFAULT_NUM_SIMULATIONS, required=False)
    args = parser.parse_args()

    # Input validation
    mode = Mode[args.mode]
    if mode == Mode.SIMULATION:
        if args.agent_type is None or args.simulation_delta_t is None or args.num_simulations is None or args.duration is None:
            parser.error("--agent_type, --simulation_delta_t, --num_simulations, and --duration are required when mode is SIMULATION")
    if mode == Mode.HUMAN:
        if (args.duration is None) ^ (args.num_human_benchmark_games is None):
            parser.error("--duration and --num_human_benchmark_games should both be provided or neither be provided")

    launch_game(
        mode=mode,
        id=args.id,
        duration=args.duration,
        agent_type=AgentType[args.agent_type] if args.agent_type is not None else None,
        num_simulations=args.num_simulations,
        simulation_delta_t=args.simulation_delta_t,
        log_keystroke_delta=args.log_keystroke_delta,
        num_human_benchmark_games=args.num_human_benchmark_games,
    )


if __name__ == "__main__":
    main()
