# -*- encoding: utf-8 -*-

'''
@File    :   sm_crypto_helper.py
@Time    :   2025/07/16 12:15:23
@Author  :   test233
@Version :   1.0
'''


import execjs

class SM2Cryptor:
    """
    SM2 加解密类，使用 execjs 调用 JavaScript 的 sm-crypto 库实现
    """
    def __init__(self):
        # 初始化 JavaScript 环境
        self.js_code = """
        const sm2 = require('sm-crypto').sm2;
        
        // 生成 SM2 密钥对
        function generateKeyPair() {
            let keypair = sm2.generateKeyPairHex();
            return {
                publicKey: keypair.publicKey,
                privateKey: keypair.privateKey
            };
        }
        
        // SM2 解密
        function decrypt(data, privateKey, cipherMode) {
            return sm2.doDecrypt(data, privateKey, cipherMode);
        }
        
        // SM2 加密
        function encrypt(data, publicKey, cipherMode) {
            return sm2.doEncrypt(data, publicKey, cipherMode);
        }
        """
        self.ctx = execjs.compile(self.js_code)
    
    def generate_keypair(self):
        """
        生成 SM2 密钥对
        :return: 包含公钥和私钥的字典 {'publicKey': ..., 'privateKey': ...}
        """
        return self.ctx.call("generateKeyPair")
    
    def encrypt(self, data: str, public_key: str, cipher_mode: int = 1) -> str:
        """
        SM2 加密
        :param data: 待加密数据
        :param public_key: 公钥
        :param cipher_mode: 加密模式 (1-C1C3C2, 0-C1C2C3)
        :return: 加密后的密文
        """
        return self.ctx.call("encrypt", data, public_key, cipher_mode)
    
    def decrypt(self, ciphertext: str, private_key: str, cipher_mode: int = 1) -> str:
        """
        SM2 解密
        :param ciphertext: 密文
        :param private_key: 私钥
        :param cipher_mode: 加密模式 (1-C1C3C2, 0-C1C2C3)
        :return: 解密后的明文
        """
        return self.ctx.call("decrypt", ciphertext, private_key, cipher_mode)

class SM3Cryptor:
    """
    SM3 哈希计算类，使用 execjs 调用 JavaScript 的 sm-crypto 库实现
    """
    def __init__(self):
        # 初始化 JavaScript 环境
        self.js_code = """
        const sm3 = require('sm-crypto').sm3;
        
        // SM3 普通哈希
        function hash(data) {
            return sm3(data);
        }
        
        // SM3 HMAC 哈希
        function hmac(data, key) {
            return sm3(data, {
                key: key
            });
        }
        """
        self.ctx = execjs.compile(self.js_code)
    
    def hash(self, data: str) -> str:
        """
        SM3 普通哈希计算
        :param data: 待哈希数据
        :return: 哈希值(16进制字符串)
        """
        return self.ctx.call("hash", data)
    
    def hmac(self, data: str, key: str) -> str:
        """
        SM3 HMAC 哈希计算
        :param data: 待哈希数据
        :param key: HMAC密钥(16进制字符串)
        :return: 哈希值(16进制字符串)
        """
        return self.ctx.call("hmac", data, key)

    
