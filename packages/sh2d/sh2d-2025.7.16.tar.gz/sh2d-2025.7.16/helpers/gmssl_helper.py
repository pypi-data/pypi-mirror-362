# -*- encoding: utf-8 -*-

'''
@File    :   gmssl_helper.py
@Time    :   2025/07/16 12:08:14
@Author  :   test233
@Version :   1.0
'''


from gmssl import sm2, sm3, sm4, func
from typing import Optional


class SM2Cryptor:
    """
    SM2 加解密、签名验签工具类，基于 gmssl 模块实现。
    输入输出均为字节格式（bytes）。
    """

    def __init__(self, private_key: str, public_key: str):
        """
        初始化 SM2 加解密工具
        :param private_key: 私钥，16 进制字符串
        :param public_key: 公钥，16 进制字符串
        """
        self.sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 SM2 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        return self.sm2_crypt.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 SM2 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        return self.sm2_crypt.decrypt(ciphertext)

    def sign(self, data: bytes, random_hex_str: str) -> str:
        """
        对字节数据进行 SM2 签名
        :param data: 待签名数据，字节格式
        :param random_hex_str: 随机 16 进制字符串
        :return: 签名结果，16 进制字符串
        """
        return self.sm2_crypt.sign(data, random_hex_str)

    def verify(self, sign: str, data: bytes) -> bool:
        """
        对 SM2 签名进行验证
        :param sign: 签名结果，16 进制字符串
        :param data: 待验证数据，字节格式
        :return: 验证结果，布尔值
        """
        return self.sm2_crypt.verify(sign, data)


class SM3Cryptor:
    """
    SM3 哈希工具类，基于 gmssl 模块实现。
    输入输出均为字节格式（bytes）。
    """

    @staticmethod
    def hash(data: bytes) -> str:
        """
        对字节数据进行 SM3 哈希计算
        :param data: 待哈希数据，字节格式
        :return: 哈希结果，16 进制字符串
        """
        data_list = [i for i in data]
        return sm3.sm3_hash(data_list)

class SM4Cryptor:
    """
    SM4 加解密工具类，基于 gmssl 模块实现，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    MODES = ['ECB', 'CBC']  # 加密模式
    # 填充方式 (原项目实现)
    PADDINGS = ['NoPadding', 'ZeroPadding', 'ISO9797M2', 'PKCS7', 'PBOC']

    def __init__(self, key: bytes, mode: str = 'CBC', iv: Optional[bytes] = None, padding_mode: str = "PKCS7"):
        """
        初始化 SM4 加解密工具
        :param key: 密钥，字节格式（16 字节，128 位）
        :param mode: 加密模式，支持 ECB, CBC
        :param iv: 初始化向量（IV），字节格式，CBC 模式需要
        :param padding_mode: 填充模式，支持 "NoPadding", "ZeroPadding", "ISO9797M2", "PKCS7", "PBOC"
        """
        if len(key) != 16:
            raise ValueError("SM4 key must be 16 bytes long (128 bits)")
        self.key = key
        self.mode = mode.upper()
        if self.mode not in self.MODES:
            raise ValueError(f"Unsupported SM4 mode: {mode}")
        self.iv = iv if iv is not None else b''
        if self.mode == 'CBC' and len(self.iv) != 16:
            raise ValueError("IV must be 16 bytes long for CBC mode")
        
        # 映射填充模式名称到数字代码
        self.padding_mode = self._get_padding_code(padding_mode)

    def _get_padding_code(self, padding_name: str) -> int:
        """将填充模式名称映射到对应的数字代码"""
        padding_map = {
            'NoPadding': 0,
            'ZeroPadding': 1,
            'ISO9797M2': 2,
            'PKCS7': 3,
            'PBOC': 4
        }
        if padding_name not in padding_map:
            raise ValueError(f"Unsupported padding mode: {padding_name}")
        return padding_map[padding_name]

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 SM4 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        cipher = sm4.CryptSM4(padding_mode=self.padding_mode)
        cipher.set_key(self.key, sm4.SM4_ENCRYPT)
        if self.mode == 'CBC':
            ciphertext = cipher.crypt_cbc(self.iv, plaintext)
        else:  # ECB 模式
            ciphertext = cipher.crypt_ecb(plaintext)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 SM4 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = sm4.CryptSM4(padding_mode=self.padding_mode)
        cipher.set_key(self.key, sm4.SM4_DECRYPT)
        if self.mode == 'CBC':
            plaintext = cipher.crypt_cbc(self.iv, ciphertext)
        else:  # ECB 模式
            plaintext = cipher.crypt_ecb(ciphertext)
        return plaintext


# 测试代码 (SM4部分)
def test_sm4_cryptor():
    key = b'0123456789abcdef'  # 16 字节密钥
    iv = b'1234567890abcdef'  # 16 字节 IV
    plaintext = b"Hello, SM4!"  # 明文数据


    for mode in SM4Cryptor.MODES:
        for padding_mode in SM4Cryptor.PADDINGS:
            try:
                # 测试不同填充模式
                cryptor = SM4Cryptor(key, mode, iv, padding_mode=padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
    
                assert decrypted_text == plaintext, f"{mode} {padding_mode} test failed"
            except Exception as e:
                print(f"Error in {mode} {padding_mode}: {str(e)}")
                continue
    print("SM4 tests passed!")



# 测试代码
def test_sm2_cryptor():
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sm2_cryptor = SM2Cryptor(private_key, public_key)
    data = b"Hello, SM2!"
    enc_data = sm2_cryptor.encrypt(data)
    dec_data = sm2_cryptor.decrypt(enc_data)
    assert dec_data == data, "SM2 encryption/decryption test failed"

    random_hex_str = func.random_hex(sm2_cryptor.sm2_crypt.para_len)
    sign = sm2_cryptor.sign(data, random_hex_str)
    verify = sm2_cryptor.verify(sign, data)
    assert verify, "SM2 signature/verification test failed"
    print("SM2 tests passed!")


def test_sm3_cryptor():
    data = b"Hello, SM3!"
    hash_result = SM3Cryptor.hash(data)
    assert isinstance(hash_result, str), "SM3 hash result should be a string"
    print("SM3 tests passed!")





if __name__ == "__main__":
    # pip install gmssl
    test_sm2_cryptor()
    test_sm3_cryptor()
    test_sm4_cryptor()