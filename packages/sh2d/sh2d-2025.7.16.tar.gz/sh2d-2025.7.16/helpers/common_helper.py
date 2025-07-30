# -*- encoding: utf-8 -*-

'''
@File    :   common_helper.py
@Time    :   2025/07/16 12:06:52
@Author  :   test233
@Version :   1.0
'''


import time
from loguru import logger
from itertools import groupby
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

# 定义类型别名
T = TypeVar("T")  # 泛型类型
DictList = List[Dict[str, Any]]  # 字典列表类型
RangeList = List[List[int]]  # 范围列表类型
GroupedDict = Dict[str, DictList]  # 分组字典类型


def timer(func: Callable[..., T]) -> Callable[..., T]:
    """
    计时装饰器，用于测量函数执行时间
    :param func: 被装饰的函数
    :return: 装饰后的函数
    """
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录结束时间
        execution_time = end_time - start_time  # 计算执行时间
        logger.debug(f"Execution time: {execution_time} seconds")  # 打印执行时间
        return result  # 返回函数执行结果
    return wrapper


def debug(func: Callable[..., T]) -> Callable[..., T]:
    """
    调试装饰器，用于打印函数调用信息和返回值
    :param func: 被装饰的函数
    :return: 装饰后的函数
    """
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # 打印函数调用信息
        logger.debug(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)  # 执行函数
        logger.debug(f"{func.__name__} returned: {result}")  # 打印函数返回值
        return result  # 返回函数执行结果
    return wrapper


def exception_handler(func: Callable[..., T]) -> Callable[..., T]:
    """
    异常处理装饰器，用于捕获并处理函数中的异常
    :param func: 被装饰的函数
    :return: 装饰后的函数
    """
    def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
        try:
            return func(*args, **kwargs)  # 执行函数
        except Exception as e:
            logger.exception(f"An exception occurred: {str(e)}")  # 打印异常信息
            # 可选：记录日志或执行其他错误处理逻辑
    return wrapper


def validate_input(*validations: Any) -> Callable[..., Callable[..., T]]:
    """
    输入验证装饰器，用于验证函数参数的合法性
    :param validations: 验证规则列表或字典
    :return: 装饰后的函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            for i, val in enumerate(args):  # 验证位置参数
                if i < len(validations):
                    if not validations[i](val):
                        raise ValueError(f"Invalid argument: {val}")
            for key, val in kwargs.items():  # 验证关键字参数
                if key in validations[len(args):]:
                    if not validations[len(args):][key](val):
                        raise ValueError(f"Invalid argument: {key}={val}")
            return func(*args, **kwargs)  # 执行函数
        return wrapper
    return decorator


def retry(max_attempts: int, delay: int = 1) -> Callable[..., Callable[..., T]]:
    """
    重试装饰器，用于在函数失败时重试
    :param max_attempts: 最大重试次数
    :param delay: 重试间隔时间（秒）
    :return: 装饰后的函数
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
            attempts = 0
            while attempts < max_attempts:  # 重试逻辑
                try:
                    return func(*args, **kwargs)  # 执行函数
                except Exception as e:
                    attempts += 1
                    logger.debug(f"Attempt {attempts} failed: {e}")  # 打印重试信息
                    time.sleep(delay)  # 等待重试
            logger.debug(f"Function failed after {max_attempts} attempts")  # 打印失败信息
        return wrapper
    return decorator


def mask_to_num(mask: str) -> int:
    """
    将子网掩码转换为掩码位数
    :param mask: 子网掩码（例如："255.255.255.0"）
    :return: 掩码位数（例如：24）
    """
    def count_bits(
        bin_str: str) -> int: return bin_str.count('1')  # 计算二进制字符串中 '1' 的数量
    mask_parts = mask.split('.')  # 分割掩码
    bit_count = [count_bits(bin(int(part))) for part in mask_parts]  # 计算每部分的位数
    return sum(bit_count)  # 返回总位数


