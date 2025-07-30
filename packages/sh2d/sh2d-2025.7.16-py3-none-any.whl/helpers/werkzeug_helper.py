# -*- encoding: utf-8 -*-

'''
@File    :   multipart_form_data_helper.py
@Time    :   2025/07/16 12:12:50
@Author  :   test233
@Version :   1.0
'''

import uuid
from io import BytesIO
from typing import Dict, List, Tuple, Union, Any
from werkzeug.formparser import parse_form_data
from werkzeug.datastructures import MultiDict, FileStorage


def parse_multipart_form_data(request_body: bytes, content_type: str) -> Dict[str, Dict[str, List[Union[str, Dict[str, Union[str, bytes]]]]]]:
    """
    解析 multipart/form-data 格式的请求体，提取普通数据和文件数据。

    :param request_body: 请求体字节流
    :param content_type: 请求的 Content-Type 头部
    :return: 包含普通数据和文件数据的字典，格式为 {'data': dict, 'files': dict}
    """
    # 将请求体转换为文件流
    body_stream: BytesIO = BytesIO(request_body)

    # 构造 WSGI 环境字典
    environ: Dict[str, Any] = {
        'REQUEST_METHOD': 'POST',
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': str(len(request_body)),
        'wsgi.input': body_stream
    }

    # 使用 werkzeug 解析请求体
    stream: Any
    form_data: MultiDict
    file_data: MultiDict
    stream, form_data, file_data = parse_form_data(environ, cls=MultiDict)

    # 提取普通数据，支持同名多值
    parsed_data: Dict[str, List[str]] = {
        key: form_data.getlist(key) for key in form_data.keys()}

    # 提取文件数据，支持同名多值
    parsed_files: Dict[str, List[Dict[str, Union[str, bytes]]]] = {
        key: [
            {
                'filename': file.filename,
                'content_type': file.content_type,
                'content': file.read()
            }
            for file in file_data.getlist(key)
        ]
        for key in file_data.keys()
    }

    return {'data': parsed_data, 'files': parsed_files}


def build_multipart_form_data(form_data: Dict[str, List[str]], file_data: Dict[str, List[Dict[str, Union[str, bytes]]]]) -> Tuple[bytes, str]:
    """
    将普通数据和文件数据重新构造为 multipart/form-data 格式的请求体。

    :param form_data: 普通数据字典，例如 {'username': ['test1', 'test2']}
    :param file_data: 文件数据字典，例如 {'file': [{'filename': 'example.txt', 'content_type': 'text/plain', 'content': b'...'}]}
    :return: 构造后的请求体（字节流）和 Content-Type 头部
    """
    # 生成唯一的 boundary
    boundary: str = f"----{uuid.uuid4().hex}"

    # 初始化字节流
    body_stream: BytesIO = BytesIO()

    # 添加普通数据
    for field_name, values in form_data.items():
        for value in values:
            body_stream.write(f"--{boundary}\r\n".encode('utf-8'))
            body_stream.write(
                f'Content-Disposition: form-data; name="{field_name}"\r\n'.encode('utf-8'))
            body_stream.write(b'\r\n')
            body_stream.write(value.encode('utf-8'))
            body_stream.write(b'\r\n')

    # 添加文件数据
    for field_name, files in file_data.items():
        for file_info in files:
            body_stream.write(f"--{boundary}\r\n".encode('utf-8'))
            body_stream.write(
                f'Content-Disposition: form-data; name="{field_name}"; filename="{file_info["filename"]}"\r\n'.encode('utf-8'))
            body_stream.write(
                f'Content-Type: {file_info["content_type"]}\r\n'.encode('utf-8'))
            body_stream.write(b'\r\n')
            body_stream.write(file_info["content"])
            body_stream.write(b'\r\n')

    # 添加结束 boundary
    body_stream.write(f"--{boundary}--\r\n".encode('utf-8'))

    # 构造 Content-Type 头部
    content_type_header: str = f"multipart/form-data; boundary={boundary}"

    # 返回请求体和 Content-Type
    return body_stream.getvalue(), content_type_header
# 测试用例


def test_parse_and_build_multipart_form_data() -> None:
    # 示例数据
    form_data: Dict[str, List[str]] = {
        'username': ['test1', 'test2']
    }
    file_data: Dict[str, List[Dict[str, Union[str, bytes]]]] = {
        'file': [
            {
                'filename': 'example1.txt',
                'content_type': 'text/plain',
                'content': b'This is the content of file 1.'
            },
            {
                'filename': 'example2.txt',
                'content_type': 'text/plain',
                'content': b'This is the content of file 2.'
            }
        ]
    }

    # 构造 multipart/form-data 请求体
    request_body: bytes
    content_type: str
    request_body, content_type = build_multipart_form_data(
        form_data, file_data)

    # 打印构造的请求体
    print("Constructed Content-Type:", content_type)
    print("Constructed Body:")
    print(request_body.decode('utf-8'))

    # 解析构造的请求体
    parsed_result: Dict[str, Dict[str, List[Union[str, Dict[str, Union[str, bytes]]]]]
                        ] = parse_multipart_form_data(request_body, content_type)

    # 打印解析结果
    print("\nParsed Data:", parsed_result['data'])
    print("Parsed Files:", parsed_result['files'])

    # 验证解析结果是否正确
    assert parsed_result['data'] == form_data, "Parsed data does not match original data"
    assert all(
        parsed_file['filename'] == file['filename'] and
        parsed_file['content_type'] == file['content_type'] and
        parsed_file['content'] == file['content']
        for field_name, files in file_data.items()
        for parsed_file, file in zip(parsed_result['files'][field_name], files)
    ), "Parsed files do not match original files"

    print("\nTest passed!")


# 运行测试用例
if __name__ == "__main__":
    test_parse_and_build_multipart_form_data()
