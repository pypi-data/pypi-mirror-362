# -*- encoding: utf-8 -*-

'''
@File    :   tripledes_helper.py
@Time    :   2025/07/16 12:16:18
@Author  :   test233
@Version :   1.0
'''

from Crypto.Cipher import DES3
from typing import Union, Optional

class TripleDESCryptor:
    """
    Triple DES (3DES) 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # 3DES支持的模式
    MODES = {
        'CBC': DES3.MODE_CBC,
        'ECB': DES3.MODE_ECB,
        'CFB': DES3.MODE_CFB,
        'OFB': DES3.MODE_OFB,
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']

    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7"):
        """
        初始化 3DES 加解密工具
        :param key: 密钥，字节格式（16 或 24 字节）16 字节密钥：实际使用 112 位（两阶段 DES）。24 字节密钥：实际使用 168 位（三阶段 DES）
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        """
        if len(key) not in (16, 24):
            raise ValueError("3DES key must be 16 or 24 bytes long")
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported 3DES mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 3DES 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        padded_data = self._pad(plaintext)
        cipher = self._init_3des()
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 3DES 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = self._init_3des()
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = self._unpad(padded_plaintext)
        return plaintext

    def _init_3des(self) -> DES3:
        """
        初始化 3DES 对象
        :return: 3DES 对象
        """
        if self.mode in (DES3.MODE_CBC, DES3.MODE_CFB, DES3.MODE_OFB):
            return DES3.new(self.key, self.mode, self.iv)
        elif self.mode == DES3.MODE_ECB:
            return DES3.new(self.key, self.mode)
        else:
            raise ValueError(f"Unsupported 3DES mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = 8  # 3DES的块大小是8字节
        padding_length = block_size - (len(data) % block_size)
        if self.padding_mode == "PKCS7":
            return data + bytes([padding_length] * padding_length)
        elif self.padding_mode == "ZeroPadding":
            return data + bytes([0] * padding_length)
        elif self.padding_mode == "ISO7816":
            return data + bytes([0x80]) + bytes([0x00] * (padding_length - 1))
        elif self.padding_mode == "X923":
            return data + bytes([0x00] * (padding_length - 1)) + bytes([padding_length])
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")

    def _unpad(self, data: bytes) -> bytes:
        """
        去除填充
        :param data: 填充后的数据，字节格式
        :return: 去除填充后的数据，字节格式
        """
        if self.padding_mode == "PKCS7":
            padding_length = data[-1]
            return data[:-padding_length]
        elif self.padding_mode == "ZeroPadding":
            return data.rstrip(b'\x00')
        elif self.padding_mode == "ISO7816":
            return data.rstrip(b'\x00')[:-1]
        elif self.padding_mode == "X923":
            padding_length = data[-1]
            return data[:-padding_length]
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")

# 测试代码
def test_3des_cryptor():
    key = b'0123456789abcdef01234567'  # 24字节密钥
    iv = b'12345678'                   # 8字节IV
    plaintext = b"Hello, 3DES!"        # 明文数据
    for mode in TripleDESCryptor.MODES:
        for padding_mode in TripleDESCryptor.PADDINGS:
            try:
                cryptor = TripleDESCryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("All tests passed!")

if __name__ == "__main__":
    test_3des_cryptor()
