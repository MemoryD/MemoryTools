# -*- coding: utf-8 -*-
"""
@name: memorytools
@author: Memory
@date: 2020/10/11
@description: 项目的入口文件
"""
from time import sleep
from tools.logger import logger

logger.info("[MemoryTools] 启动程序")

from tools.systray import SysTrayIcon
from globals import TEXT, ICON
from plugins import plugin_list


class MemoryTool(object):
    """
    程序的入口类
    """

    version = "v2.0.0 beta"

    def __init__(self):
        self.plugins = [plugin(self) for plugin in plugin_list]

        hover_text = "MemoryTools " + self.version
        self.systray = SysTrayIcon(ICON.icon, hover_text, self.create_menu(),
                                   on_quit=self.bye, default_menu_index=1,
                                   exit_ico=ICON.exit
                                   )

        self.end = False

    def create_menu(self):
        """创建托盘程序的菜单
        菜单中的每一项为元组，每个元组含义如下：
            第 1 项：菜单项名称
            第 2 项：图标路径
            第 3 项：可以递归嵌套子菜单，如果没有子菜单则为回调函数
            第 4 项：表示该项菜单后面是否有一条分割线
        """
        menu_options = []
        for plugin in self.plugins:
            menu_options.append(plugin.init_menu())
        # menu_options.append(('关于', ICON.about, self.about, True))

        return tuple(menu_options)

    def refresh_menu(self):
        """
        每次用户点击托盘菜单以后，都要重新刷新菜单。
        """
        self.systray.refreshMenu(self.create_menu())

    def bye(self, s: SysTrayIcon):
        """
        退出程序
        """
        self.end = True

    def run(self):
        """
        启动主程序，由于tkinter组件不能在线程中结束，因此在主线程中调用
        """
        self.systray.start()
        logger.info("[MemoryTools] 插件开始运行...")
        while not self.end:
            sleep(0.1)
            for plugin in self.plugins:
                try:
                    plugin.start()
                except Exception as e:
                    logger.error("[MemoryTools] %s" % e)
        logger.info("[MemoryTools] 退出程序\n")


if __name__ == '__main__':
    MemoryTool().run()
