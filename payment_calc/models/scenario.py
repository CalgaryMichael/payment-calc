import datetime
import io
import json
import os
from dataclasses import dataclass
from typing import List


@dataclass
class Debt:
    """Reprsents the shape of a debt"""
    debt_name: str
    debt_total: float
    payments: List[float]
    interest_rate: float 


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
            debts=list(Debt(**d) for d in data['debts'])
        )

