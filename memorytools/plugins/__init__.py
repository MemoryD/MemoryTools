from importlib import import_module
from pathlib import Path
from .base import BasePlugin, change_config

plugin_path = Path() / "plugins"

plugin_list = []
for d in plugin_path.iterdir():
    if d.is_dir() and d.name != "__pycache__":
        plugin = import_module("plugins." + d.name).plugin
        plugin_list.append(plugin)
        print(plugin.__module__)

# print(plugin_list)
# all_plugins = [p.plugin for p in all_plugins]
