import datetime
from typing import Iterator, List

from . import debt_calculator, savings_calculator
from payment_calc import date_utils, save, sorting
from payment_calc.models import Debt, Outcome, SavingsAccount, Scenario


def build_projected_debt_reduction(
        scenario: Scenario,
        output_fp: str=None,
        sort_key: str='debt_name',
        reverse: bool=False,
        transpose: bool=False
) -> None:
    outcomes = build_monthly_outcomes(
        scenario.debts,
        scenario.savings_accounts,
        scenario.start_date,
        sort_key=sort_key,
        reverse=reverse
    )
    save.write_outcomes_to_file(output_fp, outcomes, transpose=transpose)


def build_monthly_outcomes(
        debts: List[Debt],
        savings_accounts: List[SavingsAccount],
        current_date: datetime.date,
        **kwargs
) -> Iterator[Outcome]:
    debts = sorting.sort_debts(debts, **kwargs)
    while True:
        current_date = date_utils.next_month(current_date)
        debt_outcomes = debt_calculator.reduce_debts_for_month(debts, current_date)
        savings_outcomes = savings_calculator.project_savings_for_month(savings_accounts, debt_outcomes, current_date)
        outcome = Outcome(
            effective_date=current_date,
            debt_outcomes=debt_outcomes,
            savings_outcomes=savings_outcomes
        )
        yield outcome
        if not outcome.outstanding_debt():
            break
        debts = debt_calculator.refresh_debts(debts, debt_outcomes)

