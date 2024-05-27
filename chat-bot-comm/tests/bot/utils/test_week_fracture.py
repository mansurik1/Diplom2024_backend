import datetime

from app.store.bot.utils.week_fraction import week_fraction


def test_date_now():
    date = datetime.datetime.now()
    res = week_fraction(date)
    assert res == "3 неделя. Числитель"

def test_summer_holiday():
    dates = [
        datetime.date(2024, 6, 4),
        datetime.date(2024, 6, 15),
        datetime.date(2024, 8, 15),
        datetime.date(2024, 8, 31)
    ]
    for date in dates:
        assert week_fraction(date) == "Летние каникулы"

def test_summer_borders():
    dates = [
        datetime.date(2024, 6, 3),
        datetime.date(2024, 6, 4),
        datetime.date(2024, 8, 31),
        datetime.date(2024, 9, 1)
    ]
    expects = [
        "18 неделя. Знаменатель",
        "Летние каникулы",
        "Летние каникулы",
        "1 неделя. Числитель"
    ]
    for date, expect in zip(dates, expects):
        assert week_fraction(date) == expect
