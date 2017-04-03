# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import calendar

INITIAL_VALUE = float(os.environ["INITIAL_VALUE"])


def _bootstrap():
    with open("balance.json", "w+") as fp:
        data = {
            "balance": INITIAL_VALUE,
            "remaining_days": get_remaining_days(), 
            "log": {},
            "current_avg": None,
        }
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def get_remaining_days():
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]-now.day


def get_info():
    with open("balance.json", "r") as fp:
        data = json.loads(fp.read())
    return data


def update_balance(new_balance):
    data = get_info()
    data['balance'] = new_balance
    with open("balance.json", "w") as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def update_avg(daily_avg):
    data = get_info()
    data['current_avg'] = daily_avg
    with open("balance.json", "w") as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def update_days():
    data = get_info()
    data['remaining_days'] = get_remaining_days()
    with open("balance.json", "w") as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def avg_by_day(value, days):
    return value/days


def input_value(total, spent):
    return total-spent

def log_daily(data, value, date):
    data = get_info()
    data['log'][date] = value
    with open("balance.json", "w") as fp:
        fp.write(json.dumps(data, sort_keys=True, indent=4))


def daily(day_spent):
    now = datetime.now()
    date = now.strftime("%d/%m/%y-%H:%M:%S")

    if not os.path.exists("balance.json"):
        _bootstrap()
 
    if calendar.monthrange(now.year, now.month)[1] == now.day:
        os.rename("balance.json", "balance_%s.json" % now.month)
        _bootstrap()

    data = get_info()
    balance = data['balance']
    remaining_days = get_remaining_days()

    new_balance = input_value(balance, day_spent)
    daily_avg = round(avg_by_day(new_balance, remaining_days), 2)
    update_avg(daily_avg)
    update_balance(new_balance)
    log_daily(data, day_spent, date)
    return {"saldo": new_balance, "avg": daily_avg}


if __name__ == '__main__':
    day_spent = int(raw_input("Qual o seu gasto de hoje? "))
    daily(day_spent)





