import datetime
import io
import json
from dataclasses import dataclass
from typing import List

from .debt import Debt
from .savings import SavingsAccount


@dataclass
class Scenario:
    """Represents the expected shape of a scenario file"""
    start_date: datetime.date
    debts: List[Debt]
    savings_accounts: List[SavingsAccount]

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
            debts=list(Debt.of(**d) for d in data.get('debts', [])),
            savings_accounts=list(SavingsAccount.of(**s) for s in data.get('savings_accounts', []))
        )

