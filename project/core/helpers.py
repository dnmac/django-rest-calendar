import datetime


def get_dates(start_date):
    week_number = start_date.isocalendar()[1]
    dates = [
            start_date + datetime.timedelta(days=i)
            for i in range(0 - start_date.weekday(), 7 - start_date.weekday())
        ]

    return dates
