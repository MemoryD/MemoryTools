from PIL import Image
from time import sleep

from easydict import EasyDict
from plugins.ocr import OCR
from plugins.alert import Alert
from plugins.copytrans import CopyTrans
from systray import SysTrayIcon
from boxes import ImageBox
from utils import getSrc, readConfig, writeConfig
from setting import HOVER_TEXT, ABOUT_IMG


class MemoryTool(object):
    """
    程序的入口类
    """

    def __init__(self):
        self.icon = getSrc('icon.ico')
        config = readConfig()

        copytrans = CopyTrans(self, config)
        ocr = OCR(self, config)
        alert = Alert(self, config)
        self.plugins = [copytrans, ocr, alert]

        self.systray = SysTrayIcon(self.icon, HOVER_TEXT, self.createMenu(),
                                   on_quit=self.bye, default_menu_index=1,
                                   exit_ico=getSrc('exit.ico')
                                   )

        self.is_about = False
        self.end = False

    def about(self, s: SysTrayIcon):
        """
        菜单中的 关于 选项，如果在线程中调用会出错，因此用一个变量控制，在主线程中显示信息
        """
        self.is_about = True

    def createMenu(self):
        """创建托盘程序的菜单
        菜单中的每一项为元组，每个元组含义如下：
            第 1 项：菜单项名称
            第 2 项：图标路径
            第 3 项：可以递归嵌套子菜单，如果没有子菜单则为回调函数
            第 4 项：表示该项菜单后面是否有一条分割线
        """
        menu_options = []
        for plugin in self.plugins:
            menu_options.append(plugin.initMenu())
        menu_options.append(('关于', getSrc('about.ico'), self.about, True))

        return tuple(menu_options)

    def refreshMenu(self):
        """
        刷新菜单
        """
        self.systray.refreshMenu(self.createMenu())
        self.refreshConfig()

    def refreshConfig(self) -> None:
        """
        写入设置
        """
        config = {}
        for plugin in self.plugins:
            name, con = plugin.getConfig()
            config[name] = con

        writeConfig(config)

    def bye(self, s: SysTrayIcon):
        """退出程序"""
        self.end = True
        print('bye')

    def run(self):
        """启动"""
        self.systray.start()
        while not self.end:
            sleep(0.1)
            if self.is_about:
                self.is_about = False
                img = Image.open(getSrc(ABOUT_IMG))
                ImageBox('Memory Tools').show(img)
            for plugin in self.plugins:
                plugin.start()


if __name__ == '__main__':
    MemoryTool().run()
