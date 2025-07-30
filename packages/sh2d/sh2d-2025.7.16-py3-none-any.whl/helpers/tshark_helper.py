# -*- encoding: utf-8 -*-

'''
@File    :   tshark_helper.py
@Time    :   2025/07/16 12:16:23
@Author  :   test233
@Version :   1.0
'''


import os
import json
import gzip
import hashlib
import subprocess
import contextlib
from urllib import parse
from loguru import logger
from dataclasses import dataclass
from typing import Dict, Iterable, NamedTuple, Optional, Tuple, List


@dataclass
class Request:
    """HTTP 请求数据类"""
    frame_number: int
    frame_time_epoch: float
    frame_len: int
    method: str
    full_uri: str
    header: bytes
    body: bytes


@dataclass
class Response:
    """HTTP 响应数据类"""
    frame_number: int
    frame_time_epoch: float
    frame_len: int
    full_uri: str
    code: int
    header: bytes
    body: bytes
    _request_in: Optional[int]


class HttpPair(NamedTuple):
    """HTTP 请求和响应对"""
    request: Optional[Request]
    response: Optional[Response]


DEFAULT_HTTP_FIELDS = [
    "frame.number",
    "frame.time_epoch",
    "frame.len",
    # "http.request_number",
    "http.request_in",
    "http.request.full_uri",
    "http.request.method",
    # "http.response_number",
    "http.response.code",
    # "http.response_for.uri",
    "tcp.payload",
    "tcp.reassembled.data",
    "exported_pdu.exported_pdu",
]


