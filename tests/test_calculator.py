import datetime
from payment_calc import calculator as under_test
from payment_calc.models.scenario import Debt, DebtPayment


def test_get_active_payments__no_payments():
    current_date = datetime.date(2020, 6, 1)
    model = Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[],
        interest_rate=0.12
    )
    actual = under_test.get_active_payments(model, current_date)
    assert actual == 0.00


def test_get_active_payments__no_active_payments():
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
    actual = under_test.get_active_payments(model, current_date)
    assert actual == 0.00


def test_get_active_payments__active_payments():
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
    actual = under_test.get_active_payments(model, current_date)
    assert actual == 10.00


def test_get_active_payments__mixed_active_payments():
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
    actual = under_test.get_active_payments(model, current_date)
    assert actual == 10.00


def test_subtract_with_remainder__no_remainder():
    actual = under_test.subtract_with_remainder(100.00, 10.00, 0.12)
    assert actual == (91.00, 0.00)


def test_subtract_with_remainder__with_remainder():
    actual = under_test.subtract_with_remainder(100.00, 200.00, 0.12)
    assert actual == (0.00, 99.00)

