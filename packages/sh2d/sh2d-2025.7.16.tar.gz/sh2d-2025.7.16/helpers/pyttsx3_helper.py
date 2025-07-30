# -*- encoding: utf-8 -*-

'''
@File    :   pyttsx3_helper.py
@Time    :   2025/07/16 12:13:56
@Author  :   test233
@Version :   1.0
'''


import pyttsx3
from typing import Optional


class TextToSpeech:
    """
    文本转语音工具类，使用 pyttsx3 实现。
    """

    def __init__(self):
        """
        初始化语音引擎。
        """
        self.engine = pyttsx3.init()

    def say(self, text: str) -> None:
        """
        将文本转换为语音并播放。
        Args:
            text (str): 要转换为语音的文本。
        """
        if not text:
            raise ValueError("文本内容不能为空")
        self.engine.say(text)
        self.engine.runAndWait()

    def set_voice(self, voice_id: Optional[str] = None) -> None:
        """
        设置语音引擎的声音。
        Args:
            voice_id (Optional[str]): 声音 ID，如果为 None，则使用默认声音。
        """
        voices = self.engine.getProperty('voices')
        if voice_id is None:
            self.engine.setProperty('voice', voices[0].id)  # 默认使用第一个声音
        else:
            self.engine.setProperty('voice', voice_id)

    def set_rate(self, rate: int = 200) -> None:
        """
        设置语音引擎的语速。
        Args:
            rate (int): 语速，默认值为 200。
        """
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float = 1.0) -> None:
        """
        设置语音引擎的音量。
        Args:
            volume (float): 音量，范围为 0.0 到 1.0，默认值为 1.0。
        """
        if volume < 0.0 or volume > 1.0:
            raise ValueError("音量必须在 0.0 到 1.0 之间")
        self.engine.setProperty('volume', volume)


if __name__ == "__main__":
    # 测试代码
    tts = TextToSpeech()
    # 设置语音属性
    tts.set_rate(150)  # 设置语速
    tts.set_volume(0.8)  # 设置音量
    # 测试文本转语音
    print("Testing TextToSpeech...")
    test_text = "你好，这是一个文本转语音的测试。"
    tts.say(test_text)
    print(f"已播放文本：{test_text}")
