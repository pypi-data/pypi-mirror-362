#!/usr/bin/env python

"""
Author: Bitliker
Date: 2025-03-19 09:03:04
Version: 1.0
Description: 打包当前的 python 项目

"""

from setuptools import setup, find_packages


setup(
    name="Bitliker-libs",  # 包名
    version="1.2.2",  # 版本号
    packages=find_packages(),  # 包含的包
    description="Bitliker 个人集合工具类",  # 包的描述
    long_description=open("README.md", encoding="utf-8").read(),  # 包的详细描述
    long_description_content_type="text/markdown",  # 包的详细类型
    author="Bitliker",  # 作者
    author_email="gongpengming@163.com",
    url="https://github.com/BitlikerPython/Libs",
    install_requires=["requests", "colorama","music_tag"],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="Bitliker Tools",
    python_requires=">=3.10",
)
