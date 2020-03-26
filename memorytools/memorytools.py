import os
from PIL import Image
from time import sleep
from ocr import OCR
from alert import Alert
from copytrans import CopyTrans
from threading import Thread
from systray import SysTrayIcon
from boxes import ImageBox
from utils import *
from setting import *


class MemoryTool(object):
    '''程序的入口类'''
    def __init__(self):
        self.icon = getSrc('icon.ico')
        config = readConfig()
        self.alert = Alert(self)
        self.ct = CopyTrans(self)
        self.ocr = OCR(self)
        self.alert.setConfig(config['alert'])
        self.ct.setConfig(config['copytrans'])
        self.ocr.setConfig(config['ocr'])

        self.systray = SysTrayIcon(self.icon, HOVER_TEXT, self.createMenu(), \
            on_quit=self.bye, default_menu_index=1, exit_ico=getSrc('exit.ico'))

        self.is_about = False
        self.end = False

    def about(self, sysTrayIcon):
        '''菜单中的 关于 选项，如果在线程中调用会出错，因此用一个变量控制，在主线程中显示信息'''
        self.is_about = True
        
    def createMenu(self):
        '''创建托盘程序的菜单'''
        self.menu_options = (
                            ('复制翻译', getSrc('trans.ico'), self.ct.createMenu()),
                            ('OCR识别', getSrc('ocr.ico'), self.ocr.createMenu()),
                            ('休息提醒', getSrc('alert.ico'), self.alert.createMenu()),
                            ('关于', getSrc('about.ico'), self.about),
                            )
        return self.menu_options

    def refreshMenu(self):
        '''创新菜单'''
        self.systray.refreshMenu(self.createMenu())

    def bye(self, sysTrayIcon):
        '''退出程序时将配置写到文件中'''
        self.end = True
        config = {}
        config['alert'] = self.alert.getConfig()
        config['copytrans'] = self.ct.getConfig()
        config['ocr'] = self.ocr.getConfig()
        writeConfig(config)
        print('bye')

    def run(self):
        '''启动'''
        self.systray.start()
        while not self.end:
            sleep(0.1)
            if self.is_about:
                self.is_about = False
                img = Image.open(getSrc(ABOUT_IMG))
                ImageBox('Memory Tools').show(img)
            self.ct.start()
            self.alert.start()
            self.ocr.start()


if __name__ == '__main__':
    MemoryTool().run()
