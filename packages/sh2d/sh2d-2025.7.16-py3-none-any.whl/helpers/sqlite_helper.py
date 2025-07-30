# -*- encoding: utf-8 -*-

'''
@File    :   sqlite_helper.py
@Time    :   2025/07/16 12:16:00
@Author  :   test233
@Version :   1.0
'''


import sqlite3
from typing import List, Dict, Union, Optional
from loguru import logger

class SQLiteDB:
    """
    SQLite 数据库操作类，支持创建表、插入、更新、删除和查询操作。
    """
    def __init__(self, db_name: str, create_table_sql: Optional[List[str]] = None) -> None:
        """
        初始化函数，创建数据库连接。
        :param db_name: 数据库名称或文件路径，例如：test.db , :memory: (内存)
        :param create_table_sql: 创建表的 SQL 语句列表，例如：["CREATE TABLE tablename (name TEXT NOT NULL);"]
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        if create_table_sql:
            for sql in create_table_sql:
                self.set(sql)
    def set(self, sql: str, data: Optional[Union[List, List[List]]] = None, many: bool = False) -> int:
        """
        执行 SQL 语句，支持插入、更新、删除操作。
        :param sql: SQL 语句，例如：INSERT INTO tablename (name) VALUES (?) / DELETE from tablename where name=? / UPDATE tablename set name = ? where name=?
        :param data: 数据参数，例如：[a, b, c] 或 [[a, b, c], [a, b, c]]
        :param many: 是否批量操作，默认为 False
        :return: 受影响的行数，失败返回 0
        """
        try:
            if many:
                self.cursor.executemany(sql, data if data else [])
            else:
                self.cursor.execute(sql, data if data else [])
            affected_rows = self.cursor.rowcount
            # logger.debug(f'Executed SQL: "{sql}", Affected Rows: {affected_rows}')
            return affected_rows
        except Exception as e:
            logger.exception(f'Failed to execute SQL: "{sql}", Error: {e}')
            return 0
        finally:
            self.conn.commit()
    def get(self, sql: str, data: Optional[List] = None, to_json: bool = False, columns: Optional[List[str]] = None) -> Union[List[tuple], List[Dict]]:
        """
        执行查询 SQL 语句，支持返回原始结果或 JSON 格式。
        :param sql: SQL 查询语句，例如：SELECT * FROM tablename WHERE name=?
        :param data: 查询参数，例如：[name]
        :param to_json: 是否返回 JSON 格式，默认为 False
        :param columns: 列名列表，用于 JSON 格式输出，例如：['name']
        :return: 查询结果，例如：[(a, b)] 或 [{'name': 'a'}]
        """
        try:
            results = self.cursor.execute(sql, data if data else []).fetchall()
            if to_json:
                if not columns:
                    columns = [column[0] for column in self.cursor.description]
                return [dict(zip(columns, row)) for row in results]
            return results
        except Exception as e:
            logger.exception(f'Failed to query SQL: "{sql}", Error: {e}')
            return []
    def close(self) -> None:
        """关闭数据库连接。"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
            self.cursor = None  # 设置为 None，避免重复关闭
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            self.conn = None  # 设置为 None，避免重复关闭
    def __del__(self) -> None:
        """析构函数，自动关闭数据库连接。"""
        if hasattr(self, 'conn') and self.conn is not None:  # 检查连接状态
            self.close()

if __name__ == "__main__":
    # 创建数据库和表
    db = SQLiteDB("test.db", ["CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);"])
    # 插入数据
    db.set("INSERT INTO users (name) VALUES (?)", ["Alice"])
    db.set("INSERT INTO users (name) VALUES (?)", ["Bob"])
    # 批量插入数据
    db.set("INSERT INTO users (name) VALUES (?)", [["Charlie"], ["David"]], many=True)
    # 查询数据
    print("All Users (Raw):", db.get("SELECT * FROM users"))
    print("All Users (JSON):", db.get("SELECT * FROM users", to_json=True, columns=["id", "name"]))
    # 更新数据
    db.set("UPDATE users SET name = ? WHERE name = ?", ["Alice Smith", "Alice"])
    # 删除数据
    db.set("DELETE FROM users WHERE name = ?", ["Bob"])
    # 查询更新后的数据
    print("Updated Users (Raw):", db.get("SELECT * FROM users"))
    print("Updated Users (JSON):", db.get("SELECT * FROM users", to_json=True, columns=["id", "name"]))
    # 关闭数据库连接
    db.close()
