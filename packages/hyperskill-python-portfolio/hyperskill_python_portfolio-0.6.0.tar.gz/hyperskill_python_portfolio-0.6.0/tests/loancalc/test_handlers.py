from argparse import Namespace
from unittest.mock import patch

import pytest

from hyperskill_python_portfolio.loancalc.handlers import handle_annuity, handle_diff
from hyperskill_python_portfolio.loancalc.models import LoanResult

# Corrected paths to include the full package namespace
BASE_PATH = "hyperskill_python_portfolio.loancalc.handlers"
CALCULATE_ANNUITY_PAYMENT_PATH = f"{BASE_PATH}.calculate_annuity_payment"
CALCULATE_ANNUITY_PRINCIPAL_PATH = f"{BASE_PATH}.calculate_annuity_principal"
CALCULATE_ANNUITY_PERIODS_PATH = f"{BASE_PATH}.calculate_annuity_periods"
CALCULATE_DIFF_PATH = f"{BASE_PATH}.calculate_diff"


def test_handle_annuity_calculates_payment() -> None:
    # Arrange: Setup arguments and the mock for the core function
    args = Namespace(principal=500000, periods=360, interest=7.5, payment=None)
    mock_result = LoanResult(payment=3497, overpayment=758920)

    with patch(
        CALCULATE_ANNUITY_PAYMENT_PATH, return_value=mock_result
    ) as mock_calculate:
        # Act: Call the function we are testing
        result_string = handle_annuity(args)

    # Assert: Check that our expectations were met
    expected_interest = 7.5 / (12 * 100)
    mock_calculate.assert_called_once_with(expected_interest, 360, 500000)

    expected_string = "Your monthly payment = 3497!\nOverpayment = 758920"
    assert result_string == expected_string


def test_handle_annuity_calculates_principal() -> None:
    # Arrange
    args = Namespace(payment=3500, periods=360, interest=7.5, principal=None)
    mock_result = LoanResult(principal=500418, overpayment=759582)

    with patch(
        CALCULATE_ANNUITY_PRINCIPAL_PATH, return_value=mock_result
    ) as mock_calculate:
        # Act
        result_string = handle_annuity(args)

    # Assert
    expected_interest = 7.5 / (12 * 100)
    mock_calculate.assert_called_once_with(expected_interest, 360, 3500)

    expected_string = "Your loan principal = 500418!\nOverpayment = 759582"
    assert result_string == expected_string


def test_handle_annuity_invalid_args_exits() -> None:
    # Arrange: All arguments are provided, which is an error
    args = Namespace(payment=3500, periods=360, interest=7.5, principal=500000)

    # Act & Assert: Check that SystemExit is raised with an exit code of 1
    with pytest.raises(SystemExit) as e:
        handle_annuity(args)
    assert e.type is SystemExit
    assert e.value.code == 1


def test_handle_diff_calculates_payments() -> None:
    # Arrange
    args = Namespace(principal=500000, periods=12, interest=10, payment=None)
    mock_payments = [43750, 43403, 43056]  # Sample payments
    mock_result = LoanResult(payments=mock_payments, overpayment=27083)

    with patch(CALCULATE_DIFF_PATH, return_value=mock_result) as mock_calculate:
        # Act
        result_string = handle_diff(args)

    # Assert
    expected_interest = 10 / (12 * 100)
    mock_calculate.assert_called_once_with(expected_interest, 12, 500000)

    expected_string = (
        "Month 1: payment is 43750\n"
        "Month 2: payment is 43403\n"
        "Month 3: payment is 43056\n\n"
        "Overpayment = 27083"
    )
    assert result_string == expected_string


def test_handle_diff_with_payment_arg_exits() -> None:
    # Arrange
    args = Namespace(principal=500000, periods=12, interest=10, payment=1000)

    # Act & Assert
    with pytest.raises(SystemExit) as e:
        handle_diff(args)
    assert e.type is SystemExit
    assert e.value.code == 1
