import datetime
import io
import json
import sys
import os
from typing import List, Iterator, Tuple

from payment_calc import date_utils, save, sorting
from payment_calc.models import Debt, DebtOutcome, Outcome, Scenario


def build_projected_debt_reduction(
        scenario: Scenario,
        output_fp: str=None,
        sort_key: str='debt_name',
        reverse: bool=False,
        transpose: bool=False
) -> None:
    outcomes = reduce_debts(
        scenario.debts,
        scenario.start_date,
        sort_key=sort_key,
        reverse=reverse
    )
    save.write_outcomes_to_file(output_fp, outcomes, transpose=transpose)


def reduce_debts(debts: List[Debt], current_date: datetime.date, **kwargs) -> Iterator[Outcome]:
    debts = sorting.sort_debts(debts, **kwargs)
    while True:
        current_date = date_utils.next_month(current_date)
        outcome = reduce_debts_for_month(debts, current_date)
        yield outcome
        if not outcome.outstanding_debt():
            break
        debts = refresh_debts(debts, outcome)


def reduce_debts_for_month(
        debts: List[Debt],
        end_date: datetime.date
) -> Outcome:
    """Calculate debt reduction cycle for the amount of months between the provided dates"""
    debt_outcomes = []
    remainder = 0
    for i, debt in enumerate(debts):
        debt_outcome, remainder = reduce_debt(
            debt,
            end_date,
            remainder
        )
        debt_outcomes.append(debt_outcome)
    return Outcome(
        effective_date=end_date,
        debt_outcomes=debt_outcomes
    )


def reduce_debt(
        debt: Debt,
        current_date: datetime.date,
        remainder: float
) -> Tuple[DebtOutcome, float]:
    payment_total = sum_active_payments(debt, current_date) + remainder
    debt_total, remainder = subtract_with_remainder(
        debt.debt_total,
        payment_total,
        debt.interest_rate
    )
    debt_outcome = DebtOutcome(
        debt_name=debt.debt_name,
        debt_total=debt_total
    )
    return debt_outcome, remainder


def refresh_debts(debts: List[Debt], last_outcome: DebtOutcome) -> List[Debt]:
    """
    Return a list of debts with the debt totals from the last outcome.
    List will be ordered with the settled debts at the top.
    """
    def _map_debt(debt: Debt) -> Debt:
        for debt_outcome in last_outcome.debt_outcomes:
            if debt.debt_name == debt_outcome.debt_name:
                debt.debt_total = debt_outcome.debt_total
        return debt

    return sorting.sort_settled_on_top(
        debts=list(map(_map_debt, debts))
    )


def sum_active_payments(debt: Debt, current_date: datetime.date) -> float:
    return sum(
        p.amount
        for p in debt.payments
        if p.is_active(current_date)
    )


def subtract_with_remainder(
        value: float,
        payment: float,
        interest_rate: float
) -> Tuple[float, float]:
    value *= 1 + (interest_rate / 12)
    return max(value - payment, 0), max(payment - value, 0)

