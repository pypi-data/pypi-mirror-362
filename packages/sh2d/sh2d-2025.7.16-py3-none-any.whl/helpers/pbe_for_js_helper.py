# -*- encoding: utf-8 -*-

'''
@File    :   pbe_for_js_helper.py
@Time    :   2025/07/16 12:13:27
@Author  :   test233
@Version :   1.0
'''

import execjs

js_code = '''
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

class PBECryptor:
    """
    PBE 加解密类，使用 js2py 调用 JavaScript 方法实现加密和解密。
    """
    ENCRYPT_TYPES = ["AES", "DES", "Rabbit", "RC4", "TripleDES"]
    def __init__(self):
        # 定义 JavaScript 代码
        self.js_code = js_code
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
            print(f"[{encrypt_type}] 加密结果: {ciphertext}")
            # 解密
            plaintext = cryptor.decrypt(encrypt_type, ciphertext, password)
            print(f"[{encrypt_type}] 解密结果: {plaintext}")
            # 验证解密结果是否与原文一致
            assert plaintext == content, f"解密结果与原文不一致: {plaintext}"
            # print(f"[{encrypt_type}] 测试通过！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[{encrypt_type}] 测试失败: {str(e)}")
        # print("-" * 50)
# 测试代码
if __name__ == "__main__":
    # pip install execjs2
    # npm install crypto-js
    test_all_encrypt_types("Hello, World","123456")
    cryptor = PBECryptor()
    print(cryptor.decrypt("Rabbit","U2FsdGVkX18Cjha4VnGC2Kx5ZQ==","123"))

