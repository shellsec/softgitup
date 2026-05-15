# -*- coding: utf-8 -*-
from datetime import datetime, date

def insert_time():
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")  # Current date format: YYYYMMDD
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    week_part = days_of_week[now.weekday()]  # Current day of week
    week_number = now.isocalendar()[1]  # Current week number
    week_number_part = "Week {}".format(week_number)

    # Calculate end of year date
    end_of_year = date(now.year, 12, 31)
    days_remaining = (end_of_year - now.date()).days  # Days from current date to end of year
    days_remaining_part = "{} days to end of year".format(days_remaining)

    # Calculate current quarter
    quarter = (now.month - 1) // 3 + 1  # Current quarter
    quarter_part = "Q{}".format(quarter)

    # Calculate last day of current quarter
    if quarter == 1:
        end_of_quarter = date(now.year, 3, 31)
    elif quarter == 2:
        end_of_quarter = date(now.year, 6, 30)
    elif quarter == 3:
        end_of_quarter = date(now.year, 9, 30)
    else:
        end_of_quarter = date(now.year, 12, 31)

    # Calculate days remaining in current quarter
    quarter_days_remaining = (end_of_quarter - now.date()).days
    quarter_days_remaining_part = "{} days left in quarter".format(quarter_days_remaining)

    # Combine final string
    formatted_time = "{}-{}-{}-{}-{}-{}".format(
        date_part, week_part, week_number_part, days_remaining_part, quarter_part, quarter_days_remaining_part
    )
    editor.insertText(editor.getCurrentPos(), formatted_time)

insert_time()
