from typing import Any, List

from payment_calc.models import Debt


def sort_debts(
        debts: List[Debt],
        sort_key: str='debt_total',
        reverse: bool=False
) -> List[Debt]:
    settled = set(
        debt
        for debt in debts
        if debt.debt_total <= 0
    )
    remaining = sorted(
        list(set(debts) - settled),
        key=lambda x: _sort_debt(x, sort_key),
        reverse=reverse
    )
    return list(settled) + remaining


def _sort_debt(debt: Debt, sort_key: str) -> Any:
    if sort_key == 'payments':
        return sum(payment.amount for payment in debt.payments)

    return getattr(debt, sort_key)

