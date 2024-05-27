import datetime


def week_fraction(date: datetime.datetime = datetime.datetime.now()):
    y_now = int(date.strftime("%Y"))
    holidays = {
        "winter": {
            "start": datetime.date(y_now, 12, 30),
            "end": datetime.date(y_now, 2, 6),
        },
        "summer": {
            "start": datetime.date(y_now, 6, 4),
            "end": datetime.date(y_now, 9, 1),
        }
    }
    w_start = holidays["winter"]["start"].timetuple().tm_yday
    w_end = holidays["winter"]["end"].timetuple().tm_yday
    s_start = holidays["summer"]["start"].timetuple().tm_yday
    s_end = holidays["summer"]["end"].timetuple().tm_yday

    date_yday = date.timetuple().tm_yday
    if date_yday >= w_start and date_yday < w_end:
        return "Зимние каникулы"
    elif date_yday >= s_start and date_yday < s_end:
        return "Летние каникулы"
    else:
        if date.month < 9:
            weeks = date.isocalendar()[1] - \
                holidays["winter"]["end"].isocalendar()[1] + 1
        else:
            weeks = date.isocalendar()[1] - \
                holidays["summer"]["end"].isocalendar()[1] + 1
            
        if weeks % 2 == 0:
            week_type = "Знаменатель"
        else:
            week_type = "Числитель"
        
        return f"{weeks} неделя. {week_type}"
    