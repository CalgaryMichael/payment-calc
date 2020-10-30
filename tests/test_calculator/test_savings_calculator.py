import datetime

from payment_calc.calculator import savings_calculator as under_test
from payment_calc.models import DebtOutcome, SavingsAccount, SavingsOutcome, SavingsPayment


def test_project_savings_for_month__no_savings_account():
    current_date = datetime.date(2020, 2, 1)
    savings_accounts = []
    debt_outcomes = [
        DebtOutcome(debt_name='jazz', debt_total=100, payment_sum=25)
    ]
    actual = under_test.project_savings_for_month(savings_accounts, debt_outcomes, current_date)
    assert actual == []


def test_project_savings_for_month__with_savings_account():
    current_date = datetime.date(2020, 2, 1)
    savings_accounts = [
        SavingsAccount(
            name='Savings Account 1',
            apy=0.00,
            initial_capital=100.00,
            payments=[SavingsPayment(amount=50.00)],
            projected_date=None
        )
    ]
    debt_outcomes = [
        DebtOutcome(debt_name='jazz', debt_total=100, payment_sum=25)
    ]
    actual = under_test.project_savings_for_month(savings_accounts, debt_outcomes, current_date)
    expected = [
        SavingsOutcome(
            savings_name='Savings Account 1',
            savings_total=150.00,
            contribution=50.00
        )
    ]
    assert actual == expected


def test_filter_active__no_projected_date():
    current_date = datetime.date(2020, 2, 1)
    savings_accounts = [
        SavingsAccount(
            name='Savings Account 1',
            apy=0.00,
            initial_capital=100.00,
            payments=[],
            projected_date=None
        )
    ]
    actual = under_test.filter_active(savings_accounts, current_date)
    assert list(actual) == savings_accounts


def test_filter_active__active():
    current_date = datetime.date(2020, 2, 1)
    savings_accounts = [
        SavingsAccount(
            name='Savings Account 1',
            apy=0.00,
            initial_capital=100.00,
            payments=[],
            projected_date=datetime.date(2020, 3, 1)
        )
    ]
    actual = under_test.filter_active(savings_accounts, current_date)
    assert list(actual) == savings_accounts


def test_filter_active__inactive():
    current_date = datetime.date(2020, 2, 1)
    savings_accounts = [
        SavingsAccount(
            name='Savings Account 1',
            apy=0.00,
            initial_capital=100.00,
            payments=[],
            projected_date=datetime.date(2020, 1, 1)
        )
    ]
    actual = under_test.filter_active(savings_accounts, current_date)
    assert list(actual) == []

