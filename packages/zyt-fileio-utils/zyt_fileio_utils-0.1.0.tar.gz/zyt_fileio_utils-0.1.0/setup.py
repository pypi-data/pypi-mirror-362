# -*- coding: utf-8 -*-
"""
Project Name: zyt_fileio_utils
File Created: 2025.07.14
Author: ZhangYuetao
File Name: setup.py
Update: 2025.07.14
"""

from setuptools import setup, find_packages

# 读取 README.md 文件内容作为长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# noinspection PyInterpreter
setup(
    name="zyt_fileio_utils",
    version="0.1.0",
    author="ZhangYuetao",
    author_email="zhang894171707@gmail.com",
    description="A utility package of file io for Python projects",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/VerySeriousMan/zyt_fileio_utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
