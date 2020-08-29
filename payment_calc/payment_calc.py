import datetime
import io
import json
import sys
import os
from typing import List, Tuple

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

    outcomes = list()
    current_date = scenario.start_date
    while True:
        outcomes.append(reduce_debt(debts, scenario.start_date, current_date))
        if not outcomes[-1].outstanding_debt():
            break
        current_date = date_utils.next_month(current_date)
    save.write_outcomes_to_file(output_fp, outcomes)


def reduce_debt(
        debts: List[Debt],
        start_date: datetime.date,
        end_date: datetime.date
) -> Outcome:
    """Calculate debt reduction cycle for the amount of months between the provided dates"""
    payment_clocks = date_utils.month_diff(end_date, start_date)
    debt_outcomes = []
    remainder = 0
    for i, debt in enumerate(debts):
        payment_total = (sum(debt.payments) * payment_clocks) + remainder
        debt_total, remainder = subtract_with_remainder(debt.debt_total, payment_total, debt.interest_rate)
        debt_outcome = DebtOutcome(
            debt_name=debt.debt_name,
            debt_total=debt_total
        )
        debt_outcomes.append(debt_outcome)
    return Outcome(
        effective_date=end_date,
        debt_outcomes=debt_outcomes
    )


def subtract_with_remainder(value, payment, interest_rate) -> Tuple[float, float]:
    value *= 1 + (interest_rate / 12)
    return max(value - payment, 0), max(payment - value, 0)

