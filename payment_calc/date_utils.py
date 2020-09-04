import datetime


def month_diff(d1: datetime.date, d2: datetime.date) -> int:
    return abs(((d1.year - d2.year) * 12) + d1.month - d2.month)


def next_month(d: datetime.date) -> datetime.date:
    try:
        output = datetime.date(day=1, month=d.month + 1, year=d.year)
    except ValueError:
        if d.month == 12:
            output = datetime.date(day=1, month=1, year=d.year + 1)
        else:
            raise
    return output

