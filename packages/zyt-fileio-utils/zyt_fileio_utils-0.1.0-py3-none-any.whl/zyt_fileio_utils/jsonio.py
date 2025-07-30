# -*- coding: utf-8 -*-
"""
Project Name: zyt_fileio_utils
File Created: 2025.07.14
Author: ZhangYuetao
File Name: jsonio.py
Update: 2025.07.16
"""

import json
from pathlib import Path
from copy import deepcopy
from collections.abc import Mapping

import zyt_fileio_utils.utils as utils


def save_dict_to_json(json_path, data_dict):
    """
    将 dict 保存为 JSON 文件。

    :param json_path: 保存路径（str 或 Path）。
    :param data_dict: 要保存的字典。
    """
    if not isinstance(data_dict, Mapping):
        raise TypeError("data_dict 参数必须是 Mapping 类型")
    
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)


def read_dict_from_json(json_path, default={}):
    """
    加载 JSON 文件为 dict，若失败则使用默认配置并递归合并。

    :param json_path: JSON 文件路径（str 或 Path）。
    :param default: 默认配置。
    :return: 合并后的配置字典。
    """
    if not isinstance(default, Mapping):
        raise TypeError("default 参数必须是 Mapping 类型")
    
    json_path = Path(json_path)
    try:
        if json_path.exists():
            with json_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            if not isinstance(loaded, Mapping):
                loaded = {}
            return utils.recursive_merge_dicts(default, loaded)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return deepcopy(default)


def save_json(json_path, data):
    """
    将任意合法 JSON 数据保存到文件。

    :param json_path: 保存路径（str 或 Path）。
    :param data: 任意合法 JSON 类型的数据。
    """
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_json(json_path):
    """
    从 JSON 文件中读取数据（支持任意类型）。

    :param json_path: JSON 文件路径（str 或 Path）。
    :return: JSON 解析后的数据。
    """
    json_path = Path(json_path)
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    