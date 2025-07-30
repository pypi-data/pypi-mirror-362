# -*- encoding: utf-8 -*-

'''
@File    :   docxtpl_helper.py
@Time    :   2025/07/16 12:08:04
@Author  :   test233
@Version :   1.0
'''


import os
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage


def json_to_docx(template_path: str, output_path: str, context: dict) -> None:
    """
    根据模板和上下文数据生成 Word 文档
    :param template_path: 模板文件路径（例如：template.docx）
    :param output_path: 输出文件路径（例如：output.docx）
    :param context: 上下文数据字典，用于填充模板中的占位符
    :return: None
    """
    # 加载模板文件
    doc = DocxTemplate(template_path)
    # 遍历上下文数据，处理图片路径
    for key, value in context.items():
        if isinstance(value, str) and os.path.isfile(value):
            # 检查文件是否为图片格式
            if value.split('.')[-1].lower() in ['bmp', 'jpg', 'png', 'jpeg', 'gif']:
                # 将图片路径替换为 InlineImage 对象
                context[key] = InlineImage(doc, value, width=Mm(160))
    # 渲染模板并保存生成的文档
    doc.render(context, autoescape=True)
    doc.save(output_path)


if __name__ == '__main__':
    # 示例数据
    template_file = 'template.docx'
    output_file = 'output.docx'
    context_data = {
        'title': '示例文档',
        'content': '这是一个示例文档，用于测试模板渲染功能。',
        'image': 'example.jpg'  # 图片路径
    }
    # 调用函数生成文档
    json_to_docx(template_file, output_file, context_data)
    print(f"文档已生成：{output_file}")
