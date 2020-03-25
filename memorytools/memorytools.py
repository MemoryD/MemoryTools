import os
from PIL import Image
from time import sleep
from ocr import OCR
from alert import Alert
from copytrans import CopyTrans
from threading import Thread
# from systrayicon import SysTrayIcon
from systray import SysTrayIcon
from boxes import ImageBox
from pic import *
from utils import *
from setting import *


class Root(object):
    def __init__(self):
        self.icon = 'icon.ico'
        self.alert = Alert(self)
        self.ct = CopyTrans(self)
        self.ocr = OCR(self)
        self.systray = SysTrayIcon(self.icon, HOVER_TEXT, self.createMenu(), on_quit=self.bye, default_menu_index=1)
        self.is_about = False
        self.end = False
        if not os.path.exists(self.icon):
            bs64toImg(ICON, self.icon)

    def about(self, sysTrayIcon):
        self.is_about = True
        
    def createMenu(self):
        self.menu_options = (
                            ('复制翻译', getSrc('trans.ico'), self.ct.createMenu()),
                            ('OCR识别', getSrc('ocr.ico'), self.ocr.createMenu()),
                            ('休息提醒', getSrc('clock.ico'), self.alert.createMenu()),
                            ('关于', getSrc('about.ico'), self.about),
                            )
        return self.menu_options

    def refreshMenu(self):
        self.systray.refreshMenu(self.createMenu())

    def bye(self, sysTrayIcon):
        self.end = True

    def run(self):
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
    Root().run()
