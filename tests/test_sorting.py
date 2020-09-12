from payment_calc import sorting as under_test
from payment_calc.models.debt import Debt, DebtPayment


def test_sort_debts():
    debts = [
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        )
    ]
    actual = under_test.sort_debts(debts, sort_key='debt_total', reverse=False)
    expected = [
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        )
    ]
    assert actual == expected


def test_sort_debts__settled_on_top():
    debts = [
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 3',
            debt_total=0.00,
            payments=[DebtPayment(amount=50.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        )
    ]
    actual = under_test.sort_debts(debts, sort_key='debt_total', reverse=False)
    expected = [
        Debt(
            debt_name='jazz 3',
            debt_total=0.00,
            payments=[DebtPayment(amount=50.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        )
    ]
    assert actual == expected


def test_sort_debts__by_payment():
    debts = [
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=15.00), DebtPayment(amount=15.00)],
            interest_rate=0.12
        )
    ]
    actual = under_test.sort_debts(debts, sort_key='payments', reverse=True)
    expected = [
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=15.00), DebtPayment(amount=15.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        )
    ]
    assert actual == expected


def test_sort_debts__reverse__settled_on_top():
    debts = [
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 3',
            debt_total=0.00,
            payments=[DebtPayment(amount=50.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        )
    ]
    actual = under_test.sort_debts(debts, sort_key='debt_total', reverse=True)
    expected = [
        Debt(
            debt_name='jazz 3',
            debt_total=0.00,
            payments=[DebtPayment(amount=50.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 2',
            debt_total=200.00,
            payments=[DebtPayment(amount=25.00)],
            interest_rate=0.12
        ),
        Debt(
            debt_name='jazz 1',
            debt_total=100.00,
            payments=[DebtPayment(amount=10.00)],
            interest_rate=0.12
        )
    ]
    assert actual == expected

