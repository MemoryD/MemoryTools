from importlib import import_module
from pathlib import Path
from tools.logger import logger
from .base import BasePlugin, change_config

# 插件包所在的目录
plugin_path = Path(__file__).parent

# 加载所有的插件包
plugin_list = []
for d in plugin_path.iterdir():
    if d.is_dir() and d.name != "__pycache__":
        module = import_module("plugins." + d.name)
        plugin_list.append(module.plugin)
        logger.info("[plugin init] 发现插件包: "+module.__name__)