def num_to_mask(mask_int: int) -> str:
    """
    将掩码位数转换为子网掩码
    :param mask_int: 掩码位数（例如：24）
    :return: 子网掩码（例如："255.255.255.0"")
    """
    bin_arr = ['0'] * 32  # 初始化 32 位二进制数组
    for i in range(mask_int):  # 设置前 mask_int 位为 '1'
        bin_arr[i] = '1'
    mask_parts = [''.join(bin_arr[i * 8:i * 8 + 8])
                  for i in range(4)]  # 分割为 4 部分
    mask_parts = [str(int(part, 2)) for part in mask_parts]  # 转换为十进制
    return '.'.join(mask_parts)  # 返回子网掩码


def num_to_ranges(num_list: List[int]) -> RangeList:
    """
    将数字列表转换为范围列表
    :param num_list: 数字列表（例如：[1, 2, 3, 5, 6, 8]）
    :return: 范围列表（例如：[[1, 3], [5, 6], [8, 8]]）
    """
    num_list.sort()  # 排序数字列表
    ranges: RangeList = []
    for k, g in groupby(enumerate(num_list), lambda x: x[1] - x[0]):  # 分组连续数字
        group = [v for _, v in g]
        if len(group) == 1:
            ranges.append([group[0], group[0]])  # 单个数字
        else:
            ranges.append([group[0], group[-1]])  # 连续数字范围
    return ranges


