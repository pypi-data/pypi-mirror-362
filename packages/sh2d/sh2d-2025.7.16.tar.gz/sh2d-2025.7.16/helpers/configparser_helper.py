# -*- encoding: utf-8 -*-

'''
@File    :   configparser_helper.py
@Time    :   2025/07/16 12:07:17
@Author  :   test233
@Version :   1.0
'''


import configparser
from typing import Dict


def config_to_json(file_path: str, encoding: str = 'utf8') -> Dict[str, Dict[str, str]]:
    """
    将配置文件读取为 JSON 格式的字典
    :param file_path: 配置文件路径，例如：config.ini/config.conf/config.cfg
    :param encoding: 文件编码方式，默认为 'utf8'
    :return: 返回字典格式的配置数据，例如：{"section_name": {"key": "value"}}
    """
    config_dict: Dict[str, Dict[str, str]] = {}
    config = configparser.RawConfigParser()
    config.read(file_path, encoding=encoding)

    # 遍历所有配置项
    for section in config.sections():
        config_dict[section] = dict(config.items(section))

    return config_dict


def json_to_config(file_path: str, config_dict: Dict[str, Dict[str, str]], encoding: str = 'utf8') -> None:
    """
    将 JSON 格式的字典写入配置文件
    :param file_path: 配置文件路径，例如：config.ini/config.conf/config.cfg
    :param config_dict: JSON 格式的字典，例如：{"section_name": {"key": "value"}}
    :param encoding: 文件编码方式，默认为 'utf8'
    """
    config = configparser.RawConfigParser()

    # 遍历字典并写入配置
    for section, key_value_pairs in config_dict.items():
        config.add_section(section)
        for key, value in key_value_pairs.items():
            config.set(section, key, value)

    # 写入文件
    with open(file_path, 'w', encoding=encoding) as config_file:
        config.write(config_file)


# 测试代码
if __name__ == '__main__':
    # 测试 config_to_json
    config_path = 'config.ini'
    json_config = config_to_json(config_path)
    print(f"Config as JSON: {json_config}")

    # 测试 json_to_config
    new_config_path = 'new_config.ini'
    sample_config = {
        "Section1": {"key1": "value1", "key2": "value2"},
        "Section2": {"key3": "value3"}
    }
    json_to_config(new_config_path, sample_config)
    print(f"Config written to: {new_config_path}")
