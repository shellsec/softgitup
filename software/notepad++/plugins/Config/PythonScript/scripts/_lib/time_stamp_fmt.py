# -*- coding: utf-8 -*-
"""
与「插入时间中文」一致的长串日期规则，供其它脚本复用。

中文示例：20260515-周五-第20周-距年底还有230天-第2季度-本季度还剩46天
"""
from datetime import date, datetime, timedelta


def _now(now=None):
    return now if now is not None else datetime.now()


def shift_days(days, now=None):
    """Return datetime offset by `days` (may be negative)."""
    return _now(now) + timedelta(days=days)


def format_cn(now=None):
    now = _now(now)
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
        date_part,
        week_part,
        week_number_part,
        days_remaining_part,
        quarter_part,
        quarter_days_remaining_part,
    )


def format_en(now=None):
    now = _now(now)
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
        date_part,
        week_part,
        week_number_part,
        days_remaining_part,
        quarter_part,
        quarter_days_remaining_part,
    )


def format_ymd_hm(now=None):
    """2026-08-05 11:44"""
    return _now(now).strftime("%Y-%m-%d %H:%M")


def format_iso(now=None):
    """2026-08-05T11:44:00"""
    return _now(now).strftime("%Y-%m-%dT%H:%M:%S")


def format_week_cn(now=None):
    """2026-W32 · 第32周 · 周三"""
    now = _now(now)
    iso = now.isocalendar()
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return "{}-W{:02d} · 第{}周 · {}".format(iso[0], iso[1], iso[1], days[now.weekday()])


def format_week_en(now=None):
    """2026-W32 · Week 32 · Wed"""
    now = _now(now)
    iso = now.isocalendar()
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return "{}-W{:02d} · Week {} · {}".format(iso[0], iso[1], iso[1], days[now.weekday()])
