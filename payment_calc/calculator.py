import datetime
import io
import json
import sys
import os
from typing import List, Iterator, Tuple

from payment_calc import date_utils, save
from payment_calc.models import Debt, DebtOutcome, Outcome, Scenario


def build_projected_debt_reduction(
        scenario: Scenario,
        output_fp: str=None,
        sort_key: str='debt_name',
        reverse: bool=False
) -> None:
    debts = sorted(
        scenario.debts,
        key=lambda x: getattr(x, sort_key),
        reverse=reverse
    )

    outcomes = reduce_debts(debts, scenario.start_date)
    save.write_outcomes_to_file(output_fp, outcomes)


def reduce_debts(debts: List[Debt], start_date: datetime.date) -> Iterator[Outcome]:
    current_date = start_date
    while True:
        outcome = reduce_debts_for_month(debts, start_date, current_date)
        yield outcome
        if not outcome.outstanding_debt():
            break
        current_date = date_utils.next_month(current_date)


def reduce_debts_for_month(
        debts: List[Debt],
        start_date: datetime.date,
        end_date: datetime.date
) -> Outcome:
    """Calculate debt reduction cycle for the amount of months between the provided dates"""
    payment_clocks = date_utils.month_diff(end_date, start_date)
    debt_outcomes = []
    remainder = 0
    for i, debt in enumerate(debts):
        debt_outcome, remainder = reduce_debt(
            debt,
            end_date,
            payment_clocks,
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
        payment_clocks: int,
        remainder: float
) -> Tuple[DebtOutcome, float]:
    payment_total = (sum_active_payments(debt, current_date) * payment_clocks) + remainder
    debt_total, remainder = subtract_with_remainder(debt.debt_total, payment_total, debt.interest_rate)
    debt_outcome = DebtOutcome(
        debt_name=debt.debt_name,
        debt_total=debt_total
    )
    return debt_outcome, remainder


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

