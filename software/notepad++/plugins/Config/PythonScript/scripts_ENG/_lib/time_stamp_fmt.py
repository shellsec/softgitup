# -*- coding: utf-8 -*-
"""Rich date string (English), same rules as InsertTime.py."""
from datetime import date, datetime


def format_cn(now=None):
    if now is None:
        now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    days_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    week_part = days_of_week[now.weekday()]
    week_number = now.isocalendar()[1]
    week_number_part = "第{}周".format(week_number)
    end_of_year = date(now.year, 12, 31)
    days_remaining = (end_of_year - now.date()).days
    days_remaining_part = "距年底还有{}天".format(days_remaining)
    quarter = (now.month - 1) // 3 + 1
    quarter_part = "第{}季度".format(quarter)
    if quarter == 1:
        end_of_quarter = date(now.year, 3, 31)
    elif quarter == 2:
        end_of_quarter = date(now.year, 6, 30)
    elif quarter == 3:
        end_of_quarter = date(now.year, 9, 30)
    else:
        end_of_quarter = date(now.year, 12, 31)
    quarter_days_remaining = (end_of_quarter - now.date()).days
    quarter_days_remaining_part = "本季度还剩{}天".format(quarter_days_remaining)
    return "{}-{}-{}-{}-{}-{}".format(
        date_part, week_part, week_number_part, days_remaining_part, quarter_part, quarter_days_remaining_part
    )


def format_en(now=None):
    if now is None:
        now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    week_part = days_of_week[now.weekday()]
    week_number = now.isocalendar()[1]
    week_number_part = "Week {}".format(week_number)
    end_of_year = date(now.year, 12, 31)
    days_remaining = (end_of_year - now.date()).days
    days_remaining_part = "{} days to end of year".format(days_remaining)
    quarter = (now.month - 1) // 3 + 1
    quarter_part = "Q{}".format(quarter)
    if quarter == 1:
        end_of_quarter = date(now.year, 3, 31)
    elif quarter == 2:
        end_of_quarter = date(now.year, 6, 30)
    elif quarter == 3:
        end_of_quarter = date(now.year, 9, 30)
    else:
        end_of_quarter = date(now.year, 12, 31)
    quarter_days_remaining = (end_of_quarter - now.date()).days
    quarter_days_remaining_part = "{} days left in quarter".format(quarter_days_remaining)
    return "{}-{}-{}-{}-{}-{}".format(
        date_part, week_part, week_number_part, days_remaining_part, quarter_part, quarter_days_remaining_part
    )
