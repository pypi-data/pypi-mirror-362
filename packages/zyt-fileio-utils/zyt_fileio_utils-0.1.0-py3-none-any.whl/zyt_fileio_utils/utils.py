# -*- coding: utf-8 -*-
"""
Project Name: zyt_fileio_utils
File Created: 2025.07.14
Author: ZhangYuetao
File Name: utils.py
Update: 2025.07.16
"""

from copy import deepcopy
from collections.abc import Mapping


def recursive_merge_dicts(default, override):
    """
    递归合并两个字典，保留 default 中的默认值，override 中的值会覆盖 default。
    
    :param default: 默认配置。
    :param override: 用户配置（可能缺省）。
    :return: 合并后的新字典。
    """
    if not isinstance(default, Mapping) or not isinstance(override, Mapping):
        raise TypeError("default 和 override 参数都必须是 Mapping 类型")
    
    result = deepcopy(default)
    for key, override_value in override.items():
        default_value = result.get(key)
        if isinstance(default_value, Mapping) and isinstance(override_value, Mapping):
            result[key] = recursive_merge_dicts(default_value, override_value)
        else:
            result[key] = override_value
    return result
