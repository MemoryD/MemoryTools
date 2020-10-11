# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages
import memorytools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="memorytools",
    version=memorytools.__version__,
    author="Memory",
    author_email="memory_d@foxmail.com",
    description="some useful tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MemoryD/MemoryTools",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "baidu-aip",
        "pyperclip",
        "googletransx",
        "easydict",
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
