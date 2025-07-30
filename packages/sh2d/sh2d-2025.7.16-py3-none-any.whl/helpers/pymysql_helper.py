# -*- encoding: utf-8 -*-

'''
@File    :   pymysql_helper.py
@Time    :   2025/07/16 12:13:49
@Author  :   test233
@Version :   1.0
'''


import pymysql
from loguru import logger
from typing import List, Tuple, Union, Optional


class MySQLDB:
    """
    MySQL 数据库操作类，用于执行数据库的增删改查操作。
    """

    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 3306,
        user: str = 'root',
        password: str = 'root',
        database: str = 'test',
        charset: str = 'utf8'
    ) -> None:
        """
        初始化函数，创建数据库连接。
        :param host: 数据库主机地址，默认为 '127.0.0.1'
        :param port: 数据库端口，默认为 3306
        :param user: 数据库用户名，默认为 'root'
        :param password: 数据库密码，默认为 'root'
        :param database: 数据库名称，默认为 'test'
        :param charset: 数据库字符集，默认为 'utf8'
        """
        self.conn = None
        self.cursor = None
        try:
            self.conn = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset=charset
            )
            self.cursor = self.conn.cursor()
            logger.info("Database connection established successfully.")
        except pymysql.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise RuntimeError(f"Database connection failed: {e}")

    def set(
        self,
        sql: str,
        data: Union[List, Tuple] = [],
        many: bool = False
    ) -> bool:
        """
        执行数据库的插入、修改、删除操作。
        :param sql: SQL 语句，例如：
                   INSERT INTO tablename (name) VALUES (%s)
                   DELETE FROM tablename WHERE name=%s
                   UPDATE tablename SET name=%s WHERE name=%s
        :param data: SQL 语句的参数，例如：[a, b, c, d]
        :param many: 是否批量操作，默认为 False
        :return: 操作成功返回 True，失败返回 False
        """
        if not self.conn or not self.cursor:
            logger.error("Database connection is not established.")
            return False
        try:
            if many:
                self.cursor.executemany(sql, data)
            else:
                self.cursor.execute(sql, data)
            affected_rows = self.conn.affected_rows()
            logger.debug(
                f'Executed SQL: "{sql}", Affected rows: {affected_rows}')
            return affected_rows > 0
        except pymysql.Error as e:
            logger.error(f'Failed to execute SQL: "{sql}": {e}')
            return False
        finally:
            self.conn.commit()

    def get(
        self,
        sql: str,
        data: Union[List, Tuple] = []
    ) -> Optional[List[Tuple]]:
        """
        执行数据库的查询操作。
        :param sql: SQL 查询语句，例如：SELECT * FROM tablename WHERE name=%s
        :param data: SQL 查询参数，例如：[name,]
        :return: 查询结果，例如：[(a, b,)]，如果查询失败返回 None
        """
        if not self.conn or not self.cursor:
            logger.error("Database connection is not established.")
            return None
        try:
            self.cursor.execute(sql, data)
            results = self.cursor.fetchall()
            logger.debug(f'Executed SQL: "{sql}", Results: {results}')
            return results
        except pymysql.Error as e:
            logger.error(f'Failed to execute SQL: "{sql}": {e}')
            return None

    def close(self) -> None:
        """
        关闭数据库连接和游标。
        """
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor closed.")
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def __del__(self) -> None:
        """
        析构函数，确保对象销毁时关闭数据库连接。
        """
        self.close()


if __name__ == "__main__":
    # 初始化数据库连接
    db = MySQLDB(host='127.0.0.1', user='root',
                 password='root', database='test')
    # 测试插入操作
    insert_sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
    insert_data = [('Alice', 25), ('Bob', 30)]
    if db.set(insert_sql, insert_data, many=True):
        print("Insert operation successful!")
    else:
        print("Insert operation failed!")
    # 测试查询操作
    select_sql = "SELECT * FROM users WHERE age > %s"
    select_data = [20]
    results = db.get(select_sql, select_data)
    if results:
        print("Query results:", results)
    else:
        print("Query failed!")
    # 测试更新操作
    update_sql = "UPDATE users SET age = %s WHERE name = %s"
    update_data = [26, 'Alice']
    if db.set(update_sql, update_data):
        print("Update operation successful!")
    else:
        print("Update operation failed!")
    # 测试删除操作
    delete_sql = "DELETE FROM users WHERE name = %s"
    delete_data = ['Bob']
    if db.set(delete_sql, delete_data):
        print("Delete operation successful!")
    else:
        print("Delete operation failed!")
    # 关闭数据库连接
    db.close()
