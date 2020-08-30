import datetime
import io
import json
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DebtPayment:
    """Represents a single payment towards a debt"""
    amount: float
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

    def __init__(
            self,
            amount: float,
            start_date: Optional[str],
            end_date: Optional[str]
    ) -> None:
        self.amount = amount
        self.start_date = (
            datetime.datetime.strptime(start_date, '%Y-%m').date()
            if start_date
            else None
        )
        self.end_date = (
            datetime.datetime.strptime(end_date, '%Y-%m').date()
            if end_date
            else None
        )

    def is_active(self, current_date: datetime.date) -> bool:
        return (
            (self.start_date is None or self.start_date < current_date)
            and (self.end_date is None or self.end_date > current_date)
        )


@dataclass
class Debt:
    """Reprsents the shape of a debt"""
    debt_name: str
    debt_total: float
    payments: List[DebtPayment]
    interest_rate: float

    @classmethod
    def of(cls, *args, **kwargs):
        kwargs['payments'] = list(DebtPayment(**p) for p in kwargs.get('payments', []))
        return cls(*args, **kwargs)


@dataclass
class Scenario:
    """Represents the expected shape of a scenario file"""
    start_date: datetime.date
    debts: List[Debt]

    @classmethod
    def of(cls, fp):
        with io.open(fp, 'r') as file_:
            data = json.load(file_)

        # get the specified start date, or the beginning of the month
        start_date = (
            datetime.datetime.strptime(data['start_date'], '%Y-%m').date()
            if data.get('start_date')
            else datetime.date.today().replace(day=1)
        )
        return cls(
            start_date=start_date,
            debts=list(Debt.of(**d) for d in data['debts'])
        )

