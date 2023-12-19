from datetime import date, timedelta


# func for getting list of dates for creating lessons till the first job has gone
def get_days_array(weekday):
    d = date.today()
    days_array = []
    if d.day < 15:
        stop_day = (d.replace(day=15) + timedelta(weeks=4)).replace(day=1) - timedelta(days=1)
    else:
        stop_day = (d.replace(day=15) + timedelta(weeks=8)).replace(day=1) - timedelta(days=1)
    for i in range(10):
        next_date = d + timedelta(days=(-d.weekday() + weekday), weeks=i)
        if (next_date > d) and (next_date <= stop_day):
            days_array.append(next_date)
    return days_array
