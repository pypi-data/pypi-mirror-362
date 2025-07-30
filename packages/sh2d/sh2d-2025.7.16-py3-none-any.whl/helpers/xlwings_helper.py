# -*- encoding: utf-8 -*-

'''
@File    :   xlwings_helper.py
@Time    :   2025/07/16 12:16:38
@Author  :   test233
@Version :   1.0
'''

import xlwings
from typing import List, Dict, Any, Union
def list_to_xlsx(excel_path: str, **tables: Dict[str, List[List[Any]]]) -> None:
    """
    将数据写入 Excel 文件（列表格式）
    :param excel_path: Excel 文件路径
    :param tables: 工作表名称与数据的字典，例如：{'Sheet1': [['A1', 'B1'], ['A2', 'B2']]}
    :return: None
    """
    app = xlwings.App(visible=False, add_book=False)
    try:
        # 创建新工作簿
        workbook = app.books.add()
        for sheet_name, rows in tables.items():
            if not rows:
                continue
            # 检查工作表是否已存在
            if sheet_name in [sheet.name for sheet in workbook.sheets]:
                worksheet = workbook.sheets[sheet_name]  # 使用已存在的工作表
            else:
                worksheet = workbook.sheets.add(sheet_name)  # 添加新工作表
            # 写入数据
            for row_index, row_data in enumerate(rows):
                worksheet.range((row_index + 1, 1)).value = row_data
        # 保存文件
        workbook.save(excel_path)
    except Exception as e:
        raise RuntimeError(f"Failed to write list data to Excel: {e}")
    finally:
        # 关闭工作簿并退出应用程序
        workbook.close()
        app.quit()


def json_list_to_xlsx(excel_path: str, **tables: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    将数据写入 Excel 文件（JSON 格式）
    :param excel_path: Excel 文件路径
    :param tables: 工作表名称与数据的字典，例如：{'Sheet1': [{'A': '1', 'B': '2'}, {'A': '3', 'B': '4'}]}
    :return: None
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
            row = [str(item.get(header, "")) for header in headers[sheet_name]]
            converted_data[sheet_name].append(row)
    # 调用 list_to_xlsx 写入 Excel
    list_to_xlsx(excel_path, **converted_data)

def encrypt_excel(
    source_file: str, 
    target_file: str, 
    password: str
) -> None:
    """
    对 Excel 文件进行加密并保存为新文件
    :param source_file: 源 Excel 文件路径
    :param target_file: 目标 Excel 文件路径（加密后的文件）
    :param password: 加密密码
    :return: None
    """
    # 初始化 Excel 应用程序
    app = xlwings.App(visible=False, add_book=False)
    workbook = None
    try:
        # 打开源文件
        workbook = app.books.open(source_file)
        # 设置密码
        workbook.api.Password = password
        # 保存为目标文件
        workbook.save(target_file)
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt Excel file: {e}")
    finally:
        # 关闭工作簿并退出应用程序
        if workbook:
            workbook.close()
        app.quit()

if __name__ == "__main__":
    # 测试将列表数据写入 Excel 文件
    list_tables = {
        "Sheet1": [
            ["Name", "Age", "City"],
            ["Alice", 30, "New York"],
            ["Bob", 25, "Los Angeles"],
            ["Charlie", 35, "Chicago"]
        ],
        "Sheet2": [
            ["Product", "Price", "Quantity"],
            ["Apple", 1.2, 10],
            ["Banana", 0.8, 15]
        ]
    }
    list_output_path = "list_output.xlsx"
    print(f"Writing list data to '{list_output_path}'...")
    try:
        list_to_xlsx(list_output_path, **list_tables)
        print("List data written successfully!")
    except Exception as e:
        print(f"Error: {e}")
    # 测试将 JSON 数据写入 Excel 文件
    json_tables = {
        "Sheet1": [
            {"Name": "Alice", "Age": 30, "City": "New York"},
            {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
            {"Name": "Charlie", "Age": 35, "City": "Chicago"}
        ],
        "Sheet2": [
            {"Product": "Apple", "Price": 1.2, "Quantity": 10},
            {"Product": "Banana", "Price": 0.8, "Quantity": 15}
        ]
    }
    json_output_path = "json_output.xlsx"
    print(f"Writing JSON data to '{json_output_path}'...")
    try:
        json_list_to_xlsx(json_output_path, **json_tables)
        print("JSON data written successfully!")
    except Exception as e:
        print(f"Error: {e}")

    # 测试代码
    source_file = "example.xlsx"  # 替换为实际源文件路径
    target_file = "encrypted_example.xlsx"  # 替换为实际目标文件路径
    password = "my_password"  # 替换为实际密码
    print(f"Encrypting '{source_file}' and saving as '{target_file}'...")
    try:
        encrypt_excel(source_file, target_file, password)
        print("Encryption completed successfully!")
    except Exception as e:
        print(f"Encryption failed: {e}")