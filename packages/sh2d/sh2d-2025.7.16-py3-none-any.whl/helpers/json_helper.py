# -*- encoding: utf-8 -*-

'''
@File    :   json_helper.py
@Time    :   2025/07/16 12:08:32
@Author  :   test233
@Version :   1.0
'''


import os
import json
from loguru import logger


def write_json(file_path, data, encoding="utf8"):
    """
    将数据写入JSON文件。
    :param file_path: JSON文件的路径
    :param data: 要写入的数据（字典或列表）
    :param encoding: 文件编码，默认为utf8
    """
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_json(file_path, default_data=None, encoding="utf8"):
    """
    从JSON文件中读取数据。如果文件不存在或读取失败，则返回默认数据并创建文件。
    :param file_path: JSON文件的路径
    :param default_data: 默认数据，当文件不存在或读取失败时返回，默认为空字典
    :param encoding: 文件编码，默认为utf8
    :return: 读取到的数据或默认数据
    """
    if default_data is None:
        default_data = {}
    data = default_data
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding=encoding) as file:
                data = json.load(file)
        except Exception as e:
            logger.warning(
                f"Failed to read JSON file: {file_path}", exc_info=True)
            write_json(file_path, default_data, encoding)
    else:
        write_json(file_path, default_data, encoding)
    return data


# 测试代码
if __name__ == "__main__":
    # 测试文件路径
    test_file = "test.json"
    # 测试数据
    test_data = {"name": "Alice", "age": 25, "city": "Beijing"}
    # 测试 write_json 函数
    print("Testing write_json function...")
    write_json(test_file, test_data)
    print(f"Data written to {test_file}: {test_data}")
    # 测试 read_json 函数（文件存在且格式正确）
    print("\nTesting read_json function (file exists and is valid)...")
    read_data = read_json(test_file)
    print(f"Data read from {test_file}: {read_data}")
    # 测试 read_json 函数（文件不存在）
    print("\nTesting read_json function (file does not exist)...")
    non_existent_file = "non_existent.json"
    read_data = read_json(non_existent_file, default_data={"default": "data"})
    print(f"Data read from {non_existent_file}: {read_data}")
    # 测试 read_json 函数（文件存在但格式错误）
    print("\nTesting read_json function (file exists but is invalid)...")
    with open(test_file, "w", encoding="utf8") as file:
        file.write("invalid json data")
    read_data = read_json(test_file, default_data={"default": "data"})
    print(
        f"Data read from {test_file} (after writing invalid data): {read_data}")
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(non_existent_file):
        os.remove(non_existent_file)
