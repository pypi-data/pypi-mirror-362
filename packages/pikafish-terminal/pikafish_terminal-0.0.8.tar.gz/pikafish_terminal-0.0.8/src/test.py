from pikafish_terminal.game import play
from pikafish_terminal.logging_config import setup_logging


def main() -> None:
    """Entry point for the pikafish-terminal application."""
    # Initialize logging system
    setup_logging()
    play(depth=1, time_limit_ms=100)


if __name__ == "__main__":
    main()