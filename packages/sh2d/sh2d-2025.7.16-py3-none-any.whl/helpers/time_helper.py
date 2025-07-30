# -*- encoding: utf-8 -*-

'''
@File    :   time_helper.py
@Time    :   2025/07/16 12:16:08
@Author  :   test233
@Version :   1.0
'''


import time
from typing import Union


def datetime_to_str(dt: Union[time.struct_time, float], fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    将时间对象或时间戳转换为格式化时间字符串。
    Args:
        dt (Union[time.struct_time, float]): 时间对象（struct_time）或时间戳。
        fmt (str): 格式化字符串，默认为 '%Y-%m-%d %H:%M:%S'。
    Returns:
        str: 格式化后的时间字符串。
    """
    if isinstance(dt, float):
        dt = time.localtime(dt)  # 将时间戳转换为 struct_time
    return time.strftime(fmt, dt)


def str_to_datetime(time_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> time.struct_time:
    """
    将格式化时间字符串转换为时间对象。
    Args:
        time_str (str): 格式化时间字符串。
        fmt (str): 格式化字符串，默认为 '%Y-%m-%d %H:%M:%S'。
    Returns:
        time.struct_time: 时间对象。
    Raises:
        ValueError: 如果时间字符串与格式不匹配，抛出异常。
    """
    return time.strptime(time_str, fmt)


def get_time_before_seconds(seconds: int) -> float:
    """
    获取当前时间几秒前的时间戳。
    Args:
        seconds (int): 秒数。
    Returns:
        float: 几秒前的时间戳。
    """
    return time.time() - seconds


def get_time_before_minutes(minutes: int) -> float:
    """
    获取当前时间几分钟前的时间戳。
    Args:
        minutes (int): 分钟数。
    Returns:
        float: 几分钟前的时间戳。
    """
    return time.time() - minutes * 60


def get_time_before_hours(hours: int) -> float:
    """
    获取当前时间几小时前的时间戳。
    Args:
        hours (int): 小时数。
    Returns:
        float: 几小时前的时间戳。
    """
    return time.time() - hours * 3600


def get_time_before_days(days: int) -> float:
    """
    获取当前时间几天前的时间戳。
    Args:
        days (int): 天数。
    Returns:
        float: 几天前的时间戳。
    """
    return time.time() - days * 86400


def get_time_after_seconds(seconds: int) -> float:
    """
    获取当前时间几秒后的时间戳。
    Args:
        seconds (int): 秒数。
    Returns:
        float: 几秒后的时间戳。
    """
    return time.time() + seconds


def get_time_after_minutes(minutes: int) -> float:
    """
    获取当前时间几分钟后的时间戳。
    Args:
        minutes (int): 分钟数。
    Returns:
        float: 几分钟后的时间戳。
    """
    return time.time() + minutes * 60


def get_time_after_hours(hours: int) -> float:
    """
    获取当前时间几小时后的时间戳。
    Args:
        hours (int): 小时数。
    Returns:
        float: 几小时后的时间戳。
    """
    return time.time() + hours * 3600


def get_time_after_days(days: int) -> float:
    """
    获取当前时间几天后的时间戳。
    Args:
        days (int): 天数。
    Returns:
        float: 几天后的时间戳。
    """
    return time.time() + days * 86400


def get_time_after_months(months: int) -> float:
    """
    获取当前时间几个月后的时间戳。
    Args:
        months (int): 月数。
    Returns:
        float: 几个月后的时间戳。
    """
    now = time.localtime()
    year = now.tm_year + (now.tm_mon + months - 1) // 12
    month = (now.tm_mon + months - 1) % 12 + 1
    day = min(now.tm_mday, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year %
              400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return time.mktime((year, month, day, now.tm_hour, now.tm_min, now.tm_sec, now.tm_wday, now.tm_yday, now.tm_isdst))


def get_time_after_years(years: int) -> float:
    """
    获取当前时间几年后的时间戳。
    Args:
        years (int): 年数。
    Returns:
        float: 几年后的时间戳。
    """
    now = time.localtime()
    return time.mktime((now.tm_year + years, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, now.tm_wday, now.tm_yday, now.tm_isdst))


def time_diff_in_seconds(time1: float, time2: float) -> float:
    """
    计算两个时间相差的秒数。
    Args:
        time1 (float): 第一个时间戳。
        time2 (float): 第二个时间戳。
    Returns:
        float: 相差的秒数。
    """
    return time2 - time1


def time_diff_in_minutes(time1: float, time2: float) -> float:
    """
    计算两个时间相差的分钟数。
    Args:
        time1 (float): 第一个时间戳。
        time2 (float): 第二个时间戳。
    Returns:
        float: 相差的分钟数。
    """
    return (time2 - time1) / 60


def time_diff_in_hours(time1: float, time2: float) -> float:
    """
    计算两个时间相差的小时数。
    Args:
        time1 (float): 第一个时间戳。
        time2 (float): 第二个时间戳。
    Returns:
        float: 相差的小时数。
    """
    return (time2 - time1) / 3600


def time_diff_in_days(time1: float, time2: float) -> float:
    """
    计算两个时间相差的天数。
    Args:
        time1 (float): 第一个时间戳。
        time2 (float): 第二个时间戳。
    Returns:
        float: 相差的天数。
    """
    return (time2 - time1) / 86400


if __name__ == '__main__':
    # 测试代码
    print("测试时间对象与格式化时间字符串互转：")

    # 测试 datetime_to_str
    now = time.localtime()  # 获取当前时间对象
    formatted_str = datetime_to_str(now)
    print(f"当前时间对象: {now}")
    print(f"转换为字符串: {formatted_str}")

    # 测试 str_to_datetime
    time_str = "2023-10-01 12:34:56"
    dt = str_to_datetime(time_str)
    print(f"时间字符串: {time_str}")
    print(f"转换为时间对象: {dt}")

    # 测试自定义格式
    custom_fmt = '%Y/%m/%d %H-%M-%S'
    custom_str = datetime_to_str(now, custom_fmt)
    print(f"自定义格式字符串: {custom_str}")
    custom_dt = str_to_datetime(custom_str, custom_fmt)
    print(f"自定义格式转换回时间对象: {custom_dt}")

    # 测试时间戳转换
    timestamp = time.time()
    formatted_timestamp = datetime_to_str(timestamp)
    print(f"时间戳: {timestamp}")
    print(f"转换为字符串: {formatted_timestamp}")
    # 测试代码
    print("测试时间计算函数：")

    # 测试获取几秒前、几分钟、几小时、几天、几个月、几年后的时间
    print("10 秒前的时间戳:", get_time_before_seconds(10))
    print("5 分钟前的时间戳:", get_time_before_minutes(5))
    print("2 小时前的时间戳:", get_time_before_hours(2))
    print("3 天前的时间戳:", get_time_before_days(3))
    print("10 秒后的时间戳:", get_time_after_seconds(10))
    print("5 分钟后的时间戳:", get_time_after_minutes(5))
    print("2 小时后的时间戳:", get_time_after_hours(2))
    print("3 天后的时间戳:", get_time_after_days(3))
    print("1 个月后的时间戳:", get_time_after_months(1))
    print("2 年后的时间戳:", get_time_after_years(2))

    # 测试时间差计算函数
    time1 = time.time()
    time2 = time1 + 2 * 86400 + 3 * 3600 + 30 * 60 + 15  # 2 天 3 小时 30 分钟 15 秒后
    print("\n测试时间差计算函数：")
    print(f"时间1: {time1}, 时间2: {time2}")
    print("相差秒数:", time_diff_in_seconds(time1, time2))
    print("相差分钟数:", time_diff_in_minutes(time1, time2))
    print("相差小时数:", time_diff_in_hours(time1, time2))
    print("相差天数:", time_diff_in_days(time1, time2))
