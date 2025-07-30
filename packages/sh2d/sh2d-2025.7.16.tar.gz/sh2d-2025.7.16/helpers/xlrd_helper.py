# -*- encoding: utf-8 -*-

'''
@File    :   xlrd_helper.py
@Time    :   2025/07/16 12:16:28
@Author  :   test233
@Version :   1.0
'''


import xlrd
from loguru import logger
from datetime import datetime
from typing import Dict, List, Any
from xlrd import xldate_as_tuple


def excel_to_list(excel_path: str) -> Dict[str, List[List[Any]]]:
    """
    将 Excel 文件读取为列表格式
    :param excel_path: Excel 文件路径
    :return: 返回字典，键为工作表名称，值为二维列表，例如：{"Sheet1": [[第一行数据], [第二行数据], ...]}
    """
    result = {}
    try:
        workbook = xlrd.open_workbook(filename=excel_path)
    except Exception as e:
        logger.error(f"Failed to open {excel_path}: {e}")
        return result
    sheets = workbook.sheets()
    if not sheets:
        logger.warning(f"{excel_path} is empty")
        return result
    for sheet in sheets:
        sheet_name = sheet.name
        result[sheet_name] = []
        for row_idx in range(sheet.nrows):
            row_data = []
            for col_idx in range(sheet.ncols):
                cell = sheet.cell(row_idx, col_idx)
                cell_value = _convert_cell_value(cell)
                row_data.append(cell_value)
            result[sheet_name].append(row_data)
    return result


def excel_to_json(excel_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    将 Excel 文件读取为 JSON 格式
    :param excel_path: Excel 文件路径
    :return: 返回字典，键为工作表名称，值为字典列表，例如：{"Sheet1": [{"表头1": 值1, "表头2": 值2}, ...]}
    """
    result = {}
    try:
        workbook = xlrd.open_workbook(filename=excel_path)
    except Exception as e:
        logger.error(f"Failed to open {excel_path}: {e}")
        return result
    sheets = workbook.sheets()
    if not sheets:
        logger.warning(f"{excel_path} is empty")
        return result
    for sheet in sheets:
        sheet_name = sheet.name
        result[sheet_name] = []
        try:
            headers = sheet.row_values(0)  # 第一行为表头
        except Exception as e:
            logger.warning(f"Failed to read headers from {sheet_name}: {e}")
            continue
        for row_idx in range(1, sheet.nrows):  # 从第二行开始读取数据
            row_data = {}
            for col_idx in range(sheet.ncols):
                cell = sheet.cell(row_idx, col_idx)
                cell_value = _convert_cell_value(cell)
                row_data[headers[col_idx]] = cell_value
            result[sheet_name].append(row_data)
    return result


def _convert_cell_value(cell: xlrd.sheet.Cell) -> Any:
    """
    转换 Excel 单元格值为 Python 数据类型
    :param cell: Excel 单元格对象
    :return: 转换后的值
    """
    if cell.ctype == xlrd.XL_CELL_NUMBER and cell.value % 1 == 0:  # 整数
        return int(cell.value)
    elif cell.ctype == xlrd.XL_CELL_DATE:  # 日期
        try:
            date_tuple = xldate_as_tuple(cell.value, 0)
            return datetime(*date_tuple).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.warning(f"Failed to convert date: {e}")
            return cell.value
    elif cell.ctype == xlrd.XL_CELL_BOOLEAN:  # 布尔值
        return bool(cell.value)
    else:  # 其他类型（字符串等）
        return cell.value


if __name__ == "__main__":
    # 测试代码
    excel_file = "example.xlsx"  # 替换为实际 Excel 文件路径
    # 测试 excel_to_list
    print("Testing excel_to_list:")
    list_data = excel_to_list(excel_file)
    for sheet_name, rows in list_data.items():
        print(f"Sheet: {sheet_name}")
        for row in rows:
            print(row)
    # 测试 excel_to_json
    print("\nTesting excel_to_json:")
    json_data = excel_to_json(excel_file)
    for sheet_name, rows in json_data.items():
        print(f"Sheet: {sheet_name}")
        for row in rows:
            print(row)
