# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import calendar


INITIAL_VALUE = float(os.environ["INITIAL_VALUE"])
FILENAME = "balance.json"


def _write(data, filename=FILENAME):
    with open(filename, "w+") as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def _bootstrap():
    data = {
        "balance": INITIAL_VALUE,
        "log": {},
        "current_avg": None,
    }
    _write(data)
    return True


def get_remaining_days():
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]-now.day+1


def get_info():
    try:
        with open(FILENAME, "r") as fp:
            data = json.loads(fp.read())
    except IOError as err:
        if "No such file" in err.strerror:
            _bootstrap()
            with open(FILENAME, "r") as fp:
                data = json.loads(fp.read())
    return data


def _update(new_balance, current_avg):
    data = get_info()
    data['balance'] = new_balance
    data['current_avg'] = current_avg
    _write(data)



def avg_by_day(value, days):
    return round(value/days, 2)


def input_value(total, spent):
    return total-spent


def log_daily(data, value, date, hour, reason):
    data = get_info()
    if date not in data['log']:
        data['log'][date] = []
    data['log'][date].append({"hour": hour, "value": value, "reason": reason })
    _write(data)

def try_shift_next_month(date):
    if calendar.monthrange(date.year, date.month)[1] == date.day:
        os.rename(FILENAME, "balance_%s.json" % date.month)
        _bootstrap()

def daily(day_spent, reason):
    now = datetime.now()
    date = now.strftime("%d/%m/%y")
    hour = now.strftime("%H:%M:%S")

    if not os.path.exists(FILENAME):
        _bootstrap()

    try_shift_next_month(now)

    data = get_info()
    balance = data['balance']

    new_balance = input_value(balance, day_spent)
    daily_avg = avg_by_day(new_balance, get_remaining_days())
    _update(new_balance, daily_avg)

    log_daily(data=data, value=day_spent, date=date, hour=hour, reason=reason)
    return {"saldo": new_balance, "avg": daily_avg}


if __name__ == '__main__':
    day_spent = int(raw_input("Qual o seu gasto de hoje? "))
    daily(day_spent)





