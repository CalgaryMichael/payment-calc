import datetime

from payment_calc import date_utils as under_test


def test_month_diff__no_difference():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 1, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 0    


def test_month_diff__first_in_future():
    d1 = datetime.date(2020, 3, 1)
    d2 = datetime.date(2020, 1, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 2


def test_month_diff__second_in_future():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 3, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 2


def test_month_diff__year__first_in_future():
    d1 = datetime.date(2020, 3, 1)
    d2 = datetime.date(2019, 1, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 14


def test_month_diff__year__second_in_future():
    d1 = datetime.date(2019, 1, 1)
    d2 = datetime.date(2020, 3, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 14


def test_month_diff__days__first_in_future():
    d1 = datetime.date(2020, 1, 15)
    d2 = datetime.date(2020, 1, 1)
    diff = under_test.month_diff(d1, d2)
    assert diff == 0


def test_month_diff__days__second_in_future():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 1, 15)
    diff = under_test.month_diff(d1, d2)
    assert diff == 0

