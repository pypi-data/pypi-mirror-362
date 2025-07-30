# -*- encoding: utf-8 -*-

'''
@File    :   dingtalk_helper.py
@Time    :   2025/07/16 12:07:52
@Author  :   test233
@Version :   1.0
'''


import time
import hmac
import hashlib
import base64
import urllib.parse
from typing import List, Dict, Tuple
import requests
from loguru import logger


def _generate_signature(secret: str) -> Tuple[str, str]:
    """
    生成钉钉机器人签名和时间戳。

    :param secret: 钉钉群机器人的密钥
    :return: 返回时间戳和签名，格式为 (timestamp, sign)
    """
    timestamp = str(round(time.time() * 1000))  # 获取当前时间戳
    message = f"{timestamp}\n{secret}"  # 构造签名消息
    hmac_code = hmac.new(
        secret.encode("utf-8"), message.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()  # 使用 HMAC-SHA256 生成签名
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # 对签名进行编码
    return timestamp, sign


def send_text(
    text: str,
    webhook: str,
    secret: str = "",
    at_mobiles: List[str] = None,
    is_at_all: bool = False,
) -> bool:
    """
    发送文本消息到钉钉群。

    :param text: 要发送的文本消息
    :param webhook: 钉钉群机器人的 Webhook URL
    :param secret: 钉钉群机器人的密钥，如果未启用签名验证可为空
    :param at_mobiles: 要@的手机号列表，默认为空
    :param is_at_all: 是否@所有人，默认为 False
    :return: 发送成功返回 True，否则返回 False
    """
    if at_mobiles is None:
        at_mobiles = []
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {"content": text},
        "at": {"atMobiles": at_mobiles, "isAtAll": is_at_all},
    }
    # 如果提供了密钥，生成签名并更新 Webhook URL
    if secret:
        timestamp, sign = _generate_signature(secret)
        webhook = f"{webhook}&timestamp={timestamp}&sign={sign}"
    try:
        response = requests.post(webhook, json=data, headers=headers)
        response_json = response.json()
        if response_json.get("errcode") == 0:
            logger.debug(f"消息发送成功: {response_json['errmsg']}")
            return True
        else:
            logger.warning(f"消息发送失败: {response_json['errmsg']}")
            return False
    except Exception as e:
        logger.error(f"消息发送失败: {e}")
        return False


def send_markdown(
    title: str,
    text: str,
    webhook: str,
    secret: str = "",
    at_mobiles: List[str] = None,
    is_at_all: bool = False,
) -> bool:
    """
    发送 Markdown 消息到钉钉群。

    :param title: Markdown 消息的标题
    :param text: Markdown 消息的内容
    :param webhook: 钉钉群机器人的 Webhook URL
    :param secret: 钉钉群机器人的密钥，如果未启用签名验证可为空
    :param at_mobiles: 要@的手机号列表，默认为空
    :param is_at_all: 是否@所有人，默认为 False
    :return: 发送成功返回 True，否则返回 False
    """
    if at_mobiles is None:
        at_mobiles = []
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": text},
        "at": {"atMobiles": at_mobiles, "isAtAll": is_at_all},
    }
    # 如果提供了密钥，生成签名并更新 Webhook URL
    if secret:
        timestamp, sign = _generate_signature(secret)
        webhook = f"{webhook}&timestamp={timestamp}&sign={sign}"
    try:
        response = requests.post(webhook, json=data, headers=headers)
        response_json = response.json()
        if response_json.get("errcode") == 0:
            logger.debug(f"Markdown 消息发送成功: {response_json['errmsg']}")
            return True
        else:
            logger.warning(f"Markdown 消息发送失败: {response_json['errmsg']}")
            return False
    except Exception as e:
        logger.error(f"Markdown 消息发送失败: {e}")
        return False


# 测试代码
if __name__ == "__main__":
    # 测试发送文本消息
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=your_token"
    secret_key = "your_secret"
    send_text("这是一条测试消息", webhook_url, secret_key, ["1234567890"], False)
    # 测试发送 Markdown 消息
    send_markdown(
        "测试标题",
        "### 测试内容\n这是一条 Markdown 消息",
        webhook_url,
        secret_key,
        ["1234567890"],
        False,
    )
