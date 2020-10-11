# -*- coding: utf-8 -*-
import json
from pathlib import Path
from easydict import EasyDict
from tools.logger import logger


def change_config(set_attr):
    """
    因为每次更改属性都要刷新托盘菜单，并且写到配置文件中，
    所以定义一个装饰器，以简化代码
    :param set_attr: 更改属性的函数
    :return: 装饰过的函数
    """
    def wrapper(plugin, s):
        f = set_attr(plugin, s)
        plugin.save_config()
        plugin.root.refresh_menu()
        return f

    return wrapper


class BasePlugin(object):
    """
    所有插件的基类，提供插件的统一运行框架。
    每个插件都以一个模块的形式存在，假设在一个插件名为 test，则可以：
     1. 创建一个包为 plugins/test (文件夹名字随意)
     2. 包内至少 2 个文件：
        2.1 __init__.py: 必须包含一个变量 plugin, 指向一个 BasePlugin 的子类
        2.2 test.py（文件名随意）：插件的主要运行代码，其中有一个类必须继承 BasePlugin，并写到 __init__.py 中
     具体可以参阅plugins文件夹下面的几个插件。
    """
    def __init__(self, name: str, root, icon: str, config_path: Path):
        """
        :param name: 该插件的名字，会显示在托盘菜单中
        :param root: MemoryTools类，会由主程序自动传入
        :param icon: 图标的路径
        :param config_path: 配置文件的路径
        """
        self.name = name
        self.root = root
        self.icon = icon
        self.config_path = config_path
        logger.info("[plugin base] 初始化插件: " + self.name)

    def init_config(self):
        """
        读取目录下的配置文件，并将属性绑定到类中，
        如果没有配置文件，则使用默认的配置
        """
        if not self.config_path.exists():
            config = self.create_default_config()
        else:
            config = self.config_path.read_text(encoding="utf-8")
            config = json.loads(config)

        for attr, value in config.items():
            self.__setattr__(attr, value)

        return config

    def save_config(self):
        """
        从类中获取配置的属性，并保存到文件中
        :return:
        """
        for attr in self.config:
            self.config[attr] = self.__getattribute__(attr)

        data = json.dumps(self.config, indent=4, ensure_ascii=False)
        self.config_path.write_text(data, encoding="utf-8")

    def create_default_config(self) -> dict:
        """
        返回默认的配置
        """
        return {}

    def init_menu(self) -> tuple:
        """
        入口菜单项
        """
        return self.name, self.icon, self.create_menu(), True

    def create_menu(self) -> tuple:
        """
        子菜单，格式可以参考 MemoryTools 类中的 create_menu 方法
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        主要运行的函数，会被主程序重复调用
        """
        raise NotImplementedError
