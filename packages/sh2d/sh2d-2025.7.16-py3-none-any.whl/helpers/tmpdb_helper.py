# -*- encoding: utf-8 -*-

'''
@File    :   tmpdb_helper.py
@Time    :   2025/07/16 12:16:13
@Author  :   test233
@Version :   1.0
'''


import os
from typing import List, Tuple, Optional, Union
from .sqlite_helper import SQLiteDB
from .ipaddress_helper import ip_to_num


class TmpDB:
    """
    临时数据库操作类，支持键值对存储和 IP 范围存储。
    """

    def __init__(self, dbname: str = ":memory:") -> None:
        """
        初始化函数，创建数据库连接。
        :param dbname: 数据库名称或数据库文件路径，例如：test.db 或 :memory:
        """
        if not os.path.exists(dbname) or dbname == ":memory:":
            self.db = SQLiteDB(
                dbname,
                [
                    'CREATE TABLE IF NOT EXISTS tmp1 (key TEXT NOT NULL, value TEXT NOT NULL);',
                    'CREATE TABLE IF NOT EXISTS tmp2 (start INT NOT NULL, end INT NOT NULL, value TEXT NOT NULL);',
                ],
            )
        else:
            self.db = SQLiteDB(dbname)

    def get(self, key: str) -> Optional[str]:
        """
        根据键查询值。
        :param key: 键值
        :return: 对应的值，如果不存在则返回 None
        """
        result = self.db.get("SELECT value FROM tmp1 WHERE key=?", [key])
        return result[0][0] if result else None

    def get_ip(self, ip: str) -> List[str]:
        """
        根据 IP 查询对应的值。
        :param ip: IP 地址
        :return: 匹配的值列表
        """
        result = self.db.get(
            "SELECT value FROM tmp2 WHERE start <= ? AND ? <= end", [ip_to_num(ip), ip_to_num(ip)])
        return [row[0] for row in result]

    def get_ip_range(self) -> Optional[Tuple[int, int]]:
        """
        获取所有 IP 范围的最小起始值和最大结束值。
        :return: 最小起始值和最大结束值的元组，如果无数据则返回 None
        """
        result = self.db.get("SELECT MIN(start), MAX(end) FROM tmp2")
        return result[0] if result else None

    def set(self, key: str, value: str) -> int:
        """
        插入或更新键值对。
        :param key: 键
        :param value: 值
        :return: 受影响的行数
        """
        result = self.db.get("SELECT value FROM tmp1 WHERE key=?", [key])
        if not result:
            return self.db.set("INSERT INTO tmp1 (key, value) VALUES (?, ?)", [key, value])
        else:
            return self.db.set("UPDATE tmp1 SET value = ? WHERE key=?", [value, key])

    def sets(self, kv: List[Tuple[str, str]]) -> int:
        """
        批量插入键值对。
        :param kv: 键值对列表，例如：[('key1', 'value1'), ('key2', 'value2')]
        :return: 受影响的行数
        """
        return self.db.set("INSERT INTO tmp1 (key, value) VALUES (?, ?)", kv, many=True)

    def set_ip(self, start_ip: str, end_ip: str, value: str) -> int:
        """
        插入或更新 IP 范围对应的值。
        :param start_ip: 起始 IP 地址
        :param end_ip: 结束 IP 地址
        :param value: 值
        :return: 受影响的行数
        """
        start_num, end_num = ip_to_num(start_ip), ip_to_num(end_ip)
        result = self.db.get("SELECT value FROM tmp2 WHERE start=? AND end=?", [
                             start_num, end_num])
        if not result:
            return self.db.set("INSERT INTO tmp2 (start, end, value) VALUES (?, ?, ?)", [start_num, end_num, value])
        else:
            return self.db.set("UPDATE tmp2 SET value = ? WHERE start=? AND end=?", [value, start_num, end_num])

    def set_ips(self, ip_ranges: List[Tuple[str, str, str]]) -> int:
        """
        批量插入 IP 范围对应的值。
        :param ip_ranges: IP 范围列表，例如：[('start1', 'end1', 'value1'), ('start2', 'end2', 'value2')]
        :return: 受影响的行数
        """
        kv = [[ip_to_num(start_ip), ip_to_num(end_ip), value]
              for start_ip, end_ip, value in ip_ranges]
        return self.db.set("INSERT INTO tmp2 (start, end, value) VALUES (?, ?, ?)", kv, many=True)

    def remove(self, key: str) -> int:
        """
        根据键删除键值对。
        :param key: 键
        :return: 受影响的行数
        """
        return self.db.set("DELETE FROM tmp1 WHERE key=?", [key])

    def remove_ip(self, start_ip: str, end_ip: str) -> int:
        """
        根据起始 IP 和结束 IP 删除 IP 范围对应的值。
        :param start_ip: 起始 IP 地址
        :param end_ip: 结束 IP 地址
        :return: 受影响的行数
        """
        start_num, end_num = ip_to_num(start_ip), ip_to_num(end_ip)
        return self.db.set("DELETE FROM tmp2 WHERE start=? AND end=?", [start_num, end_num])


if __name__ == "__main__":
    # 测试代码
    db = TmpDB()
    # 测试键值对操作
    db.set("a", "a")
    db.set("a", "b")
    db.set("c", "c")
    print("Get 'a':", db.get("a"))  # 输出: b
    print("Get 'b':", db.get("b"))  # 输出: None
    print("Get 'c':", db.get("c"))  # 输出: c
    db.remove("c")
    print("Get 'c' after removal:", db.get("c"))  # 输出: None
    # 测试 IP 范围操作
    db.set_ip("192.168.1.1", "192.168.1.10", "Network1")
    db.set_ip("192.168.1.11", "192.168.1.20", "Network2")
    print("Get IP '192.168.1.5':", db.get_ip(
        "192.168.1.5"))  # 输出: ['Network1']
    print("Get IP '192.168.1.15':", db.get_ip(
        "192.168.1.15"))  # 输出: ['Network2']
    print("IP range:", db.get_ip_range())  # 输出: (3232235777, 3232235796)
    db.remove_ip("192.168.1.1", "192.168.1.10")
    print("Get IP '192.168.1.5' after removal:",
          db.get_ip("192.168.1.5"))  # 输出: []
