# -*- encoding: utf-8 -*-

'''
@File    :   pbe_for_py_helper.py
@Time    :   2025/07/16 12:13:33
@Author  :   test233
@Version :   1.0
'''

import hashlib
from Crypto.Cipher import AES, DES, DES3, ARC4
from Crypto.Util.Padding import pad, unpad


class PBECryptor:
    """
    基于密码的加密（PBE）工具类，支持 AES、DES、3DES、RC4 等算法。
    """
    ALGORITHMS = ["AES", "DES", "3DES", "RC4"]
    def __init__(self, password: str, algorithm: str = "AES", key_length: int = None):
        """
        初始化 PBE 工具
        :param password: 密码字符串
        :param algorithm: 加密算法，支持 "AES", "DES", "3DES", "RC4"
        :param key_length: 密钥长度（AES: 128/192/256, DES: 56, 3DES: 168, RC4: 任意）
        """
        self.password = password.encode('utf-8')
        self.algorithm = algorithm.upper()
        # 如果 key_length 为 None，根据算法设置默认值
        if key_length is None:
            if self.algorithm == "AES":
                self.key_length = 256  # AES 默认密钥长度为 256
        else:
            self.key_length = key_length

        # 验证算法和密钥长度是否匹配
        if self.algorithm == "AES":
            if self.key_length not in [128, 192, 256]:
                raise ValueError("AES key length must be 128, 192, or 256.")
        if self.algorithm not in PBECryptor.ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")

    def _bytes_to_key(self, salt: bytes, output: int) -> bytes:
        """
        根据密码和盐生成密钥和 IV
        :param salt: 盐值
        :param output: 输出长度
        :return: 密钥和 IV
        """
        assert len(salt) == 8, "Salt must be 8 bytes."
        data = self.password + salt
        key = hashlib.md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = hashlib.md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        加密明文
        :param plaintext: 明文字节数据
        :return: 加密后的字节数据
        """
        salt = hashlib.md5(self.password).digest()[:8]  # 生成 8 字节盐值
        if self.algorithm == "AES":
            key_iv_len = self.key_length // 8 + 16
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:self.key_length //
                             8], key_iv[self.key_length // 8:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_plaintext = pad(plaintext, AES.block_size)
        elif self.algorithm == "DES":
            key_iv_len = 8 + 8
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:8], key_iv[8:]
            cipher = DES.new(key, DES.MODE_CBC, iv)
            padded_plaintext = pad(plaintext, DES.block_size)
        elif self.algorithm == "3DES":
            key_iv_len = 24 + 8
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:24], key_iv[24:]
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            padded_plaintext = pad(plaintext, DES3.block_size)
        elif self.algorithm == "RC4":
            key_iv_len = 32
            key_iv = self._bytes_to_key(salt, key_iv_len)
            cipher = ARC4.new(key_iv)
            padded_plaintext = plaintext  # RC4 不需要填充
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        ciphertext = cipher.encrypt(padded_plaintext)
        return b"Salted__" + salt + ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        解密密文
        :param ciphertext: 加密后的字节数据
        :return: 解密后的明文字节数据
        """
        salt = ciphertext[8:16]
        if self.algorithm == "AES":
            key_iv_len = self.key_length // 8 + 16
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:self.key_length //
                             8], key_iv[self.key_length // 8:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(
                ciphertext[16:]), AES.block_size)
        elif self.algorithm == "DES":
            key_iv_len = 8 + 8
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:8], key_iv[8:]
            cipher = DES.new(key, DES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(
                ciphertext[16:]), DES.block_size)
        elif self.algorithm == "3DES":
            key_iv_len = 24 + 8
            key_iv = self._bytes_to_key(salt, key_iv_len)
            key, iv = key_iv[:24], key_iv[24:]
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(
                ciphertext[16:]), DES3.block_size)
        elif self.algorithm == "RC4":
            key_iv_len = 32
            key_iv = self._bytes_to_key(salt, key_iv_len)
            cipher = ARC4.new(key_iv)
            decrypted_data = cipher.decrypt(ciphertext[16:])
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        return decrypted_data


# 示例用法
if __name__ == "__main__":
    password = "my_password"
    plaintext = b"Hello, World!"
    # AES 加密（默认密钥长度 256）
    pbe_aes = PBECryptor(password, algorithm="AES")
    encrypted_text = pbe_aes.encrypt(plaintext)
    decrypted_text = pbe_aes.decrypt(encrypted_text)
    print(f"AES Encrypted: {encrypted_text}")
    print(f"AES Decrypted: {decrypted_text.decode('utf-8')}")
    # DES 加密
    pbe_des = PBECryptor(password, algorithm="DES")
    encrypted_text = pbe_des.encrypt(plaintext)
    decrypted_text = pbe_des.decrypt(encrypted_text)
    print(f"DES Encrypted: {encrypted_text}")
    print(f"DES Decrypted: {decrypted_text.decode('utf-8')}")
    # RC4 加密
    pbe_rc4 = PBECryptor(password, algorithm="RC4")
    encrypted_text = pbe_rc4.encrypt(plaintext)
    decrypted_text = pbe_rc4.decrypt(encrypted_text)
    print(f"RC4 Encrypted: {encrypted_text}")
    print(f"RC4 Decrypted: {decrypted_text.decode('utf-8')}")
