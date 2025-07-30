"""Main entry point for the Hangman game application."""

from .game import Game


def main() -> None:
    """Initializes and runs the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
