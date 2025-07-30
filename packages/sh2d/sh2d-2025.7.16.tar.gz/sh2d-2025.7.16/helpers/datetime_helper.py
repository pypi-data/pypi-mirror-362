# -*- encoding: utf-8 -*-

'''
@File    :   datetime_helper.py
@Time    :   2025/07/16 12:07:44
@Author  :   test233
@Version :   1.0
'''


import datetime
from typing import Union


def time_epoch_to_time_str(time_epoch: Union[int, float]) -> str:
    """
    将时间戳转换为格式化时间字符串。
    Args:
        time_epoch (Union[int, float]): 时间戳（秒或毫秒）。
    Returns:
        str: 格式化后的时间字符串，格式为 'YYYY-MM-DD HH:MM:SS'。
    """
    return datetime.datetime.fromtimestamp(time_epoch).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_str(dt: datetime.datetime = datetime.datetime.now(), fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    将日期时间对象转换为格式化时间字符串。
    Args:
        dt (datetime.datetime): 日期时间对象，默认当前时间。
        fmt (str): 格式化字符串，默认为 '%Y-%m-%d %H:%M:%S'。
    Returns:
        str: 格式化后的时间字符串。
    """
    return dt.strftime(fmt)
def str_to_datetime(time_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime.datetime:
    """
    将格式化时间字符串转换为日期时间对象。
    Args:
        time_str (str): 格式化时间字符串。
        fmt (str): 格式化字符串，默认为 '%Y-%m-%d %H:%M:%S'。
    Returns:
        datetime.datetime: 日期时间对象。
    Raises:
        ValueError: 如果时间字符串与格式不匹配，抛出异常。
    """
    return datetime.datetime.strptime(time_str, fmt)



def get_time_after_seconds(seconds: int) -> datetime.datetime:
    """
    获取当前时间几秒后的时间。
    Args:
        seconds (int): 秒数。
    Returns:
        datetime.datetime: 几秒后的时间。
    """
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)


def get_time_after_minutes(minutes: int) -> datetime.datetime:
    """
    获取当前时间几分钟后的时间。
    Args:
        minutes (int): 分钟数。
    Returns:
        datetime.datetime: 几分钟后的时间。
    """
    return datetime.datetime.now() + datetime.timedelta(minutes=minutes)


def get_time_after_hours(hours: int) -> datetime.datetime:
    """
    获取当前时间几小时后的时间。
    Args:
        hours (int): 小时数。
    Returns:
        datetime.datetime: 几小时后的时间。
    """
    return datetime.datetime.now() + datetime.timedelta(hours=hours)


def get_time_after_days(days: int) -> datetime.datetime:
    """
    获取当前时间几天后的时间。
    Args:
        days (int): 天数。
    Returns:
        datetime.datetime: 几天后的时间。
    """
    return datetime.datetime.now() + datetime.timedelta(days=days)


def get_time_after_months(months: int) -> datetime.datetime:
    """
    获取当前时间几个月后的时间。
    Args:
        months (int): 月数。
    Returns:
        datetime.datetime: 几个月后的时间。
    """
    now = datetime.datetime.now()
    year = now.year + (now.month + months - 1) // 12
    month = (now.month + months - 1) % 12 + 1
    day = min(now.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year %
              400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return now.replace(year=year, month=month, day=day)


def get_time_after_years(years: int) -> datetime.datetime:
    """
    获取当前时间几年后的时间。
    Args:
        years (int): 年数。
    Returns:
        datetime.datetime: 几年后的时间。
    """
    now = datetime.datetime.now()
    return now.replace(year=now.year + years)


def time_diff_in_seconds(time1: datetime.datetime, time2: datetime.datetime) -> float:
    """
    计算两个时间相差的秒数。
    Args:
        time1 (datetime.datetime): 第一个时间。
        time2 (datetime.datetime): 第二个时间。
    Returns:
        float: 相差的秒数。
    """
    return (time2 - time1).total_seconds()


def time_diff_in_minutes(time1: datetime.datetime, time2: datetime.datetime) -> float:
    """
    计算两个时间相差的分钟数。
    Args:
        time1 (datetime.datetime): 第一个时间。
        time2 (datetime.datetime): 第二个时间。
    Returns:
        float: 相差的分钟数。
    """
    return (time2 - time1).total_seconds() / 60


def time_diff_in_hours(time1: datetime.datetime, time2: datetime.datetime) -> float:
    """
    计算两个时间相差的小时数。
    Args:
        time1 (datetime.datetime): 第一个时间。
        time2 (datetime.datetime): 第二个时间。
    Returns:
        float: 相差的小时数。
    """
    return (time2 - time1).total_seconds() / 3600


def time_diff_in_days(time1: datetime.datetime, time2: datetime.datetime) -> float:
    """
    计算两个时间相差的天数。
    Args:
        time1 (datetime.datetime): 第一个时间。
        time2 (datetime.datetime): 第二个时间。
    Returns:
        float: 相差的天数。
    """
    return (time2 - time1).total_seconds() / 86400


if __name__ == '__main__':
    # 测试代码
    print("当前时间:", datetime.datetime.now())

    # 测试时间计算函数
    print("\n测试时间计算函数：")
    print("10 秒后的时间:", get_time_after_seconds(10))
    print("5 分钟后的时间:", get_time_after_minutes(5))
    print("2 小时后的时间:", get_time_after_hours(2))
    print("3 天后的时间:", get_time_after_days(3))
    print("1 个月后的时间:", get_time_after_months(1))
    print("2 年后的时间:", get_time_after_years(2))

    # 测试时间差计算函数
    time1 = datetime.datetime.now()
    time2 = time1 + datetime.timedelta(days=2, hours=3, minutes=30, seconds=15)
    print("\n测试时间差计算函数：")
    print(f"时间1: {time1}, 时间2: {time2}")
    print("相差秒数:", time_diff_in_seconds(time1, time2))
    print("相差分钟数:", time_diff_in_minutes(time1, time2))
    print("相差小时数:", time_diff_in_hours(time1, time2))
    print("相差天数:", time_diff_in_days(time1, time2))
    # 测试代码
    print("测试日期时间对象与格式化时间字符串互转：")
    
    # 测试 datetime_to_str
    now = datetime.datetime.now()
    formatted_str = datetime_to_str(now)
    print(f"当前时间对象: {now}")
    print(f"转换为字符串: {formatted_str}")
    
    # 测试 str_to_datetime
    time_str = "2023-10-01 12:34:56"
    dt = str_to_datetime(time_str)
    print(f"时间字符串: {time_str}")
    print(f"转换为日期时间对象: {dt}")
    
    # 测试自定义格式
    custom_fmt = '%Y/%m/%d %H-%M-%S'
    custom_str = datetime_to_str(now, custom_fmt)
    print(f"自定义格式字符串: {custom_str}")
    custom_dt = str_to_datetime(custom_str, custom_fmt)
    print(f"自定义格式转换回日期时间对象: {custom_dt}")