import webbrowser
from time import sleep
from globals import TEXT, ICON
from plugins import plugin_list
from tools.systray import SysTrayIcon


class MemoryTool(object):
    """
    程序的入口类
    """

    def __init__(self):
        self.plugins = [plugin(self) for plugin in plugin_list]

        self.systray = SysTrayIcon(ICON.icon, TEXT.hover, self.create_menu(),
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
        menu_options.append(('关于', ICON.about, self.about, True))

        return tuple(menu_options)

    def refresh_menu(self):
        """
        刷新菜单
        """
        self.systray.refreshMenu(self.create_menu())

    def about(self, s: SysTrayIcon):
        """
        菜单中的 关于 选项
        """
        webbrowser.open("https://github.com/MemoryD/MemoryTools")

    def bye(self, s: SysTrayIcon):
        """
        退出程序
        """
        self.end = True
        print('bye')

    def run(self):
        """
        启动主程序
        """
        self.systray.start()
        while not self.end:
            sleep(0.1)
            for plugin in self.plugins:
                plugin.start()


if __name__ == '__main__':
    MemoryTool().run()
