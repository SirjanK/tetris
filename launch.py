import argparse
from typing import Optional
from agent.repository import AgentType, get_agent
from game.game import Mode, Game


# Default simulation time and delta t in seconds
DEFAULT_SIMULATION_TIME = 100
DEFAULT_SIMULATION_DELTA_T = 0.1
DEFAULT_NUM_SIMULATIONS = 100


def launch_game(
        mode: Mode, id: str, 
        agent_type: Optional[AgentType] = None, 
        num_simulations: Optional[int] = None,
        simulation_time: Optional[float] = None, 
        simulation_delta_t: Optional[float] = None, 
        log_keystroke_delta: bool = False, 
        human_benchmark_time: Optional[float] = None
    ): 
    """
    Launch a game session.

    :param mode: mode to launch tetris
    :param id: id for the game used in outputting metrics
    :param agent_type: type of agent to play the game
    :param num_simulations: number of simulations to run
    :param simulation_time: time period to run one simulation game for
    :param simulation_delta_t: time period to wait between simulation actions
    :param log_keystroke_delta: whether to log the keystroke delta
    :param human_benchmark_time: time period to log the score and reset the game
    """

    def init_game() -> Game:
        return Game(
            mode=mode,
            id=id,
            agent=get_agent(agent_type),
            simulation_time=simulation_time,
            simulation_delta_t=simulation_delta_t,
            log_keystroke_delta=log_keystroke_delta, 
            human_benchmark_time=human_benchmark_time,
        )

    if mode == Mode.HUMAN:
        continue_game = True
        while continue_game:
            game = init_game()
            continue_game = game.run()
    else:
        for _ in range(num_simulations):
            game = init_game()
            game.run()


def main():
    parser = argparse.ArgumentParser(description="Launch Tetris session")

    # Game mode and id arguments
    parser.add_argument("--mode", choices=[mode.name for mode in Mode], help="mode to launch tetris", default=Mode.HUMAN.name)
    parser.add_argument("--id", type=str, help="id for the game used in outputting metrics", default="default", required=False)
    # Human mode arguments
    parser.add_argument("--log_keystroke_delta", action="store_true", help="log the keystroke time delta; only works in human mode", default=False)
    parser.add_argument("--human_benchmark_time", type=float, 
                        help="during human mode, log score after each game and reset each game after this time period in seconds", default=DEFAULT_SIMULATION_TIME, required=False)
    # Simulation mode arguments - these are required in simulation mode
    parser.add_argument("--agent_type", type=str, help="type of agent to play the game", choices=[agent_type.name for agent_type in AgentType], default=None, required=False)
    parser.add_argument("--simulation_time", type=float, help="time period to run one simulation game for", default=DEFAULT_SIMULATION_TIME, required=False)
    parser.add_argument("--simulation_delta_t", type=float, help="time period to wait between simulation actions", default=DEFAULT_SIMULATION_DELTA_T, required=False)
    parser.add_argument("--num_simulations", type=int, help="number of simulations to run", default=DEFAULT_NUM_SIMULATIONS, required=False)
    args = parser.parse_args()

    mode = Mode[args.mode]

    # Validate simulation mode arguments
    if mode == Mode.SIMULATION:
        if args.agent_type is None or args.simulation_time is None or args.simulation_delta_t is None or args.num_simulations is None:
            parser.error("--agent_type, --simulation_time, and --simulation_delta_t are required when mode is SIMULATION")

    launch_game(
        mode=mode,
        id=args.id,
        agent_type=args.agent_type,
        num_simulations=args.num_simulations,
        simulation_time=args.simulation_time,
        simulation_delta_t=args.simulation_delta_t,
        log_keystroke_delta=args.log_keystroke_delta,
        human_benchmark_time=args.human_benchmark_time,
    )


if __name__ == "__main__":
    main()
