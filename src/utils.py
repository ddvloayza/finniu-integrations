import random
import string
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def generate_random_letter(salt=4):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(salt))


def date_string():
    return date.today().strftime("%Y-%m-%d")


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def adjust_date(pre_investment_deadline_value, date=None):
    # Calcula la fecha objetivo
    date = date if date is not None else datetime.now()
    target_date = date + relativedelta(months=pre_investment_deadline_value)

    # Extrae el día del mes de la fecha objetivo
    day_of_month = target_date.day

    # Obtener el mes y año de la fecha objetivo
    month = target_date.month
    year = target_date.year

    # Ajustar la fecha según las condiciones dadas
    if 1 <= day_of_month <= 12:
        target_date = target_date.replace(day=15)
    elif 13 <= day_of_month <= 27:
        # Establecer el día al 30 del mes actual, teniendo en cuenta febrero
        if month == 2:
            if is_leap_year(year):
                target_date = target_date.replace(day=29)  # 29 en febrero bisiesto
            else:
                target_date = target_date.replace(day=28)  # 28 en febrero no bisiesto
        else:
            target_date = target_date.replace(day=30)
    elif day_of_month in {28, 29, 30, 31}:
        # Establecer el día al 15 del mes siguiente
        target_date += relativedelta(months=1)
        target_date = target_date.replace(day=15)

    return target_date