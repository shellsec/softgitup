# -*- coding: utf-8 -*-
from datetime import datetime, date

def insert_time():
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")  # 当前日期格式：YYYYMMDD
    days_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    week_part = days_of_week[now.weekday()]  # 当前星期几
    week_number = now.isocalendar()[1]  # 当前是第几周
    week_number_part = "第{}周".format(week_number)

    # 计算今年年底的日期
    end_of_year = date(now.year, 12, 31)
    days_remaining = (end_of_year - now.date()).days  # 当前日期到年底的天数
    days_remaining_part = "距年底还有{}天".format(days_remaining)

    # 计算当前季度
    quarter = (now.month - 1) // 3 + 1  # 当前季度
    quarter_part = "第{}季度".format(quarter)

    # 计算本季度的最后一天
    if quarter == 1:
        end_of_quarter = date(now.year, 3, 31)
    elif quarter == 2:
        end_of_quarter = date(now.year, 6, 30)
    elif quarter == 3:
        end_of_quarter = date(now.year, 9, 30)
    else:
        end_of_quarter = date(now.year, 12, 31)

    # 计算本季度还剩下多少天
    quarter_days_remaining = (end_of_quarter - now.date()).days
    quarter_days_remaining_part = "本季度还剩{}天".format(quarter_days_remaining)

    # 组合最终的字符串
    formatted_time = "{}-{}-{}-{}-{}-{}".format(
        date_part, week_part, week_number_part, days_remaining_part, quarter_part, quarter_days_remaining_part
    )
    editor.insertText(editor.getCurrentPos(), formatted_time)

insert_time()
