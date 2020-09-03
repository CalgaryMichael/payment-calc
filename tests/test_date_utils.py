import datetime

from payment_calc import date_utils as under_test


def test_month_diff__no_difference():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 1, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 0


def test_month_diff__first_in_future():
    d1 = datetime.date(2020, 3, 1)
    d2 = datetime.date(2020, 1, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 2


def test_month_diff__second_in_future():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 3, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 2


def test_month_diff__year__first_in_future():
    d1 = datetime.date(2020, 3, 1)
    d2 = datetime.date(2019, 1, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 14


def test_month_diff__year__second_in_future():
    d1 = datetime.date(2019, 1, 1)
    d2 = datetime.date(2020, 3, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 14


def test_month_diff__days__first_in_future():
    d1 = datetime.date(2020, 1, 15)
    d2 = datetime.date(2020, 1, 1)
    actual = under_test.month_diff(d1, d2)
    assert actual == 0


def test_month_diff__days__second_in_future():
    d1 = datetime.date(2020, 1, 1)
    d2 = datetime.date(2020, 1, 15)
    actual = under_test.month_diff(d1, d2)
    assert actual == 0


def test_next_month__simple():
    beginning = datetime.date(2020, 1, 1)
    actual = under_test.next_month(beginning)
    expected = datetime.date(2020, 2, 1)
    assert actual == expected


def test_next_month__year_increment():
    beginning = datetime.date(2020, 12, 1)
    actual = under_test.next_month(beginning)
    expected = datetime.date(2021, 1, 1)
    assert actual == expected
