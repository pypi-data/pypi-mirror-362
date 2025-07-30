# -*- coding: utf-8 -*-
"""
Project Name: zyt_fileio_utils
File Created: 2025.07.14
Author: ZhangYuetao
File Name: configio.py
Update: 2025.07.16
"""

from pathlib import Path
from copy import deepcopy
from collections.abc import Mapping

import zyt_fileio_utils.utils as utils

# ==== TOML 部分 ====
try:
    import toml
except ImportError:
    toml = None

# ==== YAML 部分 ====
try:
    import yaml
except ImportError:
    yaml = None


def save_dict_to_toml(toml_path, data_dict):
    """
    将 dict 保存为 TOML 文件。

    :param toml_path: 保存路径（str 或 Path）。
    :param data_dict: 要保存的字典。
    """
    if toml is None:
        raise ImportError("请先安装 toml 库：pip install toml")
    if not isinstance(data_dict, Mapping):
        raise TypeError("data_dict 参数必须是 Mapping 类型")

    toml_path = Path(toml_path)
    toml_path.parent.mkdir(parents=True, exist_ok=True)
    with toml_path.open("w", encoding="utf-8") as f:
        toml.dump(data_dict, f)


def read_dict_from_toml(toml_path, default={}):
    """
    加载 TOML 配置文件，如果文件不存在或解析失败则使用默认配置，
    并递归补全缺失的键。

    :param toml_path: TOML 文件路径（str 或 Path）。
    :param default: 默认配置字典。
    :return: 合并后的配置字典。
    """
    if toml is None:
        raise ImportError("请先安装 toml 库：pip install toml")
    if not isinstance(default, Mapping):
        raise TypeError("default 参数必须是 Mapping 类型")

    toml_path = Path(toml_path)
    try:
        if toml_path.exists():
            with toml_path.open("r", encoding="utf-8") as f:
                loaded = toml.load(f)
            if not isinstance(loaded, Mapping):
                loaded = {}
            return utils.recursive_merge_dicts(default, loaded)
    except (FileNotFoundError, toml.TomlDecodeError):
        pass

    return deepcopy(default)


def save_dict_to_yaml(yaml_path, data_dict):
    """
    将 dict 保存为 YAML 文件。

    :param yaml_path: 保存路径（str 或 Path）。
    :param data_dict: 要保存的字典。
    """
    if yaml is None:
        raise ImportError("请先安装 PyYAML 库：pip install pyyaml")
    if not isinstance(data_dict, Mapping):
        raise TypeError("data_dict 参数必须是 Mapping 类型")

    yaml_path = Path(yaml_path)
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.dump(data_dict, f, allow_unicode=True)


def read_dict_from_yaml(yaml_path, default={}):
    """
    加载 YAML 配置文件，如果文件不存在或解析失败则使用默认配置，
    并递归补全缺失的键。

    :param yaml_path: YAML 文件路径（str 或 Path）。
    :param default: 默认配置字典。
    :return: 合并后的配置字典。
    """
    if yaml is None:
        raise ImportError("请先安装 PyYAML 库：pip install pyyaml")
    if not isinstance(default, Mapping):
        raise TypeError("default 参数必须是 Mapping 类型")

    yaml_path = Path(yaml_path)
    try:
        if yaml_path.exists():
            with yaml_path.open("r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
            if not isinstance(loaded, Mapping):
                loaded = {}
            return utils.recursive_merge_dicts(default, loaded)
    except (FileNotFoundError, yaml.YAMLError):
        pass

    return deepcopy(default)
