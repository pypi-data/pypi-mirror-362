# -*- encoding: utf-8 -*-

'''
@File    :   base64_helper.py
@Time    :   2025/07/16 12:26:03
@Author  :   test233
@Version :   1.0
'''

import base64
class Base64CustomCodec:
    """
    支持自定义码表的 Base64 编码解码类，输入和输出均为字节。
    """
    STANDARD_ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    @staticmethod
    def encode(data, custom_alphabet=None):
        """
        Base64 编码，输入和输出均为字节。
        :param data: 要编码的数据（字节）。
        :param custom_alphabet: 自定义码表（可选，必须为 64 个字节）。
        :return: 编码后的数据（字节）。
        :raises ValueError: 如果输入不是字节，或自定义码表无效。
        """
        if not isinstance(data, bytes):
            raise ValueError("输入必须是字节！")
        if custom_alphabet and (not isinstance(custom_alphabet, bytes) or len(custom_alphabet) != 64):
            raise ValueError("自定义码表必须为 64 个字节！")
        
        # 标准 Base64 编码
        encoded_data = base64.b64encode(data)
        
        # 如果提供了自定义码表，进行码表替换
        if custom_alphabet:
            translation_table = bytes.maketrans(Base64CustomCodec.STANDARD_ALPHABET, custom_alphabet)
            encoded_data = encoded_data.translate(translation_table)
        
        return encoded_data
    @staticmethod
    def decode(encoded_data, custom_alphabet=None):
        """
        Base64 解码，输入和输出均为字节。
        :param encoded_data: 要解码的 Base64 数据（字节）。
        :param custom_alphabet: 自定义码表（可选，必须为 64 个字节）。
        :return: 解码后的数据（字节）。
        :raises ValueError: 如果输入不是字节，或自定义码表无效，或解码失败。
        """
        if not isinstance(encoded_data, bytes):
            raise ValueError("输入必须是字节！")
        if custom_alphabet and (not isinstance(custom_alphabet, bytes) or len(custom_alphabet) != 64):
            raise ValueError("自定义码表必须为 64 个字节！")
        
        # 如果提供了自定义码表，先还原为标准码表
        if custom_alphabet:
            translation_table = bytes.maketrans(custom_alphabet, Base64CustomCodec.STANDARD_ALPHABET)
            encoded_data = encoded_data.translate(translation_table)
        
        # 标准 Base64 解码
        try:
            decoded_data = base64.b64decode(encoded_data)
        except Exception as e:
            raise ValueError(f"解码失败: {str(e)}")
        
        return decoded_data
