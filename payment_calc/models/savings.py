import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SavingsPayment:
    amount: float
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


@dataclass
class SavingsAccount:
    """Represents the shape of saving information"""
    name: str
    apy: float
    initial_capital: float
    payments: List[SavingsPayment]
    projected_date: Optional[datetime.date] = None

