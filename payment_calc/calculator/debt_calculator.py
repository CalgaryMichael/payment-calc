import datetime
from typing import List, Tuple

from payment_calc import sorting
from payment_calc.models import Debt, DebtOutcome


def reduce_debts_for_month(
        debts: List[Debt],
        end_date: datetime.date
) -> List[DebtOutcome]:
    """Calculate debt reduction cycle for the amount of months between the provided dates"""
    debt_outcomes = []
    remainder = 0
    for debt in debts:
        debt_outcome, remainder = reduce_debt(
            debt,
            end_date,
            remainder
        )
        debt_outcomes.append(debt_outcome)
    return debt_outcomes


def reduce_debt(
        debt: Debt,
        current_date: datetime.date,
        remainder: float
) -> Tuple[DebtOutcome, float]:
    payment_sum = debt.sum_active_payments(current_date) + remainder
    debt_total, remainder = subtract_with_remainder(
        debt.debt_total,
        payment_sum,
        debt.interest_rate
    )
    debt_outcome = DebtOutcome(
        debt_name=debt.debt_name,
        debt_total=debt_total,
        payment_sum=payment_sum - remainder
    )
    return debt_outcome, remainder


def refresh_debts(debts: List[Debt], lastest_outcomes: List[DebtOutcome]) -> List[Debt]:
    """
    Return a list of debts with the debt totals from the last outcome.
    List will be ordered with the settled debts at the top.
    """
    def _map_debt(debt: Debt) -> Debt:
        for debt_outcome in lastest_outcomes:
            if debt.debt_name == debt_outcome.debt_name:
                debt.debt_total = debt_outcome.debt_total
        return debt

    return sorting.sort_settled_on_top(
        debts=list(map(_map_debt, debts))
    )


def subtract_with_remainder(
        value: float,
        payment: float,
        interest_rate: float
) -> Tuple[float, float]:
    value *= 1 + (interest_rate / 12)
    return max(value - payment, 0), max(payment - value, 0)

