# -*- encoding: utf-8 -*-

'''
@File    :   crypto_js_helper.py
@Time    :   2025/07/16 12:07:28
@Author  :   test233
@Version :   1.0
'''


import execjs

class PBECryptor:
    """
    PBE 加解密类，使用 js2py 调用 JavaScript 方法实现加密和解密。
    """
    ENCRYPT_TYPES = ["AES", "DES", "Rabbit", "RC4", "TripleDES"]
    def __init__(self):
        # 定义 JavaScript 代码
        self.js_code = '''
var CryptoJS = require("crypto-js");

function do_encrypt(encrypt_type, content, pwd) {
  var ret = "";
  switch (encrypt_type) {
    case "AES":
      ret = CryptoJS.AES.encrypt(content, pwd);
      break;
    case "DES":
      ret = CryptoJS.DES.encrypt(content, pwd);
      break;
    case "Rabbit":
      ret = CryptoJS.Rabbit.encrypt(content, pwd);
      break;
    case "RC4":
      ret = CryptoJS.RC4.encrypt(content, pwd);
      break;
    case "TripleDES":
      ret = CryptoJS.TripleDES.encrypt(content, pwd);
      break;
  }
  return ret.toString();
};

function do_decrypt(encrypt_type, content, pwd) {
  var ret = "";
  switch (encrypt_type) {
    case "AES":
      ret = CryptoJS.AES.decrypt(content, pwd);
      break;
    case "DES":
      ret = CryptoJS.DES.decrypt(content, pwd);
      break;
    case "Rabbit":
      ret = CryptoJS.Rabbit.decrypt(content, pwd);
      break;
    case "RC4":
      ret = CryptoJS.RC4.decrypt(content, pwd);
      break;
    case "TripleDES":
      ret = CryptoJS.TripleDES.decrypt(content, pwd);
      break;
  }
  return ret.toString(CryptoJS.enc.Utf8);
};
'''
        # 初始化 execjs 环境
        self.ctx = execjs.compile(self.js_code)


    def encrypt(self, encrypt_type: str, content: str, password: str) -> str:
        """
        加密方法
        :param encrypt_type: 加密类型（AES、DES、Rabbit、RC4、TripleDES）
        :param content: 明文内容
        :param password: 密码
        :return: 加密后的密文
        """
        if encrypt_type not in self.ENCRYPT_TYPES:
            raise ValueError(f"Unsupported encrypt type: {encrypt_type}")
        return self.ctx.call("do_encrypt",encrypt_type, content, password)

    def decrypt(self, encrypt_type: str, ciphertext: str, password: str) -> str:
        """
        解密方法
        :param encrypt_type: 加密类型（AES、DES、Rabbit、RC4、TripleDES）
        :param ciphertext: 密文
        :param password: 密码
        :return: 解密后的明文
        """
        if encrypt_type not in self.ENCRYPT_TYPES:
            raise ValueError(f"Unsupported encrypt type: {encrypt_type}")
        return self.ctx.call("do_decrypt",encrypt_type, ciphertext, password)
    

class HashCalculator:
    """
    hash计算类。
    """
    ALGORITHMS = ["SHA1", "SHA224", "SHA256", "SHA384", "SHA512", "MD5", "HmacSHA1", "HmacSHA224", "HmacSHA256", "HmacSHA384", "HmacSHA512", "HmacMD5"]

    def __init__(self):
        # 定义 JavaScript 代码
        self.js_code = '''
var CryptoJS = require("crypto-js");

// 散列哈希
function calc(type, content, pwd = "") {
  var ret = "";
  switch (type) {
    case "SHA1":
      ret = CryptoJS.SHA1(content);
      break;
    case "SHA224":
      ret = CryptoJS.SHA224(content);
      break;
    case "SHA256":
      ret = CryptoJS.SHA256(content);
      break;
    case "SHA384":
      ret = CryptoJS.SHA384(content);
      break;
    case "SHA512":
      ret = CryptoJS.SHA512(content);
      break;
    case "MD5":
      ret = CryptoJS.MD5(content);
      break;
    case "HmacSHA1":
      ret = CryptoJS.HmacSHA1(content, pwd);
      break;
    case "HmacSHA224":
      ret = CryptoJS.HmacSHA224(content, pwd);
      break;
    case "HmacSHA256":
      ret = CryptoJS.HmacSHA256(content, pwd);
      break;
    case "HmacSHA384":
      ret = CryptoJS.HmacSHA384(content, pwd);
      break;
    case "HmacSHA512":
      ret = CryptoJS.HmacSHA512(content, pwd);
      break;
    case "HmacMD5":
      ret = CryptoJS.HmacMD5(content, pwd);
      break;
  }
  return ret.toString();
}
'''
        # 初始化 execjs 环境
        self.ctx = execjs.compile(self.js_code)


    def hash(self,hash_type: str, content: str, password: str = "") -> str:
        """
        加密方法
        :param hash_type: 哈希类型（SHA1、SHA224、SHA256、SHA384、SHA512、MD5、HmacSHA1、HmacSHA224、HmacSHA256、HmacSHA384、HmacSHA512、HmacMD5）
        :param content: 内容
        :param password: 密码
        :return: hash后的结果
        """
        if hash_type not in self.ALGORITHMS:
            raise ValueError(f"Unsupported hash type: {hash_type}")
        return self.ctx.call("calc", hash_type, content, password)



def test_all_encrypt_types(content: str, password: str):
    """
    测试所有加密类型的加解密功能
    :param content: 明文内容
    :param password: 密码
    """
    encrypt_types = ["AES", "DES", "Rabbit", "RC4", "TripleDES"]
    cryptor = PBECryptor()
    for encrypt_type in encrypt_types:
        try:
            # 加密
            ciphertext = cryptor.encrypt(encrypt_type, content, password)
            # print(f"[{encrypt_type}] 加密结果: {ciphertext}")
            # 解密
            plaintext = cryptor.decrypt(encrypt_type, ciphertext, password)
            # print(f"[{encrypt_type}] 解密结果: {plaintext}")
            # 验证解密结果是否与原文一致
            assert plaintext == content, f"解密结果与原文不一致: {plaintext}"
            print(f"PBE [{encrypt_type}] 测试通过！")
        except Exception as e:
            print(f"PBE [{encrypt_type}] 测试失败: {str(e)}")

def test_all_hash_types(content: str, password: str = ""):
    """
    测试所有哈希类型的计算功能
    :param content: 内容
    :param password: 密码（仅对 HMAC 哈希类型有效）
    """
    for hash_type in HashCalculator.ALGORITHMS:
        try:
            # 创建 HashCalculator 实例
            hasher = HashCalculator()
            # 计算哈希值
            hash_value = hasher.hash(hash_type, content, password)
            print(f"[{hash_type}] 哈希结果: {hash_value}")
        except Exception as e:
            print(f"[{hash_type}] 哈希计算失败: {str(e)}")
        # print("-" * 50)
# 测试代码
if __name__ == "__main__":
    # pip install execjs2
    # npm install crypto-js
    test_all_encrypt_types("Hello, World","123456")
    test_all_hash_types("test", "123456")
    # cryptor = PBECryptor()
    # print(cryptor.decrypt("Rabbit","U2FsdGVkX18Cjha4VnGC2Kx5ZQ==","123"))

