# -*- encoding: utf-8 -*-

'''
@File    :   xlwt_helper.py
@Time    :   2025/07/16 12:16:52
@Author  :   test233
@Version :   1.0
'''


import json
import xlsxwriter
from datetime import datetime, date
from typing import Dict, List, Any, Union


def list_to_xlsx(excel_path: str, **tables: Dict[str, List[List[Any]]]) -> None:
    """
    将数据写入 Excel 文件（列表格式）
    :param excel_path: Excel 文件路径
    :param tables: 工作表名称与数据的字典，例如：{'Sheet1': [['A1', 'B1'], ['A2', 'B2']]}
    """
    workbook = xlsxwriter.Workbook(excel_path)
    for sheet_name, rows in tables.items():
        if not rows:
            continue
        worksheet = workbook.add_worksheet(sheet_name)
        for row_index, row_data in enumerate(rows):
            worksheet.write_row(row_index, 0, row_data)
    workbook.close()


def json_list_to_xlsx(excel_path: str, **tables: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    将数据写入 Excel 文件（JSON 格式）
    :param excel_path: Excel 文件路径
    :param tables: 工作表名称与数据的字典，例如：{'Sheet1': [{'A': '1', 'B': '2'}, {'A': '3', 'B': '4'}]}
    """
    # 提取表头
    headers = {}
    for sheet_name, data in tables.items():
        headers[sheet_name] = []
        for item in data:
            for key in item.keys():
                if key not in headers[sheet_name]:
                    headers[sheet_name].append(key)
    # 转换数据为列表格式
    converted_data = {}
    for sheet_name, data in tables.items():
        converted_data[sheet_name] = [headers[sheet_name]]  # 第一行为表头
        for item in data:
            row = [_to_str(item.get(header))
                   for header in headers[sheet_name]]
            converted_data[sheet_name].append(row)
    # 调用 list_to_xlsx 写入 Excel
    list_to_xlsx(excel_path, **converted_data)


def _to_str(value: Any) -> Union[str, int, float, None]:
    """
    将值转换为字符串、数字或 None，支持多种数据类型：
    - None: 原样返回
    - 数字（int, float）: 原样返回
    - 字符串: 原样返回
    - 时间日期（datetime, date）: 原样返回
    - 字典或列表: 使用 json.dumps 转换为字符串（失败时用 str 转换）
    - 其他类型: 使用 str 转换为字符串
    :param value: 输入值
    :return: 转换后的字符串、数字或 None
    """
    if value is None or isinstance(value, (int, float, str, datetime, date)):
        return value  # None、数字、字符串、时间日期格式原样返回
    if isinstance(value, (dict, list)):
        try:
            # 字典或列表用 json.dumps 转换
            return json.dumps(value, ensure_ascii=False)
        except:
            pass
    return str(value)  # 其他类型直接转字符串


if __name__ == "__main__":
    # 测试代码
    excel_file = "output.xlsx"  # 替换为实际 Excel 文件路径
    # 测试 list_to_xlsx
    print("Testing list_to_xlsx...")
    list_data = {
        "Sheet1": [["Name", "Age"], ["Alice", 30], ["Bob", 25]],
        "Sheet2": [["ID", "Score"], [1, 95], [2, 88]],
    }
    list_to_xlsx(excel_file, **list_data)
    print(f"Excel file '{excel_file}' created with list data.")
    # 测试 json_list_to_xlsx
    print("\nTesting json_list_to_xlsx...")
    json_data = {
        "Sheet1": [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}],
        "Sheet2": [{"ID": 1, "Score": 95}, {"ID": 2, "Score": 88}],
    }
    json_list_to_xlsx(excel_file, **json_data)
    print(f"Excel file '{excel_file}' updated with JSON data.")
