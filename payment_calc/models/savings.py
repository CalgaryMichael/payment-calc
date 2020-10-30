import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SavingsPayment:
    amount: float
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

    def is_active(self, current_date: datetime.date) -> bool:
        return (
            (self.start_date is None or self.start_date < current_date)
            and (self.end_date is None or self.end_date > current_date)
        )


@dataclass
class SavingsAccount:
    """Represents the shape of saving information"""
    name: str
    apy: float
    initial_capital: float
    payments: List[SavingsPayment]
    projected_date: Optional[datetime.date] = None

    @classmethod
    def of(cls, *args, **kwargs):
        kwargs['payments'] = list(SavingsPayment(**p) for p in kwargs.get('payments', []))
        return cls(*args, **kwargs)

    def sum_active_payments(self, current_date: datetime.date) -> float:
        """Returns the sum of all active payments for a given date"""
        return sum(
            p.amount
            for p in self.payments
            if p.is_active(current_date)
        )

