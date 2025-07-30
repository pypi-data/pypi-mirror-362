# -*- encoding: utf-8 -*-

'''
@File    :   pyzipper_helper.py
@Time    :   2025/07/16 12:14:06
@Author  :   test233
@Version :   1.0
'''

import os
import pyzipper
from loguru import logger
from typing import Optional


def make_zip_with_aes(
    source_dir: str,
    output_filename: str,
    password: str,
    compression_method: int = pyzipper.ZIP_LZMA,
    encryption_method: int = pyzipper.WZ_AES,
    encryption_bits: int = 128
) -> None:
    """
    使用 AES 加密将指定目录压缩为 ZIP 文件。
    :param source_dir: 需要压缩的目录路径
    :param output_filename: 输出的 ZIP 文件路径
    :param password: 加密密码
    :param compression_method: 压缩方法，默认为 ZIP_LZMA
    :param encryption_method: 加密方法，默认为 WZ_AES
    :param encryption_bits: 加密位数，默认为 128
    """
    try:
        # 使用 AES 加密创建 ZIP 文件
        with pyzipper.AESZipFile(output_filename, 'w', compression=compression_method) as zip_file:
            # 设置 ZIP 文件的密码
            zip_file.setpassword(password.encode('utf-8'))
            # 设置加密方法和位数
            zip_file.setencryption(encryption_method, nbits=encryption_bits)
            # 遍历目录中的所有文件
            for root, _, filenames in os.walk(source_dir):
                # 计算文件在 ZIP 中的相对路径
                relative_path = root.replace(source_dir, '')
                for filename in filenames:
                    # 将文件添加到 ZIP 中
                    file_path = os.path.join(root, filename)
                    zip_file.write(file_path, os.path.join(
                        relative_path, filename))
    except Exception as e:
        logger.warning(f"Failed to create ZIP file: {e}")


if __name__ == "__main__":
    # 测试目录压缩
    try:
        source_directory = "test_folder"  # 需要压缩的目录
        output_zip_file = "output.zip"    # 输出的 ZIP 文件
        zip_password = "secure_password"  # 加密密码
        make_zip_with_aes(source_directory, output_zip_file, zip_password)
    except Exception as e:
        print(f"Test failed for make_zip_with_aes: {e}")
