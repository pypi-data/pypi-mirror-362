from unittest.mock import Mock, patch

from pytest import approx

from hyperskill_python_portfolio.billsplitter.main import get_non_negative_number


@patch("hyperskill_python_portfolio.billsplitter.main.input", return_value="10")
def test_get_non_negative_number_with_valid_integer(mock_input: Mock) -> None:
    result = get_non_negative_number("Enter number:", int)

    assert result == 10
    assert isinstance(result, int)
    mock_input.assert_called_once_with("Enter number:")


@patch("hyperskill_python_portfolio.billsplitter.main.input", return_value="7.5")
def test_get_non_negative_number_with_valid_float(mock_input: Mock) -> None:
    result = get_non_negative_number("Enter value:", float)

    assert result == approx(7.5)
    assert isinstance(result, float)


@patch("hyperskill_python_portfolio.billsplitter.main.input", return_value="0")
def test_get_non_negative_number_with_zero(mock_input: Mock) -> None:
    result = get_non_negative_number("Enter number:", int)

    assert result == 0


@patch("hyperskill_python_portfolio.billsplitter.main.print")
@patch("hyperskill_python_portfolio.billsplitter.main.input", side_effect=["-5", "3"])
def test_get_non_negative_number_with_negative_input_first(
    mock_input: Mock, mock_print: Mock
) -> None:
    result = get_non_negative_number("Enter number:", int)

    assert result == 3
    mock_print.assert_any_call("Number cannot be negative.")


@patch("hyperskill_python_portfolio.billsplitter.main.print")
@patch("hyperskill_python_portfolio.billsplitter.main.input", side_effect=["abc", "5"])
def test_get_non_negative_number_with_value_error_first(
    mock_input: Mock, mock_print: Mock
) -> None:
    result = get_non_negative_number("Enter number:", int)

    assert result == 5
    mock_print.assert_any_call("Please enter a valid int.")
