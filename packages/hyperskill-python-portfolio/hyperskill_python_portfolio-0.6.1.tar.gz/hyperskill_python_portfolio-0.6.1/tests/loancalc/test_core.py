from hyperskill_python_portfolio.loancalc.core import (
    calculate_annuity_payment,
    calculate_annuity_periods,
    calculate_annuity_principal,
    calculate_diff,
)


def test_annuity_payment() -> None:
    """Tests the calculation of a fixed monthly annuity payment."""
    res = calculate_annuity_payment(1 / 120, 12, 1000000)
    assert res.payment == 87916
    assert res.overpayment == 54992


def test_annuity_principal() -> None:
    """Tests the calculation of the loan principal for an annuity loan."""
    res = calculate_annuity_principal(5.6 / 1200, 120, 8722)
    assert res.principal == 800018
    assert res.overpayment == 246622


def test_annuity_periods() -> None:
    """Tests the calculation of the repayment period for an annuity loan."""
    res = calculate_annuity_periods(7.8 / 1200, 500000, 23000)
    assert res.periods == 24
    assert res.description is not None
    assert "year" in res.description
    assert res.overpayment == 52000


def test_diff() -> None:
    """Tests the calculation of differentiated payments."""
    res = calculate_diff(10 / 1200, 10, 1000000)
    assert len(res.payments) == 10
    assert res.payments[0] > res.payments[-1]
    assert res.overpayment == sum(res.payments) - 1000000
