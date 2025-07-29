from hyperskill_python_portfolio.rps.game_logic import GameRules


def test_classic_rock_paper_scissors() -> None:
    options = GameRules()
    # User wins
    assert options.compare("rock", "scissors") == 1
    assert options.compare("scissors", "paper") == 1
    assert options.compare("paper", "rock") == 1
    # Draws
    assert options.compare("rock", "rock") == 0
    # Computer wins
    assert options.compare("rock", "paper") == -1
