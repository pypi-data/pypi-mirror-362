import pytest
from pytest import CaptureFixture, MonkeyPatch, approx

from hyperskill_python_portfolio.honest_calculator.main import HonestCalculator, Msg


@pytest.fixture
def calculator() -> HonestCalculator:
    """Provides a fresh instance of HonestCalculator for each test."""
    return HonestCalculator()


def test_is_one_digit(calculator: HonestCalculator) -> None:
    """Tests the _is_one_digit helper method for various cases."""
    assert calculator._is_one_digit(5) is True
    assert calculator._is_one_digit(9) is True
    assert calculator._is_one_digit(-5) is True
    assert calculator._is_one_digit(0) is True
    assert calculator._is_one_digit(10) is False
    assert calculator._is_one_digit(-10) is False
    assert calculator._is_one_digit(5.5) is False


def test_simple_addition(
    calculator: HonestCalculator, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    """Tests a basic calculation using monkeypatch for input and capsys for output."""
    inputs = iter(["2 + 2", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    calculator.run()

    captured = capsys.readouterr()
    assert "4.0" in captured.out
    assert captured.out.strip().startswith(Msg.ENTER_EQUATION.value)


def test_division_by_zero(
    calculator: HonestCalculator, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    """Tests that the division by zero error message is printed."""
    inputs = iter(["5 / 0", "1 + 1", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    calculator.run()

    captured = capsys.readouterr()
    assert Msg.DIV_BY_ZERO.value in captured.out


def test_store_in_memory(
    calculator: HonestCalculator, monkeypatch: MonkeyPatch
) -> None:
    """Tests that a result can be successfully stored in memory."""
    inputs = iter(["10 + 5", "y", "n"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    assert calculator.memory == approx(0.0)
    calculator.run()
    assert calculator.memory == approx(15.0)


def test_use_memory_in_calculation(
    calculator: HonestCalculator, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    """Tests that a stored value in memory can be used in the next calculation."""
    calculator.memory = 15.0
    inputs = iter(["M * 2", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    calculator.run()

    captured = capsys.readouterr()
    assert "30.0" in captured.out


def test_laziness_check(
    calculator: HonestCalculator, monkeypatch: MonkeyPatch, capsys: CaptureFixture
) -> None:
    """Tests that the laziness check prints the correct combined message."""
    inputs = iter(["1 * 0", "n", "n"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    calculator.run()

    expected_msg = (
        Msg.LAZY_PREFIX.value
        + Msg.IS_LAZY.value
        + Msg.IS_VERY_LAZY.value
        + Msg.IS_VERY_VERY_LAZY.value
    )

    captured = capsys.readouterr()
    assert expected_msg in captured.out
