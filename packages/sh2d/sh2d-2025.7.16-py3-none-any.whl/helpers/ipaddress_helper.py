# -*- encoding: utf-8 -*-

'''
@File    :   ipaddress_helper.py
@Time    :   2025/07/16 12:08:27
@Author  :   test233
@Version :   1.0
'''


import re
import ipaddress
from typing import List, Tuple
from itertools import groupby
from loguru import logger

# 定义类型别名
RangeList = List[List[int]]  # 范围列表类型


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


def ip_to_num(ip: str) -> int:
    """
    将 IP 地址转换为整数。
    :param ip: IP 地址字符串，例如 "1.1.1.1"
    :return: 对应的整数值
    """
    return int(ipaddress.ip_address(ip))


def num_to_ip(num: int) -> str:
    """
    将整数转换为 IP 地址。
    :param num: 整数值
    :return: 对应的 IP 地址字符串
    """
    return ipaddress.ip_address(num).compressed


def generate_ip_range(start_ip: str, end_ip: str) -> List[str]:
    """
    根据起始 IP 和结束 IP 生成 IP 地址范围。
    :param start_ip: 起始 IP 地址
    :param end_ip: 结束 IP 地址
    :return: IP 地址范围列表
    """
    return [num_to_ip(num) for num in range(ip_to_num(start_ip), ip_to_num(end_ip) + 1)]


def net_to_ip_range(net_str: str, strict: bool = False) -> Tuple[str, str]:
    """
    将网段字符串转换为 IP 地址范围。
    :param net_str: 网段字符串，例如 "192.168.1.0/24" 或 "192.168.1.1-33"
    :param strict: 是否严格校验网络地址
    :return: 包含起始 IP 和结束 IP 的元组
    """
    if re.search(r"^\d+\.\d+\.\d+\.\d+-\d+$", net_str):
        _net, start, end = re.findall(
            r"(\d+\.\d+\.\d+\.)(\d+)-(\d+)", net_str)[0]
        ip_range = (f"{_net}{start}", f"{_net}{end}")
    elif re.match(r"^\d+\.\d+\.\d+\.\d+-\d+\.\d+\.\d+\.\d+$", net_str):
        ip_range = re.findall(
            r"(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)", net_str)[0]
    elif re.match(r"^[0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4}-[0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4}$", net_str):
        ip_range = re.findall(
            r"([0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4})-([0-9a-fA-F]{1,4}:.*:[0-9a-fA-F]{1,4})", net_str)[0]
    else:
        try:
            network = ipaddress.ip_network(net_str, strict=strict)
            ip_range = (network.network_address.compressed,
                        network.broadcast_address.compressed)
        except Exception as e:
            logger.warning(
                f"Failed to convert {net_str} to IP range: {e}", exc_info=True)
            ip_range = ("0", "0")
    return ip_range


def net_to_ip_list(net_str: str, strict: bool = False) -> List[str]:
    """
    将网段字符串拆分为 IP 地址列表。
    :param net_str: 网段字符串
    :param strict: 是否严格校验网络地址
    :return: IP 地址列表
    """
    ip_range = net_to_ip_range(net_str, strict)
    if ip_range == ("0", "0"):
        return []
    return generate_ip_range(*ip_range)


def net_to_cidr(net_str: str, strict: bool = False) -> List[str]:
    """
    将网段字符串转换为 CIDR 格式列表。
    :param net_str: 网段字符串
    :param strict: 是否严格校验网络地址
    :return: CIDR 格式列表
    """
    ip_range = net_to_ip_range(net_str, strict)
    try:
        return [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
            ipaddress.IPv4Address(ip_range[0]), ipaddress.IPv4Address(ip_range[1]))]
    except Exception as e:
        logger.warning(
            f"Failed to convert {net_str} to CIDR: {e}", exc_info=True)
        return []


def ip_list_to_ip_ranges(ip_list: List[str]) -> List[List[str]]:
    """
    将 IP 地址列表合并为 IP 范围列表。
    :param ip_list: IP 地址列表
    :return: IP 范围列表，例如 [["ip1", "ip2"], ["ip3", "ip4"]]
    """
    num_list = [ip_to_num(ip) for ip in ip_list]
    num_ranges = num_to_ranges(num_list)
    return [[num_to_ip(start), num_to_ip(end)] for start, end in num_ranges]


def ip_list_to_cidr(ip_list: List[str]) -> List[str]:
    """
    将 IP 地址列表合并为 CIDR 格式列表。
    :param ip_list: IP 地址列表
    :return: CIDR 格式列表
    """
    num_list = [ip_to_num(ip) for ip in ip_list]
    num_ranges = num_to_ranges(num_list)
    cidr_list = []
    for start, end in num_ranges:
        try:
            cidr_list += [ipaddr.compressed for ipaddr in ipaddress.summarize_address_range(
                ipaddress.IPv4Address(num_to_ip(start)), ipaddress.IPv4Address(num_to_ip(end)))]
        except Exception as e:
            logger.warning(
                f"Failed to convert {start}-{end} to CIDR: {e}", exc_info=True)
    return cidr_list


if __name__ == "__main__":
    # 测试 IP 地址转换
    print("Testing ip_to_num and num_to_ip:")
    print(ip_to_num("1.1.1.1"))  # 输出: 16843009
    print(num_to_ip(16843009))   # 输出: 1.1.1.1
    # 测试 IP 范围生成
    print("\nTesting generate_ip_range:")
    # 输出: ['1.1.1.1', '1.1.1.2', '1.1.1.3']
    print(generate_ip_range("1.1.1.1", "1.1.1.3"))
    # 测试网段转换为 IP 范围
    print("\nTesting net_to_ip_range:")
    # 输出: ('192.168.1.0', '192.168.1.255')
    print(net_to_ip_range("192.168.1.0/24"))
    # 输出: ('192.168.1.1', '192.168.1.33')
    print(net_to_ip_range("192.168.1.1-33"))
    # 输出: ('192.168.1.5', '192.168.1.8')
    print(net_to_ip_range("192.168.1.5-192.168.1.8"))
    # 输出: ('2001:db8::1:0:0:1', '2001:db8::1:0:0:3')
    print(net_to_ip_range("2001:db8::1:0:0:1-2001:db8::1:0:0:3"))
    # 测试网段转换为 IP 列表
    print("\nTesting net_to_ip_list:")
    # 输出: ['192.168.1.0', '192.168.1.1', '192.168.1.2', '192.168.1.3']
    print(net_to_ip_list("192.168.1.0/30"))
    # 测试网段转换为 CIDR 列表
    print("\nTesting net_to_cidr:")
    print(net_to_cidr("192.168.1.0/24"))  # 输出: ['192.168.1.0/24']
    # 测试 IP 列表转换为 IP 范围列表
    print("\nTesting ip_list_to_ip_ranges:")
    # 输出: [['192.168.1.1', '192.168.1.2'], ['192.168.1.5', '192.168.1.6']]
    print(ip_list_to_ip_ranges(
        ["192.168.1.1", "192.168.1.2", "192.168.1.5", "192.168.1.6"]))
    # 测试 IP 列表转换为 CIDR 列表
    print("\nTesting ip_list_to_cidr:")
    # 输出: ['192.168.1.1/31', '192.168.1.5/31']
    print(ip_list_to_cidr(
        ["192.168.1.1", "192.168.1.2", "192.168.1.5", "192.168.1.6"]))
