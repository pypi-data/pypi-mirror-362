# -*- encoding: utf-8 -*-

'''
@File    :   pycryptodome_helper.py
@Time    :   2025/07/16 12:13:42
@Author  :   test233
@Version :   1.0
'''

from Crypto.PublicKey import RSA
from Crypto.Hash import MD2, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
from typing import Tuple, Optional
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import ARC4
from Crypto.Cipher import ARC2
from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from Crypto.Cipher import AES

class RSACryptor:

    KEY_SIZE = [512, 1024, 2048, 4096]
    KEY_FORMATS = ["PKCS#1", "PKCS#8"]
    PADDINGS = ["OAEP", "PKCS1", "NONE"]
    HASH_ALGOS = ["MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
    MGF_HASH_ALGOS = ["MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
    
    def __init__(self, private_key: Optional[str] = None, public_key: Optional[str] = None,
                 padding_mode: str = "OAEP", hash_algo: Optional[str] = "SHA256",
                 mgf_hash_algo: Optional[str] = "SHA256", passphrase: Optional[str] = None):
        """
        初始化 RSACryptor 类。
        :param private_key: PEM 格式的私钥字符串
        :param public_key: PEM 格式的公钥字符串
        :param padding_mode: RSA 填充模式，支持 "OAEP", "PKCS1", "NONE"
        :param hash_algo: Hash 算法，支持 "MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"
        :param mgf_hash_algo: MGF Hash 算法，支持 "MD2", "MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"
        :param passphrase: 私钥的密码（如果私钥是加密的）
        """
        # 导入私钥（如果提供了密码）
        self.private_key = RSA.import_key(private_key, passphrase=passphrase) if private_key else None
        self.public_key = RSA.import_key(public_key) if public_key else None
        self.padding_mode = padding_mode
        # 设置 Hash 和 MGF Hash 算法
        if padding_mode == "OAEP":
            if not hash_algo or not mgf_hash_algo:
                raise ValueError("Hash and MGFHash algorithms are required for OAEP padding mode")
            self.hash_algo = self._get_hash_algo(hash_algo)
            self.mgf_hash_algo = self._get_hash_algo(mgf_hash_algo)
        else:
            self.hash_algo = None
            self.mgf_hash_algo = None
    def _get_hash_algo(self, algo_name: str):
        """
        根据算法名称返回对应的 Hash 算法对象。
        :param algo_name: Hash 算法名称
        :return: Hash 算法对象
        """
        hash_algo_map = {
            "MD2": MD2,
            "MD5": MD5,
            "SHA1": SHA1,
            "SHA224": SHA224,
            "SHA256": SHA256,
            "SHA384": SHA384,
            "SHA512": SHA512
        }
        if algo_name in hash_algo_map:
            return hash_algo_map[algo_name]
        else:
            raise ValueError(f"Unsupported hash algorithm: {algo_name}")
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        使用公钥加密数据。
        :param plaintext: 明文数据（字节类型）
        :return: 加密后的数据（字节类型）
        """
        if not self.public_key:
            raise ValueError("Public key is not provided for encryption")
        if self.padding_mode == "OAEP":
            cipher = PKCS1_OAEP.new(self.public_key, hashAlgo=self.hash_algo,
                                    mgfunc=lambda x, y: PKCS1_OAEP.MGF1(x, y, self.mgf_hash_algo))
        elif self.padding_mode == "PKCS1":
            cipher = PKCS1_v1_5.new(self.public_key)
        elif self.padding_mode == "NONE":
            cipher = self.public_key
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")
        return cipher.encrypt(plaintext)
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        使用私钥解密数据。
        :param ciphertext: 加密后的数据（字节类型）
        :return: 解密后的明文数据（字节类型）
        """
        if not self.private_key:
            raise ValueError("Private key is not provided for decryption")
        if self.padding_mode == "OAEP":
            cipher = PKCS1_OAEP.new(self.private_key, hashAlgo=self.hash_algo,
                                   mgfunc=lambda x, y: PKCS1_OAEP.MGF1(x, y, self.mgf_hash_algo))
        elif self.padding_mode == "PKCS1":
            cipher = PKCS1_v1_5.new(self.private_key)
        elif self.padding_mode == "NONE":
            cipher = self.private_key
        else:
            raise ValueError(f"Unsupported padding mode: {self.padding_mode}")
        return cipher.decrypt(ciphertext)
    @staticmethod
    def generate_key_pair(key_size: int = 2048, key_format: str = "PKCS#8", passphrase: Optional[str] = None) -> Tuple[str, str]:
        """
        生成 RSA 密钥对。
        :param key_size: 密钥长度，支持 512, 1024, 2048, 4096
        :param key_format: 密钥格式，支持 "PKCS#1" 和 "PKCS#8"
        :param passphrase: 用于加密私钥的密码（可选）
        :return: 生成的密钥对（私钥、公钥）
        """
        if key_size not in [512, 1024, 2048, 4096]:
            raise ValueError("Unsupported key size. Supported sizes: 512, 1024, 2048, 4096")
        if key_format not in ['PKCS#1', 'PKCS#8']:
            raise ValueError("Unsupported key format. Supported formats: 'PKCS#1', 'PKCS#8'")
        # 生成密钥对
        private_key = RSA.generate(key_size)
        public_key = private_key.publickey()
        # 根据格式导出密钥
        if key_format == 'PKCS#1':
            private_key_pem = private_key.export_key(format='PEM', passphrase=passphrase).decode()
            public_key_pem = public_key.export_key(format='PEM').decode()
        elif key_format == 'PKCS#8':
            private_key_pem = private_key.export_key(format='PEM', pkcs=8, passphrase=passphrase).decode()
            public_key_pem = public_key.export_key(format='PEM', pkcs=8).decode()
        return private_key_pem, public_key_pem

 
class RC4Cryptor:
    """
    RC4 加解密工具类。
    输入输出均为字节格式（bytes）。
    """
    def __init__(self, key: bytes):
        """
        初始化 RC4 加解密工具
        :param key: 密钥，字节格式（1 到 256 字节）
        """
        if len(key) < 1 or len(key) > 256:
            raise ValueError("RC4 key must be between 1 and 256 bytes long")
        self.key = key
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 RC4 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        cipher = ARC4.new(self.key)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 RC4 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = ARC4.new(self.key)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext


class RC2Cryptor:
    """
    RC2 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # RC2支持的模式
    MODES = {
        'CBC': ARC2.MODE_CBC,
        'ECB': ARC2.MODE_ECB,
        'CFB': ARC2.MODE_CFB,
        'OFB': ARC2.MODE_OFB,
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']

    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7", effective_keylen: Optional[int] = None):
        """
        初始化 RC2 加解密工具
        :param key: 密钥，字节格式（1 到 128 字节）
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        :param effective_keylen: 有效密钥长度（位），可选，默认为密钥长度
        """
        if len(key) < 1 or len(key) > 128:
            raise ValueError("RC2 key must be between 1 and 128 bytes long")
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported RC2 mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode
        self.effective_keylen = effective_keylen if effective_keylen is not None else len(key) * 8

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 RC2 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        padded_data = self._pad(plaintext)
        cipher = self._init_rc2()
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 RC2 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = self._init_rc2()
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = self._unpad(padded_plaintext)
        return plaintext

    def _init_rc2(self) -> ARC2:
        """
        初始化 RC2 对象
        :return: RC2 对象
        """
        if self.mode in (ARC2.MODE_CBC, ARC2.MODE_CFB, ARC2.MODE_OFB):
            return ARC2.new(self.key, self.mode, self.iv, effective_keylen=self.effective_keylen)
        elif self.mode == ARC2.MODE_ECB:
            return ARC2.new(self.key, self.mode, effective_keylen=self.effective_keylen)
        else:
            raise ValueError(f"Unsupported RC2 mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = 8  # RC2的块大小是8字节
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


class DESCryptor:
    """
    DES 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # DES支持的模式
    MODES = {
        'CBC': DES.MODE_CBC,
        'ECB': DES.MODE_ECB,
        'CFB': DES.MODE_CFB,
        'OFB': DES.MODE_OFB,
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']

    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7"):
        """
        初始化 DES 加解密工具
        :param key: 密钥，字节格式（8字节）
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        """
        if len(key) != 8:
            raise ValueError("DES key must be 8 bytes long")
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported DES mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 DES 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        padded_data = self._pad(plaintext)
        cipher = self._init_des()
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 DES 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        cipher = self._init_des()
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = self._unpad(padded_plaintext)
        return plaintext

    def _init_des(self) -> DES:
        """
        初始化 DES 对象
        :return: DES 对象
        """
        if self.mode in (DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB):
            return DES.new(self.key, self.mode, self.iv)
        elif self.mode == DES.MODE_ECB:
            return DES.new(self.key, self.mode)
        else:
            raise ValueError(f"Unsupported DES mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = 8  # DES的块大小是8字节
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


class AESCryptor:
    """
    AES 加解密工具类，支持多种填充模式和加密模式。
    输入输出均为字节格式（bytes）。
    """
    # AES支持的模式
    MODES = {
        'CBC': AES.MODE_CBC,
        'ECB': AES.MODE_ECB,
        'CFB': AES.MODE_CFB,
        'OFB': AES.MODE_OFB,
        'CTR': AES.MODE_CTR,
        'GCM': AES.MODE_GCM
    }
    # 填充方式
    PADDINGS = ['PKCS7', 'ISO7816', 'X923', 'ZeroPadding']
    LENGTHS = [16, 24, 32]  # 支持的密钥长度
    def __init__(self, key: bytes, mode: str, iv: Optional[bytes] = None, padding_mode: str = "PKCS7", key_length: int = 16):
        """
        初始化 AES 加解密工具
        :param key: 密钥，字节格式
        :param mode: 加密模式，支持 CBC, ECB, CFB, OFB, CTR, GCM
        :param iv: 初始化向量（IV），字节格式，CBC/CFB/OFB/GCM 模式需要
        :param padding_mode: 填充模式，支持 "PKCS7", "ZeroPadding", "ISO7816", "X923"
        :param key_length: 密钥长度，支持 16（128位）、24（192位）、32（256位）
        """
        self.key = key
        self.mode = self.MODES.get(mode)
        if self.mode is None:
            raise ValueError(f"Unsupported AES mode: {mode}")
        self.iv = iv if iv is not None else b''
        self.padding_mode = padding_mode
        if self.padding_mode not in self.PADDINGS:
            raise ValueError(f"Unsupported padding mode: {padding_mode}")
        if key_length not in self.LENGTHS:
            raise ValueError(f"Unsupported key length: {key_length}")
        self.key_length = key_length

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        对字节数据进行 AES 加密
        :param plaintext: 明文数据，字节格式
        :return: 加密后的数据，字节格式
        """
        if self.mode == AES.MODE_GCM:
            # GCM 模式不需要填充
            cipher = self._init_aes()
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            return cipher.nonce + tag + ciphertext
        else:
            padded_data = self._pad(plaintext)
            cipher = self._init_aes()
            ciphertext = cipher.encrypt(padded_data)
            return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        对字节数据进行 AES 解密
        :param ciphertext: 加密数据，字节格式
        :return: 解密后的数据，字节格式
        """
        if self.mode == AES.MODE_GCM:
            # GCM 模式不需要填充
            nonce = ciphertext[:16]
            tag = ciphertext[16:32]
            ciphertext = ciphertext[32:]
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        else:
            cipher = self._init_aes()
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = self._unpad(padded_plaintext)
            return plaintext

    def _init_aes(self) -> AES:
        """
        初始化 AES 对象
        :return: AES 对象
        """
        if self.mode in (AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB):
            return AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            return AES.new(self.key, self.mode)
        elif self.mode == AES.MODE_CTR:
            return AES.new(self.key, self.mode, nonce=self.iv[:8])
        elif self.mode == AES.MODE_GCM:
            return AES.new(self.key, self.mode, nonce=self.iv)
        else:
            raise ValueError(f"Unsupported AES mode: {self.mode}")

    def _pad(self, data: bytes) -> bytes:
        """
        填充数据
        :param data: 原始数据，字节格式
        :return: 填充后的数据，字节格式
        """
        block_size = self.key_length
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
def test_aes_cryptor():
    key = b'0123456789abcdef'  # 16字节密钥
    iv = b'1234567890abcdef'   # 16字节IV
    plaintext = b"Hello, AES!"  # 明文数据
    for mode in AESCryptor.MODES:
        for padding_mode in AESCryptor.PADDINGS:
            try:
                cryptor = AESCryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("aes tests passed!")
# 测试代码
def test_des_cryptor():
    key = b'01234567'  # 8字节密钥
    iv = b'12345678'   # 8字节IV
    plaintext = b"Hello, DES!"  # 明文数据
    for mode in DESCryptor.MODES:
        for padding_mode in DESCryptor.PADDINGS:
            try:
                cryptor = DESCryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("des tests passed!")
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
    print("3des tests passed!")
# 测试代码
def test_rc2_cryptor():
    key = b'01234567'               # 8字节密钥
    iv = b'12345678'                # 8字节IV
    plaintext = b"Hello, RC2!"      # 明文数据
    for mode in RC2Cryptor.MODES:
        for padding_mode in RC2Cryptor.PADDINGS:
            try:
                cryptor = RC2Cryptor(key, mode, iv, padding_mode)
                ciphertext = cryptor.encrypt(plaintext)
                decrypted_text = cryptor.decrypt(ciphertext)
                assert decrypted_text == plaintext, f'{mode}/{padding_mode} test failed'
            except Exception as e:
                print(f'{mode}/{padding_mode} test failed with error: {e}')
    print("rc2 tests passed!")

def test_rsa_cryptor():
    """
    测试 RSACryptor 类的基本功能。
    """
    # 生成密钥对
    private_key, public_key = RSACryptor.generate_key_pair(key_size=2048, key_format="PKCS#8")
    # print("Private Key:\n", private_key)
    # print("Public Key:\n", public_key)

    # 初始化 RSACryptor
    rsa_cryptor = RSACryptor(private_key=private_key, public_key=public_key, padding_mode="OAEP",
                             hash_algo="SHA256", mgf_hash_algo="SHA256")

    # 测试加密和解密
    plaintext = b"Hello, RSA!"
    encrypted = rsa_cryptor.encrypt(plaintext)
    # print("Encrypted:", encrypted)
    
    decrypted = rsa_cryptor.decrypt(encrypted)
    # print("Decrypted:", decrypted.decode())  # 将字节解码为字符串
    assert decrypted == plaintext, "Decryption failed: decrypted text does not match original plaintext"
    print("rsa Test passed!")

# 测试代码
def test_rc4_cryptor():
    key = b'01234567'               # 8字节密钥
    plaintext = b"Hello, RC4!"      # 明文数据
    cryptor = RC4Cryptor(key)
    ciphertext = cryptor.encrypt(plaintext)
    # print(f"Ciphertext: {ciphertext}")
    decrypted_text = cryptor.decrypt(ciphertext)
    # print(f"Decrypted Text: {decrypted_text.decode()}")
    assert decrypted_text == plaintext, "Test failed!"
    print("rc4 Test passed!")

# 示例用法
if __name__ == "__main__":
    test_rsa_cryptor()
    test_rc4_cryptor()
    test_rc2_cryptor()
    test_3des_cryptor()
    test_des_cryptor()
    test_aes_cryptor()


# import base64
# import binascii
# from Crypto.Util.Padding import pad,unpad
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import DES
# from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

# def rsa_encrypt(msg, key, encoding='utf8'):
#     public_key = RSA.importKey(key)
#     cipher = PKCS1_cipher.new(public_key)
#     encrypt_text = base64.b64encode(cipher.encrypt(msg.encode(encoding)))
#     return encrypt_text.decode(encoding)

# class DES_ECB:

#     def __init__(self, key):

#         key = key.encode('utf8')
#         key = key[:8] if len(key) >= 8 else key + (8-len(key))*b'\0'
#         self.cipher = DES.new(key, DES.MODE_ECB)

#     def encrypt(self, text):
#         ct = self.cipher.encrypt(pad(text.encode('utf8'), 8))
#         return binascii.b2a_base64(ct).decode('utf8').strip()

#     def decrypt(self, text):
#         text = binascii.a2b_base64(text)
#         ct = self.cipher.decrypt(text)
#         return unpad(ct,8).decode('utf8').strip()