class FlowAnalyzer:
    """流量分析器，用于解析和处理 tshark 导出的 JSON 数据文件"""

    def __init__(self, json_path: str):
        """
        初始化 FlowAnalyzer 对象
        :param json_path: tshark 导出的 JSON 文件路径
        """
        self.json_path = json_path
        self._check_json_file()

    def _check_json_file(self) -> None:
        """
        检查 JSON 文件是否存在并非空
        :raises FileNotFoundError: 当 JSON 文件不存在时抛出
        :raises ValueError: 当 JSON 文件内容为空时抛出
        """
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"JSON 文件未找到！路径：{self.json_path}")
        if os.path.getsize(self.json_path) == 0:
            raise ValueError(f"JSON 文件内容为空！路径：{self.json_path}")

    def parse_json(self, fields: List[str] = DEFAULT_HTTP_FIELDS) -> Iterable[Dict[str, str]]:
        """
        解析 JSON 数据文件中的指定字段
        :param fields: 要提取的字段列表
        :return: 包含字段数据的字典生成器
        """
        with open(self.json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for packet in data:
            if not packet.get("_source"):
                continue
            packet = packet["_source"]["layers"]
            yield {
                field: packet[field][0] if isinstance(
                    packet[field], list) else packet[field]
                for field in fields
                if packet.get(field)
            }

    def parse_http_json(self, fields: List[str] = DEFAULT_HTTP_FIELDS) -> Iterable[HttpPair]:
        """
        解析 JSON 数据文件中的 HTTP 请求和响应信息
        :param fields: 要提取的字段列表
        :return: 包含 HTTP 请求和响应对的生成器
        """
        requests, responses = {}, {}
        for packet in self.parse_json(fields):
            packet = {k: v[0] if isinstance(
                v, list) else v for k, v in packet.items()}
            frame_number = int(packet["frame.number"])
            frame_time_epoch = float(packet["frame.time_epoch"])
            frame_len = int(packet["frame.len"]) if packet.get(
                "frame.len") else None
            http_request_in = int(packet["http.request_in"]) if packet.get(
                "http.request_in") else frame_number
            http_request_full_uri = parse.unquote(
                packet["http.request.full_uri"]) if packet.get("http.request.full_uri") else ""
            full_request = packet.get("tcp.reassembled.data") or packet.get(
                "tcp.payload") or packet.get("exported_pdu.exported_pdu")
            http_response_for_uri = parse.unquote(
                packet["http.response_for.uri"]) if packet.get("http.response_for.uri") else None
            http_request_method = packet["http.request.method"] if packet.get(
                "http.request.method") else None
            http_response_code = int(packet["http.response.code"]) if packet.get(
                "http.response.code") else None
            header, body = self._extract_http_body(full_request)
            if packet.get("http.response.code"):
                responses[frame_number] = Response(
                    frame_number=frame_number,
                    frame_time_epoch=frame_time_epoch,
                    frame_len=frame_len,
                    _request_in=http_request_in,
                    full_uri=http_response_for_uri,
                    code=http_response_code,
                    header=header,
                    body=body,
                )
            else:
                requests[frame_number] = Request(
                    frame_number=frame_number,
                    frame_time_epoch=frame_time_epoch,
                    frame_len=frame_len,
                    full_uri=http_request_full_uri,
                    method=http_request_method,
                    header=header,
                    body=body,
                )
        response_map = {r._request_in: r for r in responses.values()}
        yielded_resps = []
        for req_id, req in requests.items():
            resp = response_map.get(req_id)
            if resp:
                yielded_resps.append(resp)
                resp._request_in = None
                yield HttpPair(request=req, response=resp)
            else:
                yield HttpPair(request=req, response=None)
        for resp in response_map.values():
            if resp not in yielded_resps:
                resp._request_in = None
                yield HttpPair(request=None, response=resp)

    @staticmethod
    def _get_hash(file_path: str, display_filter: str) -> str:
        """
        计算文件的 MD5 哈希值
        :param file_path: 文件路径
        :param display_filter: tshark 过滤语句
        :return: MD5 哈希值
        """
        with open(file_path, "rb") as file:
            return hashlib.md5(file.read() + display_filter.encode()).hexdigest()

    @staticmethod
    def _extract_json_file(file_name: str, display_filter: str, fields: List[str], tshark_work_dir: str, json_work_path: str) -> None:
        """
        执行 tshark 提取 JSON 文件
        :param file_name: 流量文件名
        :param display_filter: tshark 过滤语句
        :param fields: 要提取的字段列表
        :param tshark_work_dir: tshark 运行目录
        :param json_work_path: JSON 文件保存路径
        """
        command = ["tshark", "-r", file_name, "-Y",
                   f"({display_filter})", "-T", "json", "-x"]
        for field in fields:
            command += ["-e", field]
        logger.debug(f"导出 JSON 命令: {' '.join(command)}")
        with open(json_work_path, "wb") as output_file:
            process = subprocess.Popen(
                command, stdout=output_file, stderr=subprocess.PIPE, cwd=tshark_work_dir)
            _, stderr = process.communicate()
        logger.debug(f"导出 JSON 文件路径: {json_work_path}")
        if stderr and b"WARNING" not in stderr:
            try:
                print(f"[Warning/Error]: {stderr.decode('utf-8')}")
            except Exception:
                print(f"[Warning/Error]: {stderr.decode('gbk')}")

    @staticmethod
    def _add_md5sum(json_work_path: str, md5_sum: str) -> None:
        """
        向 JSON 文件中添加 MD5 校验值
        :param json_work_path: JSON 文件路径
        :param md5_sum: MD5 校验值
        """
        with open(json_work_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not data:
            data.append({})
        data[0]["MD5Sum"] = md5_sum
        with open(json_work_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def get_json_data(file_path: str, display_filter: str, fields: List[str] = DEFAULT_HTTP_FIELDS,json_work_path: str = os.path.join(os.getcwd(), "output.json")) -> str:
        """
        获取 JSON 数据并保存至文件
        :param file_path: 流量文件路径
        :param display_filter: tshark 过滤语句
        :param fields: 要提取的字段列表
        :return: JSON 文件路径
        :raises FileNotFoundError: 当流量文件不存在时抛出
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"流量文件未找到！路径：{file_path}")
        md5_sum = FlowAnalyzer._get_hash(file_path, display_filter)
        logger.debug(f"MD5 校验值: {md5_sum}")
        # work_dir = os.getcwd()
        tshark_work_dir = os.path.dirname(os.path.abspath(file_path))
        # json_work_path = os.path.join(work_dir, "output.json")
        file_name = os.path.basename(file_path)
        if os.path.exists(json_work_path):
            try:
                with open(json_work_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if data[0].get("MD5Sum") == md5_sum:
                        logger.debug("MD5 校验匹配，直接返回 JSON 文件路径！")
                        return json_work_path
            except Exception:
                logger.debug("默认 JSON 文件无法解析，正在重新生成...")
        FlowAnalyzer._extract_json_file(
            file_name, display_filter, fields, tshark_work_dir, json_work_path)
        FlowAnalyzer._add_md5sum(json_work_path, md5_sum)
        return json_work_path

    @staticmethod
    def _split_http_headers(body: bytes) -> Tuple[bytes, bytes]:
        """
        分割 HTTP 头部和主体
        :param body: HTTP 原始字节流
        :return: 头部和主体的元组
        """
        header_end = body.find(b"\r\n\r\n")
        if header_end != -1:
            header_end += 4
            return body[:header_end], body[header_end:]
        elif body.find(b"\n\n") != -1:
            header_end = body.index(b"\n\n") + 2
            return body[:header_end], body[header_end:]
        else:
            logger.warning("未找到 HTTP 头部和主体的分割位置！")
            return b"", body

    @staticmethod
    def _dechunk_http_response(body: bytes) -> bytes:
        """
        解码分块 HTTP 响应
        :param body: HTTP 主体字节流
        :return: 解码后的字节流
        """
        chunks = []
        chunk_size_end = body.find(b"\n") + 1
        line_endings = b"\r\n" if bytes(
            [body[chunk_size_end - 2]]) == b"\r" else b"\n"
        line_endings_length = len(line_endings)
        while True:
            chunk_size = int(body[:chunk_size_end], 16)
            if not chunk_size:
                break
            chunks.append(body[chunk_size_end: chunk_size + chunk_size_end])
            body = body[chunk_size_end + chunk_size + line_endings_length:]
            chunk_size_end = body.find(line_endings) + line_endings_length
        return b"".join(chunks)

    def decode_chunked_data(self,chunked_data):
        data = b""
        while True:
            chunk_size_end = chunked_data.find(b"\r\n")
            if chunk_size_end == -1:
                break
            
            chunk_size_hex = chunked_data[:chunk_size_end].decode("ascii")
            chunk_size = int(chunk_size_hex.split(";")[0], 16)
            
            if chunk_size == 0:
                break
            
            chunk_start = chunk_size_end + 2
            chunk_end = chunk_start + chunk_size
            chunk = chunked_data[chunk_start:chunk_end]
            data += chunk
            
            chunked_data = chunked_data[chunk_end + 2:]
        
        return data
    def _extract_http_body(self, full_request: str) -> Tuple[bytes, bytes]:
        """
        提取 HTTP 请求或响应的头部和主体
        :param full_request: HTTP 原始字节流
        :return: 头部和主体的元组
        """
        header, body = self._split_http_headers(bytes.fromhex(full_request))
        if b'Transfer-Encoding: chunked' in header:
            body = self.decode_chunked_data(body)

        with contextlib.suppress(Exception):
            body = self._dechunk_http_response(body)

        with contextlib.suppress(Exception):
            if body.startswith(b"\x1f\x8b"):
                body = gzip.decompress(body)
        return header, body


if __name__ == "__main__":
    pass
    # 测试代码
    # file_path = "example.pcap"  # 替换为实际流量文件路径
    # display_filter = "http"  # 替换为实际过滤条件
    # json_path = FlowAnalyzer.get_json_data(file_path, display_filter)
    # for request, response in FlowAnalyzer(json_path).parse_http_json():
    #     if request:
    #         print(f"Request: {request}")
    #     if response:
    #         print(f"Response: {response}")
    # file = ""
    # # 非http
    # display_filter = "ftp"
    # fields = ["frame.number", "ftp.current-working-directory", "tcp.payload"]
    # json_path = FlowAnalyzer.get_json_data(
    #     file, display_filter=display_filter, fields=fields
    # )
    # for item in FlowAnalyzer(json_path).parse_json(fields):
    #     # item is dict
    #     print(f"item: {item}")
