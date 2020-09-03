import datetime

from payment_calc.models import scenario as under_test


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

