import datetime

from payment_calc.models import debt as under_test


def test_debt_payment__is_active__no_dates():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date=None,
        end_date=None
    )
    assert model.is_active(current_date) is True


def test_debt_payment__is_active__start_date__before_current():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date='2020-01',
        end_date=None
    )
    assert model.is_active(current_date) is True


def test_debt_payment__is_active__start_date__after_current():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date='2020-07',
        end_date=None
    )
    assert model.is_active(current_date) is False


def test_debt_payment__is_active__end_date__before_current():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date=None,
        end_date='2020-12',
    )
    assert model.is_active(current_date) is True


def test_debt_payment__is_active__end_date__after_current():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date=None,
        end_date='2020-01',
    )
    assert model.is_active(current_date) is False


def test_debt_payment__is_active__both_dates__in_range():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.DebtPayment(
        amount=100.00,
        start_date='2020-01',
        end_date='2020-12',
    )
    assert model.is_active(current_date) is True


def test_sum_active_payments__no_payments():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[],
        interest_rate=0.12
    )
    actual = model.sum_active_payments(current_date)
    assert actual == 0.00


def test_sum_active_payments__no_active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            under_test.DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-03'
            )
        ],
        interest_rate=0.12
    )
    actual = model.sum_active_payments(current_date)
    assert actual == 0.00


def test_sum_active_payments__active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            under_test.DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-12'
            )
        ],
        interest_rate=0.12
    )
    actual = model.sum_active_payments(current_date)
    assert actual == 10.00


def test_sum_active_payments__mixed_active_payments():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            under_test.DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-12'
            ),
            under_test.DebtPayment(
                amount=15,
                start_date='2020-01',
                end_date='2020-03'
            )
        ],
        interest_rate=0.12
    )
    actual = model.sum_active_payments(current_date)
    assert actual == 10.00


def test_sum_active_payments__mixed_carry_over():
    current_date = datetime.date(2020, 6, 1)
    model = under_test.Debt(
        debt_name='jazz',
        debt_total=0.00,
        payments=[
            under_test.DebtPayment(
                amount=10.00,
                carry_over=True
            ),
            under_test.DebtPayment(
                amount=15.00,
                carry_over=False
            )
        ],
        interest_rate=0.12
    )
    actual = model.sum_active_payments(current_date)
    assert actual == 10.00

