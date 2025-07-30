# -*- encoding: utf-8 -*-

'''
@File    :   zipfile_helper.py
@Time    :   2025/07/16 12:17:02
@Author  :   test233
@Version :   1.0
'''


import os
import datetime
import zipfile
from typing import Dict, List, Optional


def unzip(zip_file_path: str, extract_dir: str) -> None:
    """
    解压 ZIP 文件到指定目录。
    Args:
        zip_file_path (str): ZIP 文件路径。
        extract_dir (str): 解压目标目录。
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def make_zip_without_root(source_dir: str, output_zip_path: str) -> None:
    """
    打包文件夹，不包含根目录。
    Args:
        source_dir (str): 要打包的目录路径。
        output_zip_path (str): 生成的 ZIP 文件路径。
    """
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, _, files in os.walk(source_dir):
            relative_path = root.replace(source_dir, '').lstrip(os.path.sep)
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(relative_path, file)
                zip_ref.write(file_path, arcname)


def make_zip_with_root(source_dir: str, output_zip_path: str) -> None:
    """
    打包文件夹，包含根目录。
    Args:
        source_dir (str): 要打包的目录路径。
        output_zip_path (str): 生成的 ZIP 文件路径。
    """
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        parent_dir = os.path.dirname(source_dir)
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, parent_dir)
                zip_ref.write(file_path, arcname)


def get_creation_times(zip_file_path: str) -> Dict[str, datetime.datetime]:
    """
    获取 ZIP 文件内各文件的创建时间。
    Args:
        zip_file_path (str): ZIP 文件路径。
    Returns:
        Dict[str, datetime.datetime]: 文件名与创建时间的映射。
    """
    creation_times = {}
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            file_info = zip_ref.getinfo(file_name)
            try:
                creation_time = file_info.date_time
                creation_datetime = datetime.datetime(
                    year=creation_time[0],
                    month=creation_time[1],
                    day=creation_time[2],
                    hour=creation_time[3],
                    minute=creation_time[4],
                    second=creation_time[5]
                )
                creation_times[file_name] = creation_datetime
            except KeyError:
                continue
    return creation_times


if __name__ == "__main__":
    # 测试代码
    test_dir = "test_dir"  # 测试目录
    output_zip_v1 = "output_v1.zip"  # 不包含根目录的 ZIP 文件
    output_zip_v2 = "output_v2.zip"  # 包含根目录的 ZIP 文件
    # 创建测试目录和文件
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "file1.txt"), "w") as f:
        f.write("This is file1.")
    with open(os.path.join(test_dir, "file2.txt"), "w") as f:
        f.write("This is file2.")
    # 测试打包功能
    print("Testing make_zip_without_root...")
    make_zip_without_root(test_dir, output_zip_v1)
    print(f"ZIP file '{output_zip_v1}' created without root directory.")
    print("\nTesting make_zip_with_root...")
    make_zip_with_root(test_dir, output_zip_v2)
    print(f"ZIP file '{output_zip_v2}' created with root directory.")
    # 测试解压功能
    print("\nTesting unzip...")
    unzip(output_zip_v1, "extracted_v1")
    print(f"ZIP file '{output_zip_v1}' extracted to 'extracted_v1'.")
    # 测试获取创建时间功能
    print("\nTesting get_creation_times...")
    creation_times = get_creation_times(output_zip_v1)
    for file_name, creation_time in creation_times.items():
        print(f"File: {file_name}, Creation Time: {creation_time}")
