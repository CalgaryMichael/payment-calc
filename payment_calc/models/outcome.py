import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class DebtOutcome:
    debt_name: str
    debt_total: float
    payment_sum: float


@dataclass
class SavingsOutcome:
    savings_name: str
    savings_total: float
    contribution: float


@dataclass
class Outcome:
    effective_date: datetime.date
    debt_outcomes: List[DebtOutcome]
    savings_outcomes: List[SavingsOutcome]

    def outstanding_debt(self) -> bool:
        """Determine if any of the outcome contains any outstanding debts"""
        return sum(d.debt_total for d in self.debt_outcomes) > 0

