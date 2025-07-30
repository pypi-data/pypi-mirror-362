# -*- encoding: utf-8 -*-

'''
@File    :   re_helper.py
@Time    :   2025/07/16 12:14:59
@Author  :   test233
@Version :   1.0
'''

import re
from typing import List, Optional, Dict, Union


class TextHandler:
    """
    文本处理类，用于处理文本中的正则表达式匹配、替换、验证等操作。
    """
    # 正则表达式映射，用于匹配常见的数据格式
    REGEX_MAP_A: Dict[str, str] = {
        "ipv4": r'((?<!\d)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?!\d))',
        "port": r'((?<!\d)(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d))',
        "ipv4_port": r'((?:(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])(?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))',
        "ipv6": r'((?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?::[0-9A-Fa-f]{1,4}){1,2})|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?::[0-9A-Fa-f]{1,4}){1,6})|(?::(?::[0-9A-Fa-f]{1,4}){1,7})))',
        "ipv6_port": r'(\[(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){6}:[0-9A-Fa-f]{1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?::[0-9A-Fa-f]{1,4}){1,2})|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?::[0-9A-Fa-f]{1,4}){1,6})|(?::(?::[0-9A-Fa-f]{1,4}){1,7}))\](?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))',
        "domain": r'((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})',
        "domain_port": r'((?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{0,3}|[0-9])(?!\d)))',
        "url": r'(https?://[-\w]+(?:\.[\w-]+)+(?::\d+)?(?:/[^.!,?\"<>\[\]{}\s\x7F-\xFF]*(?:[.!,?]+[^.!,?\"<>\[\]\{\}\s\x7F-\xFF]+)*)?)',
        "icp": r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]ICP[备证]\d+号(?:-\d+)?)',
        "id_card": r'((?<!\d)[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10, 11, 12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx](?!\dXx))',
        "bank_card": r'((?<!\d)[1-9]\d{9,29}(?!\d))',
        "credit_code": r'((?<![0-9A-HJ-NPQRTUWXY])[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}(?![0-9A-HJ-NPQRTUWXY]))',
        "email": r'((?:(?:[^<>()[\]\\.,;:\s@\"`]+(?:\.[^<>()[\]\\.,;:\s@\"`]+)*)|(?:\".+\"))@(?:(?:\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(?:(?:[a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,})))',
    }
    # 正则表达式映射，用于替换或删除特定字符
    REGEX_MAP_B: Dict[str, str] = {
        "html": r'(<[^>]+>)',
        "filename": r'([\/\\\:\*\?\"\<\>\|])',
    }

    @staticmethod
    def replace(text: str, regex: str, replacement: str = '') -> str:
        """
        使用正则表达式替换文本中的匹配项。
        :param text: 待处理的文本
        :param regex: 正则表达式或映射中的键
        :param replacement: 替换的字符串，默认为空
        :return: 替换后的文本
        """
        pattern = TextHandler.REGEX_MAP_B.get(regex, regex)
        return re.sub(pattern, replacement, text)

    @staticmethod
    def extract(text: str, regex: Optional[str] = None) -> Union[List[str], Dict[str, List[str]]]:
        """
        使用正则表达式提取文本中的匹配项。
        :param text: 待处理的文本
        :param regex: 正则表达式或映射中的键，为空时返回所有类型的匹配结果
        :return: 如果 regex 不为空，返回匹配项列表；否则返回一个字典，包含所有类型的匹配结果
        """
        if regex is None:
            # 返回所有类型的匹配结果
            return {
                regex_type: re.findall(pattern, text)
                for regex_type, pattern in TextHandler.REGEX_MAP_A.items()
            }
        else:
            # 返回指定类型的匹配结果
            pattern = TextHandler.REGEX_MAP_A.get(regex, regex)
            return re.findall(pattern, text)

    @staticmethod
    def validate(text: str, regex: str) -> bool:
        """
        使用正则表达式验证文本是否完全匹配。
        :param text: 待验证的文本
        :param regex: 正则表达式或映射中的键
        :return: 是否完全匹配
        """
        pattern = TextHandler.REGEX_MAP_A.get(regex, regex)
        return bool(re.fullmatch(pattern, text))

    @staticmethod
    def identify(text: str) -> Optional[str]:
        """
        识别文本的类型。
        :param text: 待识别的文本
        :return: 文本类型，如果无法识别则返回 None
        """
        for _type, pattern in TextHandler.REGEX_MAP_A.items():
            if re.fullmatch(pattern, text):
                return _type
        return None

    @staticmethod
    def validate_id_card(id_card: str) -> bool:
        """
        验证身份证号码是否合法。
        :param id_card: 身份证号码
        :return: 是否合法
        """
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        total = sum(int(id_card[i]) * weights[i] for i in range(17))
        return id_card[-1].upper() == check_codes[total % 11]

    @staticmethod
    def validate_luhn(bank_card: str) -> bool:
        """
        验证银行卡号是否合法（使用 Luhn 算法）。
        :param bank_card: 银行卡号
        :return: 是否合法
        """
        total = 0
        for i, char in enumerate(reversed(bank_card)):
            num = int(char)
            if i % 2 == 1:
                num *= 2
                if num > 9:
                    num = num - 9
            total += num
        return total % 10 == 0

    @staticmethod
    def validate_credit_code(credit_code: str) -> bool:
        """
        验证统一社会信用代码是否合法。
        :param credit_code: 统一社会信用代码
        :return: 是否合法
        """
        weights = [1, 3, 9, 27, 19, 26, 16, 17,
                   20, 29, 25, 13, 8, 24, 10, 30, 28]
        chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
        total = sum(chars.index(credit_code[i])
                    * weights[i] for i in range(17))
        return credit_code[-1] == chars[(31 - total % 31) % 31]


