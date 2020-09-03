import pytest

from payment_calc.models.scenario import Debt, DebtPayment


@pytest.fixture(scope='module')
def debt() -> Debt:
    return Debt(
        debt_name='jazz',
        debt_total=100,
        payments=[
            DebtPayment(
                amount=10,
                start_date='2020-01',
                end_date='2020-06'
            )
        ],
        interest_rate=0.12
    )

