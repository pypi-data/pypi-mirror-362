# -*- coding: utf-8 -*-
"""
Project Name: zyt_fileio_utils
File Created: 2025.07.14
Author: ZhangYuetao
File Name: textio.py
Update: 2025.07.14
"""

import ast
from pathlib import Path


def save_list_to_txt(txt_path, data_list):
    """
    将 list 存入 txt 文件，每个元素占一行。如果文件不存在则新建，存在则追加。

    :param txt_path: 保存的txt路径（str 或 Path）。
    :param data_list: 待保存的数据列表。
    """
    txt_path = Path(txt_path)
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if txt_path.exists() else "w"

    with txt_path.open(mode, encoding="utf-8") as f:
        for item in data_list:
            f.write(str(item) + "\n")


def read_list_from_txt(txt_path, parse=False):
    """
    从 txt 文件读取 list，可选解析数据结构。

    :param txt_path: 读取的txt路径（str 或 Path）。
    :param parse: 是否解析数据结构，默认 False。
    :return: 读取的 list。
    """
    txt_path = Path(txt_path)
    with txt_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        return [ast.literal_eval(line) for line in lines] if parse else lines


def save_text(txt_path, text, mode="w"):
    """
    保存纯文本内容，可指定写入模式（'w' 覆盖，'a' 追加）。

    :param txt_path: 保存路径（str 或 Path）。
    :param text: 字符串内容。
    :param mode: 写入模式，默认覆盖写入 'w'，可选 'a'。
    """
    txt_path = Path(txt_path)
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    with txt_path.open(mode, encoding="utf-8") as f:
        f.write(text)


def read_text(txt_path):
    """
    读取整个文本文件为一个字符串。

    :param txt_path: 文本路径（str 或 Path）。
    :return: 文件内容字符串。
    """
    txt_path = Path(txt_path)
    with txt_path.open("r", encoding="utf-8") as f:
        return f.read()
