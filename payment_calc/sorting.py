from typing import Any, List

from payment_calc.models import Debt


def sort_debts(
        debts: List[Debt],
        sort_key: str='debt_total',
        reverse: bool=False
) -> List[Debt]:
    settled = set(filter_settled(debts))
    unsettled = sorted(
        list(set(debts) - settled),
        key=lambda x: _sort_debt(x, sort_key),
        reverse=reverse
    )
    return list(settled) + unsettled


def _sort_debt(debt: Debt, sort_key: str) -> Any:
    if sort_key == 'payments':
        return sum(payment.amount for payment in debt.payments)

    return getattr(debt, sort_key)


def sort_settled_on_top(debts: List[Debt]) -> List[Debt]:
    settled = filter_settled(debts)
    unsettled = list(d for d in debts if d not in settled)
    return settled + unsettled


def filter_settled(debts: List[Debt]) -> List[Debt]:
    return list(filter(lambda x: x.debt_total <= 0, debts))