def split_list(lst: List[T], chunk_size: int) -> List[List[T]]:
    """
    将列表按指定大小分割
    :param lst: 原始列表（例如：[1, 2, 3, 4, 5]）
    :param chunk_size: 每段大小（例如：2）
    :return: 分割后的列表（例如：[[1, 2], [3, 4], [5]]）
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def compare_lists(list_1: List[T], list_2: List[T]) -> Tuple[List[T], List[T], List[T]]:
    """
    比较两个列表，返回减少、遗留和新增的元素
    :param list_1: 第一个列表（例如：[1, 2, 3]）
    :param list_2: 第二个列表（例如：[3, 4, 5]）
    :return: 减少、遗留和新增的元素（例如：([1, 2], [3], [4, 5])）
    """
    removed = [item for item in list_1 if item not in list_2]  # 减少的元素
    common = [item for item in list_1 if item in list_2]  # 遗留的元素
    added = [item for item in list_2 if item not in list_1]  # 新增的元素
    return removed, common, added


def group_dicts(dict_list: DictList, keys: List[str]) -> GroupedDict:
    """
    将字典列表按指定键分组
    :param dict_list: 字典列表（例如：[{"a": 1, "b": 2}, {"a": 1, "b": 3}]）
    :param keys: 分组键列表（例如：["a"]）
    :return: 分组后的字典（例如：{"1": [{"a": 1, "b": 2}, {"a": 1, "b": 3}]}）
    """
    grouped_dict: GroupedDict = {}
    for item in dict_list:
        group_key = '_'.join(str(item.get(key, 'None'))
                             for key in keys)  # 生成分组键
        grouped_dict.setdefault(group_key, []).append(item)  # 添加字典到分组
    return grouped_dict


def compare_dicts(dict_list_1: DictList, dict_list_2: DictList, keys: List[str]) -> Tuple[DictList, DictList, DictList]:
    """
    比较两个字典列表，返回减少、遗留和新增的字典
    :param dict_list_1: 第一个字典列表
    :param dict_list_2: 第二个字典列表
    :param keys: 比较键列表
    :return: 减少、遗留和新增的字典
    """
    grouped_dict_1 = group_dicts(dict_list_1, keys)  # 分组第一个字典列表
    grouped_dict_2 = group_dicts(dict_list_2, keys)  # 分组第二个字典列表
    removed_keys, common_keys, added_keys = compare_lists(
        list(grouped_dict_1.keys()), list(grouped_dict_2.keys()))
    removed = [
        item for key in removed_keys for item in grouped_dict_1[key]]  # 减少的字典
    common = [item for key in common_keys for item in grouped_dict_2[key]]  # 遗留的字典
    added = [item for key in added_keys for item in grouped_dict_2[key]]  # 新增的字典
    return removed, common, added


def idn_to_xn(domain: str) -> Optional[str]:
    """
    将中文域名转换为英文域名
    :param domain: 中文域名（例如："中文.中国"）
    :return: 英文域名（例如："xn--fiq228c.xn--fiqz9s"）
    """
    try:
        return domain.encode('idna').decode('utf-8')  # 转换域名
    except Exception as e:
        logger.debug(f"An exception occurred: {str(e)}")
        return None


def xn_to_idn(domain: str) -> Optional[str]:
    """
    将英文域名转换为中文域名
    :param domain: 英文域名（例如："xn--fiq228c.xn--fiqz9s"")
    :return: 中文域名（例如："中文.中国"）
    """
    try:
        return domain.encode('utf-8').decode('idna')  # 转换域名
    except Exception:
        logger.debug(f"An exception occurred: {str(e)}")
        return None


if __name__ == '__main__':
    # 测试 mask_to_num 和 num_to_mask
    print("Testing mask_to_num and num_to_mask:")
    mask = "255.255.255.0"
    mask_bits = mask_to_num(mask)
    print(f"mask_to_num('{mask}') -> {mask_bits}")  # 输出: 24
    # 输出: 255.255.255.0
    print(f"num_to_mask({mask_bits}) -> {num_to_mask(mask_bits)}")
    # 测试 num_to_ranges
    print("\nTesting num_to_ranges:")
    num_list = [1, 2, 3, 5, 6, 8]
    # 输出: [[1, 3], [5, 6], [8, 8]]
    print(f"num_to_ranges({num_list}) -> {num_to_ranges(num_list)}")
    # 测试 split_list
    print("\nTesting split_list:")
    lst = [1, 2, 3, 4, 5]
    chunk_size = 2
    # 输出: [[1, 2], [3, 4], [5]]
    print(f"split_list({lst}, {chunk_size}) -> {split_list(lst, chunk_size)}")
    # 测试 compare_lists
    print("\nTesting compare_lists:")
    list_1 = [1, 2, 3]
    list_2 = [3, 4, 5]
    # 输出: ([1, 2], [3], [4, 5])
    print(
        f"compare_lists({list_1}, {list_2}) -> {compare_lists(list_1, list_2)}")
    # 测试 group_dicts
    print("\nTesting group_dicts:")
    dict_list = [{"a": 1, "b": 2}, {"a": 1, "b": 3}]
    keys = ["a"]
    # 输出: {'1': [{'a': 1, 'b': 2}, {'a': 1, 'b': 3}]}
    print(
        f"group_dicts({dict_list}, {keys}) -> {group_dicts(dict_list, keys)}")
    # 测试 compare_dicts
    print("\nTesting compare_dicts:")
    dict_list_1 = [{"a": 1, "b": 2}, {"a": 1, "b": 3}]
    dict_list_2 = [{"a": 1, "b": 3}, {"a": 2, "b": 4}]
    keys = ["a"]
    # 输出: ([{'a': 1, 'b': 2}], [{'a': 1, 'b': 3}], [{'a': 2, 'b': 4}])
    print(
        f"compare_dicts({dict_list_1}, {dict_list_2}, {keys}) -> {compare_dicts(dict_list_1, dict_list_2, keys)}")
    # 测试 idn_to_xn 和 xn_to_idn
    print("\nTesting idn_to_xn and xn_to_idn:")
    chinese_domain = "中文.中国"
    xn_domain = idn_to_xn(chinese_domain)
    # 输出: xn--fiq228c.xn--fiqz9s
    print(f"idn_to_xn('{chinese_domain}') -> {xn_domain}")
    print(f"xn_to_idn('{xn_domain}') -> {xn_to_idn(xn_domain)}")  # 输出: 中文.中国