class SM4Cryptor:
    """SM4 加密解密核心类"""
    MODES = ['ecb', 'cbc']
    PADDINGS = ['pkcs#7', 'pkcs#7']
    def __init__(self):
        self.js_code = """
        const sm4 = require('sm-crypto').sm4;
        
        function generateKey() {
            // 生成 128 比特(16字节)的随机密钥
            const chars = '0123456789abcdef';
            let result = '';
            for (let i = 0; i < 32; i++) {
                result += chars[Math.floor(Math.random() * chars.length)];
            }
            return result;
        }
        
        function encrypt(data, key, options = {}) {
            return sm4.encrypt(data, key, options);
        }
        
        function decrypt(data, key, options = {}) {
            return sm4.decrypt(data, key, options);
        }
        """
        self.ctx = execjs.compile(self.js_code)
    
    def generate_key(self):
        """生成 128 比特 SM4 密钥"""
        return self.ctx.call("generateKey")
    
    def encrypt(self, data, key, mode='ecb', iv=None, padding='pkcs#7', output='hex'):
        """SM4 加密"""
        options = {
            'mode': mode,
            'padding': padding,
            'output': output
        }
        if mode == 'cbc' and iv:
            options['iv'] = iv

        return self.ctx.call("encrypt", data, key, options)
    
    def decrypt(self, ciphertext, key, mode='ecb', iv=None, padding='pkcs#7', output='utf8'):
        """SM4 解密"""
        options = {
            'mode': mode,
            'padding': padding,
            'output': output
        }
        if mode == 'cbc' and iv:
            options['iv'] = iv
        return self.ctx.call("decrypt", ciphertext, key, options)


def test_sm4_cryptor():
    """
    测试 SM2 加解密功能
    """
    # print("=== SM4 加解密测试 ===")
    
    # 创建 SM2 加密器实例
    cryptor = SM4Cryptor()
    
    # 生成密钥
    key = cryptor.generate_key()
    # print(f"生成的密钥: {key}")
    # 测试数据
    data = "Hello, SM4!"
    # print(f"\n原始数据: {data}")
    for mode in SM4Cryptor.MODES:
        # print(f"\n测试模式: {mode}")
        # 生成 IV (仅在 CBC 模式下需要)
        iv = None
        if mode == 'cbc':
            iv = '0123456789abcdeffedcba9876543210'
        for padding in SM4Cryptor.PADDINGS:
            # print(f"使用填充方式: {padding}")
            # 加密
            ciphertext = cryptor.encrypt(data, key, mode=mode, iv=iv, padding=padding)
            # print(f"\n加密结果: {ciphertext}")
            # 解密
            decrypted_data = cryptor.decrypt(ciphertext, key, mode=mode, iv=iv, padding=padding)
            # print(f"解密结果: {decrypted_data}")
            assert decrypted_data == data, f"{mode} 模式解密结果与原始数据不一致!"
    print(f"sm4 测试通过")


    
    


def test_sm2_cryptor():
    """
    测试 SM2 加解密功能
    """
    # print("=== SM2 加解密测试 ===")
    
    # 创建 SM2 加密器实例
    cryptor = SM2Cryptor()
    
    # 生成密钥对
    keypair = cryptor.generate_keypair()
    # print(f"公钥: {keypair['publicKey']}")
    # print(f"私钥: {keypair['privateKey']}")
    
    # 测试数据
    test_data = "Hello, SM2 国密算法!"
    # print(f"\n原始数据: {test_data}")
    
    # 加密 (默认 C1C3C2 模式)
    ciphertext = cryptor.encrypt(test_data, keypair['publicKey'])
    # print(f"\n加密结果 (C1C3C2): {ciphertext}")
    
    # 解密
    plaintext = cryptor.decrypt(ciphertext, keypair['privateKey'])
    # print(f"解密结果: {plaintext}")
    assert plaintext == test_data, "解密结果与原始数据不一致!"
    
    # 测试 C1C2C3 模式
    ciphertext_mode0 = cryptor.encrypt(test_data, keypair['publicKey'], 0)
    # print(f"\n加密结果 (C1C2C3): {ciphertext_mode0}")
    
    plaintext_mode0 = cryptor.decrypt(ciphertext_mode0, keypair['privateKey'], 0)
    # print(f"解密结果: {plaintext_mode0}")
    assert plaintext_mode0 == test_data, "C1C2C3 模式解密失败!"
    
    print("sm2 测试通过!")


if __name__ == "__main__":
    # 使用前请确保已安装:
    # pip install execjs
    # npm install sm-crypto
    test_sm4_cryptor()
    test_sm2_cryptor()

