# -*- encoding: utf-8 -*-

'''
@File    :   pywin32_helper.py
@Time    :   2025/07/16 12:14:01
@Author  :   test233
@Version :   1.0
'''


import win32file
import win32com.client
import datetime
from loguru import logger
from typing import Optional


def change_file_time(file_path: str, new_system_time: datetime.datetime) -> None:
    """
    修改文件的创建时间、修改时间和访问时间。

    :param file_path: 文件路径
    :param new_system_time: 新的系统时间（datetime.datetime 类型）
    """
    try:
        # 打开文件并获取文件句柄
        file_handle = win32file.CreateFile(
            file_path, win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0
        )
        # 设置文件的创建时间、修改时间和访问时间
        win32file.SetFileTime(file_handle, new_system_time,
                              new_system_time, new_system_time)
        # 关闭文件句柄
        file_handle.close()
    except Exception as e:
        logger.warning(f"Failed to update file time for {file_path}: {e}")


def encrypt_excel(
    old_filename: str,
    new_filename: str,
    new_passwd: str,
    old_passwd: Optional[str] = ''
) -> None:
    """
    设置或修改 Excel 文件的密码。

    :param old_filename: 原始文件路径
    :param new_filename: 新文件路径
    :param new_passwd: 新密码
    :param old_passwd: 原始密码（可选，默认为空）
    """
    try:
        # 创建 Excel 应用程序对象
        excel_app = win32com.client.Dispatch("Excel.Application")
        # 打开 Excel 文件
        workbook = excel_app.Workbooks.Open(
            old_filename, False, False, None, old_passwd)
        # 禁用 Excel 的警告提示
        excel_app.DisplayAlerts = False
        # 保存文件并设置新密码
        workbook.SaveAs(new_filename, None, new_passwd, '')
        # 退出 Excel 应用程序
        excel_app.Quit()
    except Exception as e:
        logger.warning(f"Failed to encrypt Excel file: {e}")


def say(text: str) -> None:
    """
    将文本转换为语音并播放。

    :param text: 需要播放的文本
    """
    try:
        # 创建语音对象
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        # 播放文本
        speaker.Speak(text)
    except Exception as e:
        logger.warning(f"Failed to speak text: {e}")


if __name__ == "__main__":
    # 测试修改文件时间
    try:
        import datetime
        new_time = datetime.datetime(2023, 10, 1, 12, 0, 0)
        change_file_time("test.txt", new_time)
    except Exception as e:
        print(f"Test failed for change_file_time: {e}")
    # 测试加密 Excel 文件
    try:
        encrypt_excel("old_excel.xlsx", "new_excel.xlsx",
                      "new_password", "old_password")
    except Exception as e:
        print(f"Test failed for encrypt_excel: {e}")
    # 测试文本转语音
    try:
        say("Hello, this is a test message.")
    except Exception as e:
        print(f"Test failed for say: {e}")
