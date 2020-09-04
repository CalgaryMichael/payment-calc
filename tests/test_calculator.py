import datetime
from payment_calc import calculator as under_test
from payment_calc.models.outcome import DebtOutcome, Outcome
from payment_calc.models.scenario import Debt, DebtPayment


def test_reduce_debt__no_remainder(debt: Debt):
    actual_debt_outcome, actual_remainder = under_test.reduce_debt(
        debt=debt,
        current_date=datetime.date(2020, 3, 1),
        remainder=0.00
    )
    expected_debt_outcome = DebtOutcome(debt_name='jazz', debt_total=91.00)
    expected_remainder = 0.00
    assert actual_debt_outcome == expected_debt_outcome
    assert actual_remainder == expected_remainder


def test_reduce_debt__with_remainder(debt: Debt):
    actual_debt_outcome, actual_remainder = under_test.reduce_debt(
        debt=debt,
        current_date=datetime.date(2020, 3, 1),
        remainder=120.00
    )
    expected_debt_outcome = DebtOutcome(debt_name='jazz', debt_total=0.00)
    expected_remainder = 29.00
    assert actual_debt_outcome == expected_debt_outcome
    assert actual_remainder == expected_remainder


def test_refresh_debts__no_change():
    debts = [
        Debt(
            debt_name='jazz',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        )
    ]
    outcome = Outcome(
        effective_date=None,
        debt_outcomes=[
            DebtOutcome(
                debt_name='jazz',
                debt_total=50.00
            )
        ]
    )
    actual = under_test.refresh_debts(debts, outcome)
    assert actual == debts


def test_refresh_debts__debt_reduced():
    debts = [
        Debt(
            debt_name='jazz',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        )
    ]
    outcome = Outcome(
        effective_date=None,
        debt_outcomes=[
            DebtOutcome(
                debt_name='jazz',
                debt_total=50.00
            )
        ]
    )
    actual = under_test.refresh_debts(debts, outcome)
    expected = [
        Debt(
            debt_name='jazz',
            debt_total=50.00,
            payments=[DebtPayment(amount=10.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        )
    ]
    assert actual == expected


def test_refresh_debts__settled_at_top():
    debts = [
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        )
    ]
    outcome = Outcome(
        effective_date=None,
        debt_outcomes=[
            DebtOutcome(
                debt_name='jazz 1',
                debt_total=50.00
            ),
            DebtOutcome(
                debt_name='jazz 2',
                debt_total=0.00
            )
        ]
    )
    actual = under_test.refresh_debts(debts, outcome)
    expected = [
        Debt(
            debt_name='jazz 2',
            debt_total=0.00,
            payments=[DebtPayment(amount=25.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=50.00,
            payments=[DebtPayment(amount=10.00, start_date='2020-01', end_date='2020-06')],
            interest_rate=0.12
        )
    ]
    assert actual == expected


def test_sum_active_payments__no_payments():
    current_date = datetime.date(2020, 6, 1)
    model = Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[],
        interest_rate=0.12
    )
    actual = under_test.sum_active_payments(model, current_date)
    assert actual == 0.00


def test_sum_active_payments__no_active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-03'
            )
        ],
        interest_rate=0.12
    )
    actual = under_test.sum_active_payments(model, current_date)
    assert actual == 0.00


def test_sum_active_payments__active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-12'
            )
        ],
        interest_rate=0.12
    )
    actual = under_test.sum_active_payments(model, current_date)
    assert actual == 10.00


def test_sum_active_payments__mixed_active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-12'
            ),
            DebtPayment(
                amount=15,
                start_date='2020-01',
                end_date='2020-03'
            )
        ],
        interest_rate=0.12
    )
    actual = under_test.sum_active_payments(model, current_date)
    assert actual == 10.00


def test_subtract_with_remainder__no_remainder():
    actual = under_test.subtract_with_remainder(100.00, 10.00, 0.12)
    assert actual == (91.00, 0.00)


def test_subtract_with_remainder__with_remainder():
    actual = under_test.subtract_with_remainder(100.00, 200.00, 0.12)
    assert actual == (0.00, 99.00)

