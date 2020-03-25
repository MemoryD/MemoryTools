import os
from PIL import Image
from time import sleep
from ocr import OCR
from alert import Alert
from copytrans import CopyTrans
from threading import Thread
from systrayicon import SysTrayIcon
from boxes import ImageBox
from pic import *
from utils import *
from setting import *


class Root(object):
    def __init__(self):
        self.alert = Alert(self)
        self.ct = CopyTrans(self)
        self.ocr = OCR(self)
        self.icon = 'icon.ico'
        self.is_about = False
        self.end = False
        if not os.path.exists(self.icon):
            getPic(ICON, self.icon)

    def about(self, sysTrayIcon):
        self.is_about = True
        
    def createMenu(self):
        self.menu_options = (
                            ('复制翻译', None, (
                                        (self.ct.pauseText(), None, self.ct.pauseTrans),
                                        (self.ct.languageText(), None, self.ct.turnLanguage),
                                        (self.ct.newlineText(), None, self.ct.turnNewline),
                                        (self.ct.strictText(), None, self.ct.turnStrict)
                                        )),
                            ('OCR识别', None, (
                                        (self.ocr.pauseText(), None, self.ocr.pauseOcr),
                                        (self.ocr.modeText(), None, self.ocr.turnMode),
                                        (self.ocr.newlineText(), None, self.ocr.turnNewline),
                                        )),
                            ('休息提醒', None, (
                                        (self.alert.alertText(), None, self.alert.pauseAlert),
                                        ('更改时间', None, self.alert.changeTime),
                                        )),
                            ('关于', 'menu.ico', self.about)
                            )
        return self.menu_options

    def bye(self, sysTrayIcon):
        self.end = True

    def sti(self):
        SysTrayIcon(self.icon, HOVER_TEXT, self.createMenu(), on_quit=self.bye, default_menu_index=1)

    def run(self):
        thread = Thread(target=self.sti)
        thread.setDaemon(True)
        thread.start()
        while not self.end:
            sleep(0.1)
            if self.is_about:
                self.is_about = False
                img = Image.open(ABOUT_IMG)
                ImageBox('Memory Tools').show(img)
            self.ct.start()
            self.alert.start()
            self.ocr.start()


if __name__ == '__main__':
    Root().run()
