import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DebtOutcome:
    debt_name: str
    debt_total: float
    payment_sum: float


@dataclass
class Outcome:
    effective_date: datetime.date
    debt_outcomes: List[DebtOutcome]

    def outstanding_debt(self) -> bool:
        """Determine if any of the outcome contains any outstanding debts"""
        return sum(d.debt_total for d in self.debt_outcomes) > 0