# 测试代码
if __name__ == "__main__":
    # 测试替换功能
    test_html = "<p>This is <b>bold</b> text.</p>"
    cleaned_html = TextHandler.replace(test_html, "html", "")
    print(f"Cleaned HTML: {cleaned_html}")  # 输出: "This is bold text."
    test_filename = "file/name*with?illegal|characters.txt"
    cleaned_filename = TextHandler.replace(test_filename, "filename", "_")
    # 输出: "file_name_with_illegal_characters.txt"
    print(f"Cleaned Filename: {cleaned_filename}")
    # 测试提取功能
    test_text = "My IP is 192.168.1.1 and port is 8080."
    extracted_ips = TextHandler.extract(test_text, "ipv4")
    print(f"Extracted IPs: {extracted_ips}")  # 输出: ['192.168.1.1']
    test_url = "Visit https://example.com/path for more info."
    extracted_urls = TextHandler.extract(test_url, "url")
    # 输出: ['https://example.com/path']
    print(f"Extracted URLs: {extracted_urls}")
    test_url = "Visit https://example.com/path for more info."
    extracted_all = TextHandler.extract(test_url)
    print(f"Extracted all: {extracted_all}")
    # 测试验证功能
    test_id_card = "11010519491231002X"
    is_valid_id = TextHandler.validate_id_card(test_id_card)
    print(f"Is Valid ID Card: {is_valid_id}")  # 输出: True
    test_bank_card = "6228480402564890018"
    is_valid_bank_card = TextHandler.validate_luhn(test_bank_card)
    print(f"Is Valid Bank Card: {is_valid_bank_card}")  # 输出: True
    test_credit_code = "91350100M000100Y43"
    is_valid_credit_code = TextHandler.validate_credit_code(test_credit_code)
    print(f"Is Valid Credit Code: {is_valid_credit_code}")  # 输出: True
    # 测试识别功能
    test_domain = "www.example.com"
    identified_type = TextHandler.identify(test_domain)
    print(f"Identified Type: {identified_type}")  # 输出: "domain"
    test_email = "user@example.com"
    identified_type = TextHandler.identify(test_email)
    print(f"Identified Type: {identified_type}")  # 输出: "email"
