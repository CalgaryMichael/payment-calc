import datetime
from typing import Iterator, List

from payment_calc.models import SavingsAccount, SavingsOutcome


def project_savings_for_month(
        savings_accounts: List[SavingsAccount],
        debt_rollover: float,
        current_date: datetime.date
) -> List[SavingsOutcome]:
    savings_outcomes = []
    for savings_account in filter_active(savings_accounts, current_date):
        contribution = calculate_total_contribution(
            savings_account.initial_capital,
            savings_account.sum_active_payments(current_date),
            savings_account.apy,
            debt_rollover
        )
        savings_total = savings_account.initial_capital + contribution
        savings_outcomes.append(SavingsOutcome(
            savings_name=savings_account.name,
            savings_total=savings_total,
            contribution=contribution
        ))
    return savings_outcomes


def calculate_total_contribution(
        initial_capital: float,
        base_contribution: float,
        apy: float,
        debt_rollover: float
) -> float:
    interest = initial_capital * (apy / 12)
    return round(interest + base_contribution + debt_rollover, 2)



def filter_active(
        savings_accounts: List[SavingsAccount],
        current_date: datetime.date
) -> Iterator[SavingsAccount]:
    return filter(
        lambda x: x.projected_date is None or x.projected_date >= current_date,
        savings_accounts
    )


def refresh_savings(savings_accounts: List[SavingsAccount], lastest_outcomes: List[SavingsOutcome]) -> List[SavingsAccount]:
    """Return a list of savings accounts with the savings totals from the last outcome"""
    def _map_savings(savings_account: SavingsAccount) -> SavingsAccount:
        for savings_outcome in lastest_outcomes:
            if savings_account.name == savings_outcome.savings_name:
                savings_account.initial_capital = savings_outcome.savings_total
        return savings_account

    return list(map(_map_savings, savings_accounts))

