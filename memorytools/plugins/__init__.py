# -*- coding: utf-8 -*-
"""
@file: __init__
@author: Memory
@date: 2020/10/11
@description: plugin的初始化文件，用于创建一个plugin_list
"""
from .base import BasePlugin, change_config
from .alert import Alert
from .copytrans import CopyTrans
from .ocr import OCR
from .help import Help


plugin_list = [CopyTrans, OCR, Alert, Help]


# 以下代码是用于自动寻找插件包的，但是如果使用pyinstaller打包的话，
# 需要将plugins文件夹拷进去才能正常工作，因此暂不使用
# from importlib import import_module
# from tools.logger import logger
# from setuptools import find_packages
# packages = find_packages()
# plugin_list = []
# for package in packages:
#     if package.startswith("plugins."):
#         module = import_module(package)
#         plugin_list.append(module.plugin)
#         logger.info("[plugin init] 发现插件包: "+module.__name__)
