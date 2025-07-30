# -*- encoding: utf-8 -*-

'''
@File    :   binascii_helper.py
@Time    :   2025/07/16 12:06:41
@Author  :   test233
@Version :   1.0
'''


import binascii


def hex_to_bytes(hex_str: str) -> bytes:
    """
    将十六进制字符串转换为字节数据
    :param hex_str: 十六进制字符串（例如："666c6167"）
    :return: 转换后的字节数据，如果输入为空则返回空字节
    """
    return binascii.unhexlify(hex_str) if hex_str else b''


def bytes_to_hex(data_bytes: bytes, encoding: str = 'utf8') -> str:
    """
    将字节数据转换为十六进制字符串
    :param data_bytes: 字节数据（例如：b'flag'）
    :param encoding: 字符串编码格式，默认为 'utf8'
    :return: 转换后的十六进制字符串，如果输入为空则返回空字符串
    """
    return binascii.hexlify(data_bytes).decode(encoding) if data_bytes else ''


if __name__ == '__main__':
    # 示例：十六进制字符串与字节数据之间的转换
    hex_str = '666c6167'
    print(f"Hex string to bytes: {hex_to_bytes(hex_str)}")
    data_bytes = b'flag'
    print(f"Bytes to hex string: {bytes_to_hex(data_bytes)}")
