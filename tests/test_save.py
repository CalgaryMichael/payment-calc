import datetime

from payment_calc import save as under_test
from payment_calc.models.outcome import DebtOutcome, Outcome


def test_build_output_data_shape__not_transposed():
    outcomes = [
        Outcome(
            effective_date=datetime.date(2020, 1, 1),
            debt_outcomes=[
                DebtOutcome(debt_name='jazz 1', debt_total=100.00),
                DebtOutcome(debt_name='jazz 2', debt_total=200.00)
            ]
        ),
        Outcome(
            effective_date=datetime.date(2020, 2, 1),
            debt_outcomes=[
                DebtOutcome(debt_name='jazz 1', debt_total=50.00),
                DebtOutcome(debt_name='jazz 2', debt_total=100.00)
            ]
        )
    ]
    actual = under_test.build_output_data_shape(outcomes, transpose=False)
    expected = [
        {
            'effective_date': datetime.date(2020, 1, 1),
            'debt_outcomes': [
                {'debt_name': 'jazz 1', 'debt_total': 100.00},
                {'debt_name': 'jazz 2', 'debt_total': 200.00},
            ]
        },
        {
            'effective_date': datetime.date(2020, 2, 1),
            'debt_outcomes': [
                {'debt_name': 'jazz 1', 'debt_total': 50.00},
                {'debt_name': 'jazz 2', 'debt_total': 100.00},
            ]
        }
    ]
    assert actual == expected


def test_build_output_data_shape__transposed():
    outcomes = [
        Outcome(
            effective_date=datetime.date(2020, 1, 1),
            debt_outcomes=[
                DebtOutcome(debt_name='jazz 1', debt_total=100.00),
                DebtOutcome(debt_name='jazz 2', debt_total=200.00)
            ]
        ),
        Outcome(
            effective_date=datetime.date(2020, 2, 1),
            debt_outcomes=[
                DebtOutcome(debt_name='jazz 1', debt_total=50.00),
                DebtOutcome(debt_name='jazz 2', debt_total=100.00)
            ]
        )
    ]
    actual = under_test.build_output_data_shape(outcomes, transpose=True)
    expected = [
        {
            'debt_name': 'jazz 1',
            'debt_total': [
                {'effective_date': datetime.date(2020, 1, 1), 'debt_total': 100.00},
                {'effective_date': datetime.date(2020, 2, 1), 'debt_total': 50.00}
            ]
        },
        {
            'debt_name': 'jazz 2',
            'debt_total': [
                {'effective_date': datetime.date(2020, 1, 1), 'debt_total': 200.00},
                {'effective_date': datetime.date(2020, 2, 1), 'debt_total': 100.00}
            ]
        }
    ]
    assert actual == expected

