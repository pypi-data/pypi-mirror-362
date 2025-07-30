# -*- encoding: utf-8 -*-

'''
@File    :   hashlib_helper.py
@Time    :   2025/07/16 12:08:21
@Author  :   test233
@Version :   1.0
'''


import hashlib

class HashCalculator:
    """哈希计算器"""
    
    # 支持的哈希算法
    ALGORITHMS = {
        "MD5 (128位)": hashlib.md5,
        "SHA1 (160位)": hashlib.sha1,
        "SHA224 (224位)": hashlib.sha224,
        "SHA256 (256位)": hashlib.sha256,
        "SHA384 (384位)": hashlib.sha384,
        "SHA512 (512位)": hashlib.sha512,
        "SHA3-224 (224位)": hashlib.sha3_224,
        "SHA3-256 (256位)": hashlib.sha3_256,
        "SHA3-384 (384位)": hashlib.sha3_384,
        "SHA3-512 (512位)": hashlib.sha3_512,
        "BLAKE2s (256位)": hashlib.blake2s,
        "BLAKE2b (512位)": hashlib.blake2b,
        "SHAKE128 (128位)": hashlib.shake_128,
        "SHAKE256 (256位)": hashlib.shake_256,
        # "RIPEMD160 (160位)": lambda: hashlib.new('ripemd160'),
        # "Whirlpool (512位)": lambda: hashlib.new('whirlpool'),
    }
    
    @staticmethod
    def hash(text: bytes, algorithm: str, length: int = None) -> str:
        """计算哈希值"""
        try:
            if algorithm not in HashCalculator.ALGORITHMS:
                raise ValueError(f"不支持的哈希算法: {algorithm}")
                
            hash_func = HashCalculator.ALGORITHMS[algorithm]
            
            # 处理特殊的哈希算法
            if algorithm in ["SHAKE128 (128位)", "SHAKE256 (256位)"]:
                if not length:
                    length = 128 if "128" in algorithm else 256
                h = hash_func()
                h.update(text)
                return h.hexdigest(length // 8)  # 转换为字节长度
            else:
                h = hash_func()
                h.update(text)
                return h.hexdigest()
                
        except Exception as e:
            raise ValueError(f"哈希计算错误: {str(e)}")



def test_hash_calculator():
    """测试哈希计算器"""
    text = b"Hello, World!"
    
    for name, func in HashCalculator.ALGORITHMS.items():
        if isinstance(func, str):  # 特殊处理 RIPEMD160 和 Whirlpool
            print(f"{name}: {HashCalculator.hash(text, func)}")
        else:
            print(f"{name}: {HashCalculator.hash(text, name)}")

# 测试代码
if __name__ == "__main__":
    test_hash_calculator()
