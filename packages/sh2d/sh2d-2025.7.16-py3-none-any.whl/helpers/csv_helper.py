# -*- encoding: utf-8 -*-

'''
@File    :   csv_helper.py
@Time    :   2025/07/16 12:07:35
@Author  :   test233
@Version :   1.0
'''


import csv
from typing import List, Dict, Generator, Any


def write_list_to_csv(file_path: str, data_rows: List[List[Any]], encoding: str = "utf8") -> None:
    """
    将多行数据写入CSV文件。
    :param file_path: CSV文件的路径，例如：data.csv
    :param data_rows: 多行数据，格式为[[1, 2], [3, 4]]
    :param encoding: 文件编码，默认为utf8
    """
    with open(file_path, "a", newline="", encoding=encoding) as csv_file:
        csv_writer = csv.writer(csv_file, dialect="excel")
        csv_writer.writerows(data_rows)


def read_csv_to_list(file_path: str, encoding: str = "utf8") -> Generator[List[str], None, None]:
    """
    从CSV文件中读取数据并返回一个生成器，每次生成一行数据。
    :param file_path: CSV文件的路径，例如：data.csv
    :param encoding: 文件编码，默认为utf8
    :return: 生成器，每次生成一行数据，格式为["1", "2", "3"]
    """
    with open(file_path, "r", encoding=encoding) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            yield row


def read_csv_to_json(file_path: str, encoding: str = "utf8") -> Generator[Dict[str, str], None, None]:
    """
    从CSV文件中读取数据并返回一个生成器，每次生成一行数据的字典形式。
    :param file_path: CSV文件的路径，例如：data.csv
    :param encoding: 文件编码，默认为utf8
    :return: 生成器，每次生成一行数据的字典形式，格式为{"header1": "value1", "header2": "value2"}
    """
    with open(file_path, "r", encoding=encoding) as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # 读取表头
        for row in csv_reader:
            yield dict(zip(headers, row))


def write_json_list_to_csv(file_path: str, json_data: List[Dict[str, Any]], encoding: str = "utf8") -> None:
    """
    将JSON格式的数据写入CSV文件。
    :param file_path: CSV文件的路径，例如：data.csv
    :param json_data: JSON格式的数据，格式为[{"header1": "value1", "header2": "value2"}, ...]
    :param encoding: 文件编码，默认为utf8
    """
    # 提取所有表头
    headers = []
    for item in json_data:
        for key in item.keys():
            if key not in headers:
                headers.append(key)

    # 构建数据行
    rows = [headers]  # 第一行为表头
    for item in json_data:
        row = [str(item.get(header, "")) for header in headers]
        rows.append(row)

    # 写入CSV文件
    write_list_to_csv(file_path, rows, encoding)


# 测试代码
if __name__ == "__main__":
    # 测试 write_list_to_csv
    test_data = [[1, 2, 3], [4, 5, 6]]
    write_list_to_csv("test.csv", test_data)
    print("Data written to test.csv")
    # 测试 read_csv_to_list
    for row in read_csv_to_list("test.csv"):
        print(f"Row from CSV: {row}")
    # 测试 read_csv_to_json
    for row in read_csv_to_json("test.csv"):
        print(f"Row as JSON: {row}")
    # 测试 write_json_list_to_csv
    json_data = [{"header1": "value1", "header2": "value2"},
                 {"header1": "value3", "header2": "value4"}]
    write_json_list_to_csv("test_json.csv", json_data)
    print("JSON data written to test_json.csv")
