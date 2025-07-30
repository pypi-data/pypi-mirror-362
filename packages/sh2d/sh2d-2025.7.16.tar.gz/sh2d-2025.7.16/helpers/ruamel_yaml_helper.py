# -*- encoding: utf-8 -*-

'''
@File    :   ruamel_yaml_helper.py
@Time    :   2025/07/16 12:15:18
@Author  :   test233
@Version :   1.0
'''


from ruamel.yaml import YAML
from typing import Any, Dict, Optional


def write_json_to_yaml(file_path: str, data: Dict[str, Any], encoding: str = 'utf8') -> None:
    """
    将 JSON 格式的数据写入 YAML 文件，并确保列表元素缩进为 4 个字符。
    Args:
        file_path (str): YAML 文件路径。
        data (Dict[str, Any]): 要写入的 JSON 数据。
        encoding (str, optional): 文件编码，默认为 'utf8'。
    """
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)  # 设置映射和序列的缩进
    with open(file_path, 'w', encoding=encoding) as file:
        yaml.dump(data, file)


def read_yaml_to_json(file_path: str, encoding: str = 'utf8') -> Optional[Dict[str, Any]]:
    """
    从 YAML 文件中读取数据并解析为 JSON 格式。
    Args:
        file_path (str): YAML 文件路径。
        encoding (str, optional): 文件编码，默认为 'utf8'。
    Returns:
        Optional[Dict[str, Any]]: 解析后的 JSON 数据，如果文件读取失败则返回 None。
    """
    try:
        yaml = YAML()
        with open(file_path, 'r', encoding=encoding) as file:
            return yaml.load(file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None


if __name__ == "__main__":
    # 测试代码
    yaml_file_path = "test.yaml"  # 替换为实际 YAML 文件路径
    # 测试 write_json_to_yaml
    print("Testing write_json_to_yaml...")
    test_data = {
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "Java", "SQL"],
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    }
    write_json_to_yaml(yaml_file_path, test_data)
    print(f"YAML file '{yaml_file_path}' created with test data.")
    # 测试 read_yaml_to_json
    print("\nTesting read_yaml_to_json...")
    loaded_data = read_yaml_to_json(yaml_file_path)
    if loaded_data:
        print("Loaded data from YAML file:")
        print(loaded_data)
