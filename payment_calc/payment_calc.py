import datetime
import io
import json
import sys
import os

from payment_calc.models import Scenario


def decrease_debt(scenario, sort_key='debt_name', reverse=False):
    debts = sorted(scenario.debts, key=lambda x: getattr(x, sort_key), reverse=reverse)

    start_date = scenario.start_date
    months = 1
    remainder = 0
    while sum(d.debt_total for d in debts) > 0:
        date = start_date + datetime.timedelta(days=30 * months)
        print()
        print(f'{date.month} {date.year}')
        print('----------------')
        for i, debt in enumerate(debts):
            payment_total = sum(debt.payments) + remainder
            debt_total, remainder = subtract_with_remainder(debt.debt_total, payment_total, debt.interest_rate)
            debts[i].debt_total = debt_total
            print(f'{debt.debt_name} - {round(debt_total, 2)}')
        months += 1



def subtract_with_remainder(value, payment, interest_rate):
    value *= 1 + (interest_rate / 12)
    return max(value - payment, 0), max(payment - value, 0)

