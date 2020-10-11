# -*- coding: utf-8 -*-
from importlib import import_module
from pathlib import Path
from tools.logger import logger
from .base import BasePlugin, change_config
from .alert import Alert
from .copytrans import CopyTrans
from .ocr import OCR
from .help import Help
# from setuptools import setup, find_packages

plugin_list = [CopyTrans, OCR, Alert, Help]


# packages = find_packages()
# plugin_list = []
# for package in packages:
#     if package.startswith("plugins."):
#         module = import_module(package)
#         plugin_list.append(module.plugin)
#         logger.info("[plugin init] 发现插件包: "+module.__name__)

# 插件包所在的目录
# plugin_path = Path(__file__).parent

# 加载所有的插件包
# plugin_list = []
# for d in plugin_path.iterdir():
#     if d.is_dir() and d.name != "__pycache__":
#         module = import_module("plugins." + d.name)
#         plugin_list.append(module.plugin)
#         logger.info("[plugin init] 发现插件包: "+module.__name__)
