# -*- encoding: utf-8 -*-

'''
@File    :   zmail_helper.py
@Time    :   2025/07/16 12:17:08
@Author  :   test233
@Version :   1.0
'''


import zmail
from loguru import logger
from typing import List, Optional

def send_mail(
    title: str = "",
    content: str = "",
    attachments: Optional[List[str]] = None,
    username: str = "",
    password: str = "",
    to_user: Optional[List[str]] = None,
    cc: Optional[List[str]] = None,
    is_html: bool = False
) -> bool:
    """
    发送邮件。
    Args:
        title (str): 邮件标题。
        content (str): 邮件内容，可以是纯文本或 HTML。
        attachments (Optional[List[str]]): 附件文件路径列表，默认为空。
        username (str): 发件人邮箱账号。
        password (str): 发件人邮箱密码或授权码。
        to_user (Optional[List[str]]): 收件人邮箱地址列表，默认为空。
        cc (Optional[List[str]]): 抄送人邮箱地址列表，默认为空。
        is_html (bool): 邮件内容是否为 HTML 格式，默认为 False。
    Returns:
        bool: 邮件发送成功返回 True，失败返回 False。
    """
    # 初始化邮件服务器
    server = zmail.server(username, password)
    
    # 构建邮件内容
    mail = {
        'subject': title,
        'attachments': attachments or [],
    }
    if is_html:
        mail['content_html'] = content
    else:
        mail['content_text'] = content
    
    # 发送邮件
    try:
        server.send_mail(to_user or [], mail, cc=cc or [])
        logger.debug(f"邮件发送成功：从 {username} 发送至 {to_user}，抄送 {cc}")
        return True
    except Exception as e:
        logger.error(f"邮件发送失败：从 {username} 发送至 {to_user}，抄送 {cc}", exc_info=True)
        return False
if __name__ == "__main__":
    # 测试代码

    
    # 测试发送邮件
    print("Testing send_mail...")
    result = send_mail(
        title="测试邮件",
        content="这是一封测试邮件。",
        attachments=["test.txt"],  # 替换为实际文件路径
        username="your_email@example.com",  # 替换为实际邮箱账号
        password="your_password",  # 替换为实际密码或授权码
        to_user=["recipient1@example.com", "recipient2@example.com"],  # 替换为实际收件人
        cc=["cc@example.com"],  # 替换为实际抄送人
        is_html=False
    )
    if result:
        print("邮件发送成功！")
    else:
        print("邮件发送失败！")
