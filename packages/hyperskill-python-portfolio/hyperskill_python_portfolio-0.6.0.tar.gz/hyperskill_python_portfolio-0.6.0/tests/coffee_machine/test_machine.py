"""Unit tests for the CoffeeMachine class."""

import unittest
from io import StringIO
from unittest.mock import patch

from hyperskill_python_portfolio.coffee_machine.machine import CoffeeMachine
from hyperskill_python_portfolio.coffee_machine.models import State


class TestCoffeeMachine(unittest.TestCase):
    """Test suite for the CoffeeMachine."""

    def setUp(self) -> None:
        """Create a fresh machine instance for test isolation."""
        self.machine = CoffeeMachine(water=400, milk=540, beans=120, cups=9, money=550)

    def test_buy_espresso_success(self) -> None:
        """Test a successful purchase of an espresso."""
        # Initial state check
        self.assertEqual(self.machine.state, State.MAIN_MENU)

        # Action: buy
        self.machine.process_input("buy")
        self.assertEqual(self.machine.state, State.CHOOSING_COFFEE)

        # Action: choose espresso (1)
        # We use a patch to capture the print output
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.machine.process_input("1")
            self.assertEqual(
                fake_out.getvalue().strip(),
                "I have enough resources, making you a coffee!",
            )

        # Verify final state and resources
        self.assertEqual(self.machine.state, State.MAIN_MENU)
        self.assertEqual(self.machine.water, 150)  # 400 - 250
        self.assertEqual(self.machine.beans, 104)  # 120 - 16
        self.assertEqual(self.machine.cups, 8)
        self.assertEqual(self.machine.money, 554)  # 550 + 4

    def test_buy_latte_insufficient_water(self) -> None:
        """Test a failed purchase due to insufficient resources."""
        # Set water to a low value for this specific test
        self.machine.water = 100

        # Action: buy -> choose latte (2)
        self.machine.process_input("buy")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.machine.process_input("2")
            self.assertEqual(fake_out.getvalue().strip(), "Sorry, not enough water!")

        # Verify state and that resources have NOT changed
        self.assertEqual(self.machine.state, State.MAIN_MENU)
        self.assertEqual(self.machine.water, 100)  # Unchanged
        self.assertEqual(self.machine.money, 550)  # Unchanged

    def test_full_fill_cycle(self) -> None:
        """Test the multi-step fill process."""
        self.machine.process_input("fill")
        self.assertEqual(self.machine.state, State.FILLING_WATER)

        self.machine.process_input("1000")
        self.assertEqual(self.machine.state, State.FILLING_MILK)

        self.machine.process_input("50")
        self.assertEqual(self.machine.state, State.FILLING_BEANS)

        self.machine.process_input("20")
        self.assertEqual(self.machine.state, State.FILLING_CUPS)

        self.machine.process_input("5")
        self.assertEqual(self.machine.state, State.MAIN_MENU)

        # Verify final resources
        self.assertEqual(self.machine.water, 1400)  # 400 + 1000
        self.assertEqual(self.machine.milk, 590)  # 540 + 50
        self.assertEqual(self.machine.beans, 140)  # 120 + 20
        self.assertEqual(self.machine.cups, 14)  # 9 + 5

    def test_take_money(self) -> None:
        """Test the take action."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.machine.process_input("take")
            self.assertEqual(fake_out.getvalue().strip(), "I gave you $550")

        # Verify money is now zero
        self.assertEqual(self.machine.money, 0)
        self.assertEqual(self.machine.state, State.MAIN_MENU)

    def test_exit_command(self) -> None:
        """Test the exit command transitions to SHUTDOWN state."""
        self.assertTrue(self.machine.is_running)
        self.machine.process_input("exit")
        self.assertEqual(self.machine.state, State.SHUTDOWN)
        self.assertFalse(self.machine.is_running)


if __name__ == "__main__":
    unittest.main()
