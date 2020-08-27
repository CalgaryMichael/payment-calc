import datetime
import io
import json
import sys
import os


def decrease_debt(debts, sort_key='debt_name', reverse=False):
    debts = sorted(debts, key=lambda x: x[sort_key], reverse=reverse)

    start_date = datetime.date.today()
    months = 1
    remainder = 0
    while sum(d['debt_total'] for d in debts) > 0:
        date = start_date + datetime.timedelta(days=30 * months)
        print()
        print(f'{date.month} {date.year}')
        print('----------------')
        for i, debt in enumerate(debts):
            payment_total = sum(debt['payment']) + remainder
            debt_total, remainder = subtract_with_remainder(debt['debt_total'], payment_total, debt['interest_rate'])
            debts[i]['debt_total'] = debt_total
            print(f'{debt["debt_name"]} - {round(debt_total, 2)}')
        months += 1



def subtract_with_remainder(value, payment, interest_rate):
    value *= 1 + (interest_rate / 12)
    return max(value - payment, 0), max(payment - value, 0)


if __name__ == '__main__':
    file_loc = os.path.abspath(sys.argv[1])
    with io.open(file_loc, 'r') as file_:
        debts = json.load(file_)
    decrease_debt(debts, sort_key='payment', reverse=True)

